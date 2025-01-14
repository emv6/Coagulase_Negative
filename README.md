# Coagulase_Negative
Identification of Coagulase Negative Variants of *Staphylococcus aureus* within New Zealand Dairy Cows

All genomic analysis is run on New Zealand eScience Infrastructure (NESI) unless specified

### Kraken2 
To identify the species assignment of the 1308 NAS isolates sequenced 
```bash
#!/bin/bash

CONF=0.5
DAT=`find ${1} -name "*R1*.fastq.gz"`
mkdir -p /Sequencing_Reports/
OUTPUT=/Sequencing_Reports/

for i in ${DAT[@]}
do
        FQ1=${i}
        FQ2=`echo ${i} | sed s/R1/R2/`
        echo $FQ1
        echo $FQ2
        base=$(basename ${i}  _R1_001.fastq.gz)
        echo "basename is ${base}"
        echo "#!/bin/bash" > tmp.sh
        echo "set -x; module load Kraken2; kraken2 --confidence ${CONF} --report ${OUTPUT}/${base}.report --threads 24 --paired ${FQ1} ${FQ2} > ${OUTPUT}/${base}.log" >> tmp.sh
        sbatch -J KrakenIllumina_EV --mem 80G --time 0-1 -c 24  tmp.sh
        sleep 0.5
done
```
```python
import os
import glob
def parse_kraken_report(file_path, rank):

##Kraken2 report file and return the top 3 entries for the given rank.

   top_entries = []
   with open(file_path, 'r') as file:
       for line in file:
           cols = line.strip().split('\t')
           if len(cols) < 6:
               continue
           percentage, _, _, tax_rank, _, name = cols
           if tax_rank == rank:  # Filter by rank
               top_entries.append((float(percentage), name.strip()))
   return sorted(top_entries, reverse=True)[:3]
def summarize_reports(input_folder, output_file, rank):

##Summarize the top entries from Kraken2 reports and save to a single file.
  
   report_files = glob.glob(os.path.join(input_folder, "*.report"))
   with open(output_file, 'w') as out_file:
       out_file.write("Combined Kraken2 Report Summary\n")
       out_file.write("=" * 50 + "\n\n")
       for report_file in report_files:
           file_name = os.path.basename(report_file)
           top_entries = parse_kraken_report(report_file, rank)
           out_file.write(f"Summary for {file_name}\n")
           out_file.write("Top 3 by percentage:\n")
           for percentage, name in top_entries:
               out_file.write(f"  {name}: {percentage:.2f}%\n")
           out_file.write("\n")
def print_summary(output_file):

##Print the location of the combined summary file.

   print(f"Combined summary saved in: {output_file}")

# Usage
input_folder = "/Kraken_output/"
output_file = "combined_summary.txt"
rank = "S"  # Use "S" for species or "G" for genus
summarize_reports(input_folder, output_file, rank)
print_summary(output_file)
```
### [SKESA](https://github.com/ncbi/SKESA) Assembly 
Genome Assembly was completed using a SKESA script

```bash
#!/bin/bash -e
#SBATCH --cpus-per-task=20 --mem 50Gb --time 166:00:00 -J EV_SKESA_MULTI

module purge
module load SKESA/2.4.0-gimpi-2022a_saute.1.3.0_1

INPUT=Coagulase_Negative.txt #txt file filename in column 1, R1 in column 2 and R2 in column 3

#Output Directory for contigs
mkdir -p ~/SKESA_Contigs/
output_dir=~/SKESA_Contigs

#Ensure the INPUT variable is set
if [ -z $INPUT ]; then echo "Error: INPUT variable is not set!"
exit 1
fi

#Check the INPUT file exists
if [ ! -f $INPUT ]; then echo "Error: File $INPUT not found!"
exit 1
fi

#Read the input file line by line
while IFS=$'\t' read -r isolate_name r1_path r2_path;
do
if [ -f $r1_path ] && [ -f $r2_path ]; then

echo "Starting processing for isolate: $isolate_name"

#Run Skesa
echo Running: skesa --reads \"$r1_path\" \"$r2_path\" --contigs_out \"$output_dir/${isolate_name}_contigs.fasta\ ""

skesa --reads $r1_path $r2_path --contigs_out $output_dir/${isolate_name}_contigs.fasta

if [ $? -eq 0 ]; then
echo "Finished processing for isolate: $isolate_name"
else
"Error: SKESA failed for isolate: $isolate_name"
fi
else
echo "Warning: Files for isolate $isolate_name not found, skipping....."
fi
done < $INPUT

echo "Contigs generation completed. Check the $output_dir directory"\
```
### [ABRicate](https://github.com/tseemann/abricate)
```bash
#Virulence Factor Database
abricate --mincov 55 --minid 90 *_contigs.fasta --db VFDB > summary_vfdb.txt
```
```bash
#Resistome
abricate --mincov 55 --minid 90 *_contigs.fasta --db CARD > summary_card.txt
```

### Studying the Staphylocoagulase (*coa*) gene
```python
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
```
```bash
#!/bin/bash


# Input file containing the virulome data

input_file="coa_virulome.txt"

output_file_positive="samtoolscoord_positive.txt"

output_file_negative="samtoolscoord_negative.txt"

# Clear or create the output files
> "$output_file_positive"
> "$output_file_negative"

# Read each line of the input file
while IFS=$'\n' read -r line; do

 # Skip empty lines
 if [[ -z "$line" ]]; then
   continue
 fi

 # Extract fields using awk
 read contig_file contig_name start_coord end_coord strand <<< $(echo "$line" | awk '{print $1, $2, $3, $4, $5}')

 #Print extracted values to ensure they are correct
 echo "Processing line: $line"
 echo "Extracted values - File: $contig_file, Contig: $contig_name, Start: $start_coord, End: $end_coord, Strand: $strand"

 # Checking samtools command
 samtools_command="samtools faidx $contig_file $contig_name:$start_coord-$end_coord"

 # Execute the samtools command and append output to the appropriate file
 if [[ "$strand" == "+" ]]; then
   echo "Writing to positive file: $output_file_positive"
   $samtools_command | sed -e "s|>|> ${contig_file}_${strand}_|" >> "$output_file_positive"
 elif [[ "$strand" == "-" ]]; then
   echo "Writing to negative file: $output_file_negative"
   $samtools_command | sed -e "s|>|> ${contig_file}_${strand}_|" >> "$output_file_negative"
 else
   echo "Strand is neither '+' nor '-': $strand"
 fi

done < "$input_file"
```
Convert the *coa* gene matches identified on the reverse strand to the reverse complement using seqtk \
`module load seqtk/1.4-GCC-11.3.0` \
`seqkit seq -r samtoolscoord_negative.txt > samtoolscoord_negative_reversecomp.txt` \
`cat samtoolscoord_negative_reversecomp.txt samtoolscoord_positive.txt > coa_sequences.txt` 

[Translate](https://www.bioinformatics.org/sms2/translate.html) *coa* sequences to protein sequences







