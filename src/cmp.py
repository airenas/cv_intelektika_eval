import argparse
import sys

from src.normalizer import normalize


def main(argv):
    parser = argparse.ArgumentParser(description="Cmp word to word reference and predictions",
                                     epilog="E.g. " + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--ref", nargs='?', required=True, help="Reference file")
    parser.add_argument("--pred", nargs='?', required=True, help="Predictions file")
    parser.add_argument("--n", nargs='?', default=20, help="Take first n sentences")
    args = parser.parse_args(args=argv)

    def read_file(f):
        res = []
        with open(f, 'r') as in_f:
            for line in in_f:
                line = line.strip()
                if not line:
                    continue
                strs = line.split("\t")
                res.append(strs[1])
        return res

    refs = read_file(args.ref)
    pred = read_file(args.pred)

    for i in range(int(args.n)):
        reference, predicted = refs[i], pred[i]
        print("reference:", reference)
        print("predicted:", predicted)
        print('---')


if __name__ == "__main__":
    main(sys.argv[1:])
