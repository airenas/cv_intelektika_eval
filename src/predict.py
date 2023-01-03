import argparse
import os
import queue
import sys
import threading

from tqdm import tqdm

from src.transcriber import Transcriber


class Work:
    def __init__(self, file: str):
        self.file = file
        self.wait_queue = queue.Queue(maxsize=1)
        self.str = ""

    def done(self):
        return self.wait_queue.put(self, block=False)

    def wait(self):
        return self.wait_queue.get()

    def predict(self, trans) -> str:
        self.str = predict(trans, self.file)
        self.done()


def predict(trans, file):
    return trans.predict(file)


def main(argv):
    parser = argparse.ArgumentParser(description="Does Common Voice dataset prediction",
                                     epilog="E.g. " + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--in_f", nargs='?', required=True, help="List file")
    parser.add_argument("--l", nargs='?', required=True, help="Audio file directory")
    parser.add_argument("--url", nargs='?', default="https://atpazinimas.intelektika.lt", help="Transcriber URL")
    args = parser.parse_args(args=argv)

    trans = Transcriber(args.url)

    jobs = []
    with open(args.in_f, 'r') as in_f:
        for line in in_f:
            line = line.strip()
            if not line:
                continue
            strs = line.split("\t")
            f = strs[0]
            fa = "%s/%s" % (args.l, f)
            jobs.append(Work(fa))

    job_queue = queue.Queue(maxsize=10)
    workers = []
    wc = 15

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

    def start():
        while True:
            _j = job_queue.get()
            if _j is None:
                return
            _j.predict(trans)

    for i in range(wc):
        start_thread(start)

    with tqdm("read mappings", total=len(jobs)) as pbar:
        for i, j in enumerate(jobs):
            j.wait()
            pbar.update(1)
            print("%s\t%s" % (os.path.basename(j.file), j.str))
    for w in workers:
        w.join()


if __name__ == "__main__":
    main(sys.argv[1:])
