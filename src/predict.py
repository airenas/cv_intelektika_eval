import argparse
import os
import queue
import sys
import threading
from pathlib import Path

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, TimeElapsedColumn, MofNCompleteColumn

from src.transcriber import Transcriber


class Work:
    def __init__(self, file: str, cache_dir: str = ""):
        self.file = file
        self.cache_file = Path(cache_dir) / (os.path.basename(file) + ".txt")
        self.wait_queue = queue.Queue(maxsize=1)
        self.str = ""

    def done(self):
        return self.wait_queue.put(self, block=False)

    def wait(self):
        return self.wait_queue.get()

    def predict(self, trans, update_f) -> str:
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                self.str = f.read()
        else:
            self.str = predict(trans, self.file, update_f)
            with open(self.cache_file, 'w') as f:
                f.write(self.str)

        self.done()


def predict(trans, file, update_f):
    txt, _ = trans.predict(file, update_f)
    return txt


def main(argv):
    parser = argparse.ArgumentParser(description="Does Common Voice dataset prediction",
                                     epilog="E.g. " + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--in_file", nargs='?', required=True, help="List file")
    parser.add_argument("--l", nargs='?', required=True, help="Audio file directory")
    parser.add_argument("--url", nargs='?', default="https://atpazinimas.intelektika.lt", help="Transcriber URL")
    parser.add_argument("--out_file", nargs='?', required=True, help="Output file for transcriptions")
    parser.add_argument("--cache_dir", nargs='?', default="", help="Cache directory")
    parser.add_argument("--old_clean", nargs='?', type=int, default="0", help="Use old clean service")
    parser.add_argument("--key", nargs='?', required=False, help="Transcription API secret key")
    parser.add_argument("--workers", nargs='?', type=int, default=4, help="Workers count")

    args = parser.parse_args(args=argv)

    if not args.cache_dir:
        raise RuntimeError("Cache dir is required")

    trans = Transcriber(url=args.url, old_clean=args.old_clean, model="ben", speakers="", key=args.key)

    jobs = []
    with open(args.in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip()
            if not line:
                continue
            strs = line.split("\t")
            f = strs[0]
            fa = "%s/%s" % (args.l, f)
            jobs.append(Work(file=fa, cache_dir=args.cache_dir))

    job_queue = queue.Queue(maxsize=10)
    workers = []
    wc = args.workers

    print("URL    : {}".format(args.url))
    print("Workers: {}".format(args.workers))
    print("Files  : {}".format(len(jobs)))
    print("In     : {}".format(args.out_file))
    print("Out    : {}".format(args.in_file))

    def add_jobs():
        for _j in jobs:
            job_queue.put(_j)
        for _i in range(wc):
            job_queue.put(None)

    def start_thread(method):
        thread = threading.Thread(target=method, daemon=True)
        thread.start()
        workers.append(thread)

    start_thread(add_jobs)

    progress = Progress()
    overall_progress = Progress(*Progress.get_default_columns(), TimeElapsedColumn(), MofNCompleteColumn())
    overall_task = overall_progress.add_task("All Files", total=len(jobs))

    def start():
        task = progress.add_task("Transcribing", total=100)
        while True:
            _j = job_queue.get()
            if _j is None:
                return
            _f = os.path.basename(_j.file)
            _f, _ = os.path.splitext(_f)

            def update(st, name):
                progress.update(task, description=f"{_f} - {name}")
                progress.update(task, completed=st)

            progress.update(task, description=f"{_f} - Uploading", total=100)

            _j.predict(trans, update)
            overall_progress.update(overall_task, advance=1)

    for i in range(wc):
        start_thread(start)

    progress_group = Group(Panel(Group(progress)), Panel(Group(overall_progress)), )
    with open(args.out_file, 'w') as out_f:
        with Live(progress_group, refresh_per_second=4):
            for j in jobs:
                j.wait()
                out_f.write("%s\t%s\n" % (os.path.basename(j.file), j.str.replace("\n", " ")))

    for w in workers:
        w.join()


if __name__ == "__main__":
    main(sys.argv[1:])
