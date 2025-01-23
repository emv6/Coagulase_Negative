#!/usr/bin/env python 3

def print_header ():
    header = """
======================================
Script Name is Coamatches.py
Description:
    This script searches a virulome file for matches to the gene coagulase (coa) and outputs the line matches to a text file for further analysis

Author: Emma Voss
Version 1.1

=======================================

"""
    print(header)
print_header()


input_file = "VFDB_Output.tab" 
output_file = "coa_virulome.txt"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        if "coa" in line: #Check to see if coa is in the line
            outfile.write(line) #write the matching line to the out file

print(f"Lines containing 'coa' have been saved to {output_file}.")