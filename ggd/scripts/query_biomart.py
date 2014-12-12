import argparse
import requests
import sys


def main():

  # create the top-level parser
  parser = argparse.ArgumentParser(prog='query_biomart')
  parser.add_argument('--dataset',
    dest='ensembl_dataset',
    metavar='STRING',
    help='The ENSEMBL dataset to use.')
  parser.add_argument('--atts',
    dest='attributes',
    nargs = '*',
    metavar='STRING',
    help='The BioMart attributes to retreive.')
  # parse the args and call the selected function
  args = parser.parse_args()

  urlStart = \
      '''http://ensembl.org/biomart/martservice?query=''' \
      '''<?xml version="1.0" encoding="UTF-8"?>''' \
      '''<!DOCTYPE Query>''' \
      '''<Query virtualSchemaName="default" formatter="TSV" header="0" uniqueRows="0" count="" datasetConfigVersion="0.6">''' \
      '''<Dataset name="%s" interface="default">''' % (args.ensembl_dataset)
  urlColumns = ""

  # add the requested columns to the XML request
  for attribute in args.attributes:
      urlColumns += \
      '''<Attribute name="''' + attribute + '''"/>'''
  urlEnd = \
      '''</Dataset>''' \
      '''</Query>'''

  url = urlStart + urlColumns + urlEnd
  req = requests.get(url, stream=True)
  for line in req.iter_lines():
      print line
   
if __name__ == '__main__':
  """
  Ex. query_biomart.py --dataset hsapiens_gene_ensembl   \
                       --atts chromosome_name exon_chrom_start exon_chrom_end
  """
  main()


