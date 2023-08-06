from cyvcf2 import VCF
from collections import namedtuple, defaultdict
from enum import IntEnum
import numpy as np
import h5py
import argparse
import sys
import os

from sqt.io.fasta import IndexedFasta

from hashlib import shake_128

class Effect(IntEnum):
    none = 0,
    coding_sequence_variant = 1,
    chromosome = 2<<0,
    inframe_insertion = 2<<1,
    disruptive_inframe_insertion = 2<<2,
    inframe_deletion = 2<<3,
    disruptive_inframe_deletion = 2<<4,
    downstream_gene_variant = 2<<5,
    exon_variant = 2<<6,
    exon_loss_variant = 2<<7,
    frameshift_variant = 2<<8,
    gene_variant = 2<<9,
    intergenic_region = 2<<10,
    conserved_intergenic_variant = 2<<11,
    intragenic_variant = 2<<12,
    intron_variant = 2<<13,
    conserved_intron_variant = 2<<14,
    miRNA = 2<<15,
    missense_variant = 2<<16,
    initiator_codon_variant = 2<<17,
    non_coding_exon_variant = 2<<18,
    rare_amino_acid_variant = 2<<19,
    splice_acceptor_variant = 2<<20,
    splice_donor_variant = 2<<21,
    splice_region_variant = 2<<22,
    stop_lost = 2<<23,
    five_prime_UTR_premature = 2<<24,
    start_codon_gain_variant = 2<<25,
    start_lost = 2<<26,
    stop_gained = 2<<27,
    synonymous_variant = 2<<28,
    start_retained = 2<<29,
    stop_retained_variant = 2<<30,
    non_canonical_start_codon = 2<<31,
    protein_protein_contact = 2<<32,
    non_coding_transcript_variant = 2<<33,
    transcript = 2<<34,
    regulatory_region_variant = 2<<35,
    upstream_gene_variant = 2<<36,
    three_prime_UTR_variant = 2<<37,
    three_prime_UTR_truncation_and_exon_loss = 2<<38,
    five_prime_UTR_variant = 2<<39,
    five_prime_UTR_truncation_and_exon_loss_variant = 2<<40,
    five_prime_UTR_premature_start_codon_gain_variant = 2<<41,
    sequence_feature_and_exon_loss_variant = 2<<42
    TF_binding_site_variant = 2 << 43
    non_coding_transcript_exon_variant  = 2 << 44


def store(stored, stored_transcripts, samplenames, out_filenames):
    for samplename, out_filename in zip(samplenames, out_filenames):
        out_file = h5py.File(out_filename, 'w')
        print(out_filename)
        for chrom in sorted(stored[samplename].keys()):
            grp_chrom = out_file.create_group(chrom)

            #stored[samplename][chrom] = [x[0:len(dtype["names"])] for x in stored[samplename][chrom]]

            dtype = {'names':['key', 'transcript_start', 'transcript_stop', 'length', 'qual', 'qd', 'mq', 'effect', 'ref', 'alt_count', 'depth', 'context', 'rsid', 'precious', 'common'],
                    'formats':['uint64', 'uint32', 'uint32', 'uint32', 'float32', 'float32', 'float32', 'int64', 'uint8', 'uint8', 'uint8', 'a3', 'int32', 'bool_', 'bool_']}


            dtype_transcripts = {'names':['variant_id', 'effect', 'gene_id', 'rank_affected', 'rank_total', 'feature_id', 'hgvsc', 'hgvsp', 'distance', 'impact', 'coding'],
                    'formats':['int32', 'int64', 'a20', 'int8', 'int8', 'a20', 'a20', 'a20', 'uint8', 'int32', 'bool_']}

            stored_np = np.array(np.array(stored[samplename][chrom], dtype=dtype))
            stored_transcripts_np = np.array(np.array(stored_transcripts[samplename][chrom], dtype= dtype_transcripts))

            grp_chrom.create_dataset("variants", data=stored_np)
            grp_chrom.create_dataset("variants_transcripts", data=stored_transcripts_np)
            keys = np.unique(stored_np["key"])
            grp_chrom.create_dataset("variant_keys", data=keys, dtype=np.int64)


Annotation = namedtuple("Annotation", "allele effect impact gene geneid featuretype featureid biotype rank hgvsc hgvsp c_pos_len cds_pos protein_pos_len distance errors")


def is_variant(g):
    return g[0] == 1 or g[1] == 1


def is_het(g):
    return g[0] != g[1]



def main(args):
    f = VCF(args.input)

    # identify the used caller
    caller = None
    rawheader = [x.split("=",1) for x in f.raw_header.split("\n")]

    for h in rawheader:
        if h[0] == "##source" and h[1].lower().startswith("freebayes"):
            caller = "freeBayes"

    #for key, value in f.metadata.items():
    #    print(key, value)
    #    if key.startswith("GATK"):
    #        caller = "GATK"

     #   if key == "source" and isinstance(value, list) and len(value) > 0 and value[0].startswith("freeBayes"):
     #       caller = "freeBayes"

    if args.ref is not None:
        print(args.ref)
        fasta_reader = IndexedFasta(args.ref)


    if caller == "freeBayes":
        ac_field = "AO"
        mq_field = "MQM"
        ad_field = "AO"
    elif caller == "GATK":
        ac_field = "AC"
        mq_field = "MQ"
        ad_field = "AD"
    else:
        raise Exception('Unknown Caller')


    stored = defaultdict(lambda: defaultdict(list))
    stored_transcripts = defaultdict(lambda: defaultdict(list))

