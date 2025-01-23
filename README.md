# Coagulase_Negative
![bash](https://img.shields.io/badge/language-bash-green)
![Python](https://img.shields.io/badge/language-Python-blue)
![R](https://img.shields.io/badge/language-R-red)

Identification of Coagulase Negative Variants of *Staphylococcus aureus* within New Zealand Dairy Cows. All genomic analysis was run on New Zealand eScience Infrastructure [NeSI](https://github.com/nesi) unless specified.

## FastQC 
[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) was used to check for QC of the samples for adaptor content and sequence quality
```#!/bin/bash -e
#SBATCH --cpus-per-task=8 --mem 50Gb --time 1:00:00 -J FASTQC_EV

module load FastQC/0.11.9

FASTQC = /pathtorawreads
OUTPUT_DIR = /processedreadsdirectory/FASTQC/

mkdir -p $OUTPUT_DIR

for file in $FASTQC/*.fq.gz;
do
if [-f $FILE ];
then echo "Running FastQC on $FILE"
fastqc $FILE -o $OUTPUTDIR
else
echo "No FASTQ files found in $FASTQ"
fi
done
echo "FastQC analysis completed for all samples"
```
## Kraken2 
To identify the species assignment of the 1308 NAS isolates sequenced 
Script for [Kraken2 Analysis](https://github.com/emv6/Coagulase_Negative/blob/main/Kraken2.sh)
Script for analysing [Kraken2 Reports](https://github.com/emv6/Coagulase_Negative/blob/main/Kraken2_Report.py)

## [SKESA](https://github.com/ncbi/SKESA) Assembly 
Genome Assembly was completed using a [SKESA script](https://github.com/emv6/Coagulase_Negative/blob/main/skesa.sh)

## [ABRicate](https://github.com/tseemann/abricate)
```bash
#Virulence Factor Database
abricate --mincov 55 --minid 90 *_contigs.fasta --db VFDB > summary_vfdb.txt
```
```bash
#Resistome
abricate --mincov 55 --minid 90 *_contigs.fasta --db CARD > summary_card.txt
```

## [Prokka](https://github.com/tseemann/prokka)
```
#!/bin/bash
assembly_dir=assembly/Coag_Neg/
output_dir=assembly/Coag_Neg/prokka_annotations

mkdir -p $output_dir

for assembly in $assembly_dir/*.fasta; do
base_name=$(basename $assembly .fasta)

prokka --outdir $output_dir/$base_name \
       --prefix $base_name \
       --genus Staphylococcus \
       --kingdom Bacteria \
       --cpus 8 \
       $assembly
done
``` 


## Defining *Spa* Types 
*Spa* Types were determined using [SpaTyper](https://github.com/HCGB-IGTP/spaTyper). The list of genomes is made from the contigs.fa created by SKESA. 
```ls *.fa > list_of_genomes.txt ##Creating a list of genomes from all fastq files 
sed -i '1 i\spaTyper  -f ' list_of_genomes.txt
echo "--output spa.xls" &>> list_of_genomes.txt
tr '\n' ' ' < list_of_genomes.txt > spa_command.txt
chmod +x spa_command.txt
./ spa_command.txt
```
## Defining *agr* types
[AGRvate](https://github.com/VishnuRaghuram94/AgrVATE) was used to identify each genomes *agr* type. A conda environment was created then the contig fasta files was used as input for AGRvate. 

## Studying the Staphylocoagulase (*coa*) gene
Script that analyses Virulome file for matches to the gene coagulase(*coa*) gene - [coa_matches](https://github.com/emv6/Coagulase_Negative/blob/main/coa_match.py) \
Script analyses the coa_match and uses samtools to output the nucleotide sequence for the *coa* match. [Output_Coa_Gene](https://github.com/emv6/Coagulase_Negative/blob/main/Output_coa_gene.sh)

Convert the *coa* gene matches identified on the reverse strand to the reverse complement using seqtk \
`module load seqtk/1.4-GCC-11.3.0` \
`seqtk seq -r samtoolscoord_negative.fa > samtoolscoord_negative_reversecomp.fa` \
`cat samtoolscoord_negative_reversecomp.fa samtoolscoord_positive.fa > coa_sequences.fa` 

[Translate](https://www.bioinformatics.org/sms2/translate.html) *coa* sequences to protein sequences







