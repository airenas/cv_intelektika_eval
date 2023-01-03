import argparse
import sys

from evaluate import load
from jiwer import compute_measures

from src.normalizer import normalize


def main(argv):
    parser = argparse.ArgumentParser(description="Calculates WER",
                                     epilog="E.g. " + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--ref", nargs='?', required=True, help="Reference file")
    parser.add_argument("--pred", nargs='?', required=True, help="Predictions file")
    args = parser.parse_args(args=argv)

    def read_file(f):
        res = []
        with open(f, 'r') as in_f:
            for line in in_f:
                line = line.strip()
                if not line:
                    continue
                strs = line.split("\t")
                res.append(normalize(strs[1]))
        return res

    refs = read_file(args.ref)
    pred = read_file(args.pred)

    print("Refs: {}, Predictions: {}".format(len(refs), len(pred)))
    refs = refs[:len(pred)]

    wer = load("wer")
    wer_score = wer.compute(predictions=refs, references=pred)
    print("WER: {:.2f}".format(100 * wer_score))

    res = compute_measures(truth=refs, hypothesis=pred)
    print(res)
    print("Err: {}/{}, (s: {}, d: {}, i: {})".format(res['substitutions'] + res['deletions'] + res['insertions'],
                                                     res['hits'] + res['substitutions'] + res['deletions'],
                                                     res['substitutions'], res['deletions'], res['insertions']))


if __name__ == "__main__":
    main(sys.argv[1:])
