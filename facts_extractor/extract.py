import json
import os

from argparse import ArgumentParser
from stanfordcorenlp import StanfordCoreNLP
from sys import argv
from sys import path

path.insert(0, '../')
from common.stanfordcorenlp.corenlpfactory import CoreNLPFactory

class FactsExtractor:


    def extract_triples(self, input_filename, verbose=False):
        if not input_filename.startswith('/'):
            input_filename = os.path.dirname(os.path.realpath(__file__)) + '/' + filename

        print('Processing text from {} \nPlease wait, as it may take a while ...'.format(input_filename))

        output_filename = os.path.splitext(input_filename)[0] + '_extracted_triples.txt'
        open(output_filename, 'w').close()

        if verbose:
            print('Searching for triples ...')
        output = self.__openie(input_filename, output_filename, verbose)
        print('Extracted triples were stored at {}'.format(output))

        return output

    def __openie(self, input, output, verbose=False):
        with open(input, 'r') as input_file:
            contents = input_file.read()
            input_file.close()

        nlp = CoreNLPFactory.createCoreNLP()
        annotated = nlp.annotate(contents, properties={'annotators': 'tokenize, ssplit, pos, ner, depparse, parse, openie', 'outputFormat': 'json'})

        json_output = json.loads(annotated)

        for sentence in json_output['sentences']:
            for openie in sentence['openie']:
                with open(output, 'a') as output_file:
                    triple = '{}:({};{};{})'.format(sentence['index'], openie['subject'], openie['relation'], openie['object'])
                    if verbose:
                       print(triple)
                    output_file.write(triple + '\n')
                    output_file.close()

        return output

def main(args):
    arg_p = ArgumentParser('python extractor.py')
    arg_p.add_argument('-f', '--filename', type=str, default=None)
    arg_p.add_argument('-v', '--verbose', action='store_true')

    args = arg_p.parse_args(args[1:])
    filename = args.filename
    verbose = args.verbose

    if filename is None:
        print('No file provided.')
        exit(1)

    extractor = FactsExtractor()
    extractor.extract_triples(filename, verbose)

if __name__ == '__main__':
    exit(main(argv))
