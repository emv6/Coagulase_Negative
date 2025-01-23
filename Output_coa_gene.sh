#!/bin/bash


# Input file containing the virulome data

input_file="coa_virulome.txt"

output_file_positive="samtoolscoord_positive.fa"

output_file_negative="samtoolscoord_negative.fa"

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