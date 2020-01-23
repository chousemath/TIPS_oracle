import sys
from mpark_parser import export_csv


def main(_from, _to):
    export_csv(_from, _to)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
