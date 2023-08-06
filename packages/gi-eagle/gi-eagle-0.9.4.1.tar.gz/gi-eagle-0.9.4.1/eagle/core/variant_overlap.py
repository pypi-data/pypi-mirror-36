'''calculate the venn diagramm counts for 3 samples'''
import argparse

import numpy as np

from eagle.core.common import NamedDict
from eagle.core.wrap.sample import Sample


def venn_counts(a, b, c):
    in_abc = np.intersect1d(a, np.intersect1d(b, c)).shape[0]
    in_ab = np.intersect1d(a, b).shape[0] - in_abc
    in_ac = np.intersect1d(a, c).shape[0] - in_abc
    in_bc = np.intersect1d(b, c).shape[0] - in_abc
    in_a = a.shape[0] - in_ab - in_ac - in_abc
    in_b = b.shape[0] - in_ab - in_bc - in_abc
    in_c = c.shape[0] - in_ac - in_bc - in_abc
    return np.array((in_abc, in_ab, in_ac, in_bc, in_a, in_b, in_c))


def shift_keys(s, chrom):
    v = s.variants(chrom, fields=["key"])
    if v is None:
        return np.array([])
    return s.variants(chrom, fields=["key"])["key"].astype(np.int64) >> 1


def run(sample1, sample2, sample3):
    # VennCounts = namedtuple("VennCounts", "abc ab ac bc a b c")

    s1 = Sample(sample1)
    s2 = Sample(sample2)
    s3 = Sample(sample3)

    all_venn_counts = np.zeros(7, dtype="int")

    chromosomes = set(s1.chromosomes)
    chromosomes.union(s2.chromosomes)
    chromosomes.union(s3.chromosomes)

    for chrom in chromosomes:
            v1 = shift_keys(s1, chrom)
            v2 = shift_keys(s2, chrom)
            v3 = shift_keys(s3, chrom)
            all_venn_counts += venn_counts(v1, v2, v3)

    abc, ab, ac, bc, a, b, c = all_venn_counts

    ret = {
        "abc": abc,
        "ab": ab,
        "ac": ac,
        "bc": bc,
        "a": a,
        "b": b,
        "c": c,
        }

    ret = NamedDict(ret)

    return ret


def out(venncount):
    # TODO better numpy savetxt to stdout with format
    print("abc", venncount.abc, sep="\t")
    print("ab", venncount.ab, sep="\t")
    print("ac", venncount.ac, sep="\t")
    print("bc", venncount.bc, sep="\t")
    print("a", venncount.a, sep="\t")
    print("b", venncount.b, sep="\t")
    print("c", venncount.c, sep="\t")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sample1")
    parser.add_argument("sample2")
    parser.add_argument("sample3")
    # TODO quality filter
    args = parser.parse_args()

    out(run(args.sample1, args.sample2, args.sample3))


if __name__ == "__main__":
    main()
