# Coagulase_Negative
Identification of Coagulase Negative Variants of *Staphylococcus aureus* within New Zealand Dairy Cows

All genomic analysis was run on New Zealand eScience Infrastructure (NESI) unless specified

### Kraken2 
To identify the species assignment of the 1308 NAS isolates sequenced 
Script for [Kraken2 Analysis](https://github.com/emv6/Coagulase_Negative/blob/main/Kraken2.sh)
Script for analysing [Kraken2 Reports](https://github.com/emv6/Coagulase_Negative/blob/main/Kraken2_Report.py)

### [SKESA](https://github.com/ncbi/SKESA) Assembly 
Genome Assembly was completed using a [SKESA script](https://github.com/emv6/Coagulase_Negative/blob/main/skesa.sh)

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
Script that analyses Virulome file for matches to the gene coagulase(*coa*) gene - [coa_matches](https://github.com/emv6/Coagulase_Negative/blob/main/coa_match.py) \
Script analyses the coa_match and uses samtools to output the nucleotide sequence for the *coa* match. [Output_Coa_Gene](https://github.com/emv6/Coagulase_Negative/blob/main/Output_coa_gene.sh)

Convert the *coa* gene matches identified on the reverse strand to the reverse complement using seqtk \
`module load seqtk/1.4-GCC-11.3.0` \
`seqtk seq -r samtoolscoord_negative.fa > samtoolscoord_negative_reversecomp.fa` \
`cat samtoolscoord_negative_reversecomp.fa samtoolscoord_positive.fa > coa_sequences.fa` 

[Translate](https://www.bioinformatics.org/sms2/translate.html) *coa* sequences to protein sequences







