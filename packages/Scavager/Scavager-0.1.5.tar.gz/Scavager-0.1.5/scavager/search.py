from __future__ import division
import argparse
from . import main
import pkg_resources

def run():
    parser = argparse.ArgumentParser(
        description='postsearch analysis of peptides and proteins',
        epilog='''

    Example usage
    -------------
    $ scavager input.pep.xml -prefix DECOY_ -fdr 1.0
    -------------
    ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', help='input pepXML file')
    parser.add_argument('-prefix', help='decoy prefix', default='DECOY_')
    parser.add_argument('-o', help='path to output folder', default=False)
    parser.add_argument('-db', help='path to fasta file. \
                        Used for sequence coverage and LFQ calculation', default=False)
    parser.add_argument('-fdr', help='false discovery rate in %%', default=1.0, type=float)
    parser.add_argument('-e', help='Used only for msgf+ and Morpheus search engines.\
    Cleavage rule in quotes! X!Tandem style for cleavage rules. Examples:\
    "[RK]|{P}" means cleave after R and K, but not before P;\
    "[X]|[D]" means cleave before D;\
    "[RK]|{P},[M]|[X]" means mix of trypsin and cnbr', default='[RK]|{P}')
    parser.add_argument('-allowed_peptides', help='Path to file with peptides considered in postsearch analysis.\
    Sequences must be separated by new line. For example, it can be variant peptides and its decoys in case \
    of proteogenomics searches for group-specific FDR calculation', default='')
    parser.add_argument('-version', action='version', version='%s' % (pkg_resources.require("scavager")[0], ))
    args = vars(parser.parse_args())
    main.process_file(args)
    print('The search is finished.')



if __name__ == '__main__':
    run()
