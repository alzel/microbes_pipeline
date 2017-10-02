import os
import sys
import re
import glob
from collections import Counter


import argparse

parser = argparse.ArgumentParser(description='Reads input directory of paired end reads and generates output file',
                                 epilog='Example of use: '
                                        'generate_map.py "./data/*" output_test.tsv -e .fastq.gz')
parser.add_argument("input_dir", type=str,
                    help="Input pattern, glob format")
parser.add_argument("output_file", type=str,
                    help="Name of the output file")
parser.add_argument("-e", "--ending", type=str, default=".fastq.gz",
                    help="Common ending of all files")

args = parser.parse_args()


# Return the longest common suffix in a list of strings
def longest_common_suffix(list_of_strings):
        reversed_strings = [' '.join(s.split()[::-1]) for s in list_of_strings]
        reversed_lcs = os.path.commonprefix(reversed_strings)
        lcs = ' '.join(reversed_lcs.split()[::-1])
        return lcs


path = args.input_dir
output_file = args.output_file

#path = './2017-08-23_test/*'
#output_file = "test"
head, tail = os.path.split(path)

# tail = re.sub(r'^[*]+', 'X', tail)
# print("###{0}###".format(tail))

ending = ".fastq.gz"


listing = glob.glob(path)


if not listing:
    print ('no matches')
    sys.exit()

naked_files = []
for element in listing:
    head, file = os.path.split(element)
    result = re.search(ending, element)
    if result:
        file = re.sub(ending, "",  file)
        file = re.sub("[1,2]$", "", file)
        naked_files.append(file)


f = open(output_file,'w')
for file, count in Counter(naked_files).items():
    if count == 2:
        file1 = file + "1" + ending
        file2 = file + "2" + ending

        sample = longest_common_suffix([file1, file2])
        sample = re.sub(r'[_.]$', '', sample)

        file1 = os.path.join(head, file1)
        file2 = os.path.join(head, file2)
        f.write("{0}\t{1},{2}\n".format(sample, file1, file2))
    elif count == 1:
        r = re.compile(".*?{0}.*?".format(file))
        newlist = list(filter(r.match, listing))
        if len(newlist) == 1:
             sample = re.sub(r'[_.]$', '', file)
             f.write("{0}\t{1}\n".format(sample, newlist[0]))


f.close()