#    samplenames = args.samples
#    out_filenames = args.output

    if args.samples:
        # if the user provides samples, use them
        samplenames = args.samples
        unknown_samples = set(samplenames) - set(f.samples)
        # if there are unkown samples:
        if unknown_samples:
            print("ERROR following samples are not included in the vcf: ", file=sys.stderr, end="")
            print(*sorted(unknown_samples), sep=", ", file=sys.stderr)
            exit(-1)
    else:
        # else use all samples in the vcf file
        samplenames = f.samples

    # create outputnames corresponding to sample names in the provided out dir
    out_dir = args.outdir
    out_filenames = [os.path.join(out_dir, s + ".h5") for s in samplenames]

    # the coding for the different bases
    base_to_index = { "A": 0, "C": 1, "G": 2, "T": 3 }

    samples = f.samples

    # for each snp in vcf file
    for i, line in enumerate(f):
        if i % 1000 == 0:
            print(i, "variants processed", file=sys.stderr)

        chrom = line.CHROM.upper() #chromosome
        ref   = line.REF #reference base(s)
        pos   = line.POS #position
        rsid = line.ID #dbsnp rsid
        pm = "PM" in line.INFO #precious

        # get rs id number as int, if not existing rsid = 0
        if not rsid: rsid = "rs0"
        rsid = int(rsid.split(";")[0][2:])
        qual  = float(line.QUAL) if line.QUAL else 0 # mapping quality

        genotypes = line.genotypes
        gt_depth = line.gt_depths

        #print(line.gt_alt_depths)
        #print(line.gt_phred_ll_het)
        #print(line.gt_phred_ll_homalt)
        #print(line.gt_quals)
        #print(line.ploidy)
        #exit()

        dp = 0
        for g, d in zip(genotypes, gt_depth):
            if is_variant(g): # is variant
                dp += d

        #dp = sum([s.data.DP for s in line.samples if s.is_variant]) # depth

        # only write for samples with depth > 0
        if dp == 0:
            continue

        # quality per depth
        qd = qual / dp 

#        print(dir(line.INFO))
#        print(line.INFO.get(ac_field))

        # ignore snps with N in ref
        if "N" in ref:
            continue

        common = "COMMON" in line.INFO and line.INFO["COMMON"] == 1

        alt_counts = line.gt_alt_depths

        for samplename, genotype, depth, alt_c in zip(samplenames, genotypes, gt_depth, alt_counts):
            #ignore non variants sample
            if not is_variant(genotype):
                continue

            # get ploidity
            het = is_het(genotype)

            # get annotations (hit transcripts)
            annotations = line.INFO["ANN"].split(",")


            mapping_qualities = line.INFO[mq_field]
            if not type(mapping_qualities) is tuple:
                mapping_qualities = [mapping_qualities]

            for alt, mq in zip(map(str, line.ALT), mapping_qualities):
                # get context (motifs)

                if args.ref is not None and len(alt) == 1 and len(ref) == 1: # if reference was a parameter
                    context = fasta_reader.get(chrom)[line.POS-2:line.POS+1].decode()
                elif "CTX" in line.INFO: # look for ctx tag in vcf
                    context = line.INFO["CTX"][0]
                else:
                    #no context at all
                    context = ""

                effects = 0
                pre_transcript_id = len(stored_transcripts[samplename][chrom])
                for a in annotations:
                    #each transcript has its own annotation
                    A = Annotation(*a.split("|"))
                    coding = A.biotype == "protein_coding" # maybe there are other biotypes
                    distance = A.distance if len(A.distance) else -1

                    if A.rank:
                        rank_affected, rank_total = map(int, A.rank.split("/"))
                    else:
                        rank_affected, rank_total = 0, 0

                    e = 0
                    for effect in A.effect.split("&"):
                        if not effect:
                            effect = "none"
                        reffect_replaced = effect.replace("3_", "three_").replace("5_", "five_")
                        e = e | Effect[reffect_replaced]

                    indel_hash = 0

                    if len(alt) == 1 and len(ref) == 1: # snp
                        typ = base_to_index[alt] # 000, 001, 010, 011
                        ref_char = ord(line.REF)
                    else: #structural variant
                        if len(alt) == len(ref): # mnp
                            typ = 4 # 100
                        elif len(alt) > 1 and len(ref) == 1: #ins
                            indel_hash = int.from_bytes(shake_128(alt.encode()).digest(4), "big")
                            typ = 5 # 101
                        elif len(alt) == 1 and len(ref) > 1: #del
                            indel_hash = len(ref)
                            typ = 6 # 110
                        else: # something else
                            typ = 7 # 110
                        ref_char = 0

                    key = (indel_hash << 32) + (pos << 4) + (typ << 1) + het

                    length = max(len(alt), len(ref))

                    impact = ["MODIFIER", "LOW", "MODERATE", "HIGH"].index(A.impact)
                    effects |= e

                    stored_transcripts[samplename][chrom].append((len(stored[samplename][chrom]), e, A.geneid, rank_affected, rank_total, A.featureid, A.hgvsc, A.hgvsp, distance, impact, coding))
                last_transcript_id = len(stored_transcripts[samplename][chrom])

                stored[samplename][chrom].append((key, pre_transcript_id, last_transcript_id, length, qual, qd, mq, effects, ref_char, alt_c, depth, context, rsid, pm, common))
                pre_transcript_id = last_transcript_id

    #TODO: svm_D additional to impact?

    # create output directories of not exist
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    store(stored, stored_transcripts, samplenames, out_filenames)


def create_parser(parser):
    parser.add_argument("input", help="the input in vcf format")
    parser.add_argument("outdir", help="the output directory")
    parser.add_argument("--samples", nargs="*", help="limit the output creation to these samples")
    parser.add_argument("--ref", help="the reference in fasta format to extract a variant motifs information", default=None)
    parser.set_defaults(func=main)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    create_parser(parser)
    args = parser.parse_args()

    main(args)

