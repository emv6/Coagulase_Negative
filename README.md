# Coagulase_Negative
![bash](https://img.shields.io/badge/language-bash-green)
![Python](https://img.shields.io/badge/language-Python-blue)
![R](https://img.shields.io/badge/language-R-red)

Identification of Coagulase Negative Variants of *Staphylococcus aureus* within New Zealand Dairy Cows. All genomic analysis was run on New Zealand eScience Infrastructure [NeSI](https://github.com/nesi) unless specified.

## Quality Control
### FastQC 
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
### Kraken2 
To identify the species assignment of the 1274 NAS isolates sequenced 
script for [Kraken2 Analysis](https://github.com/emv6/Coagulase_Negative/blob/main/Kraken2.sh)
Script for analysing [Kraken2 Reports](https://github.com/emv6/Coagulase_Negative/blob/main/Kraken2_Report.py)

## [SKESA](https://github.com/ncbi/SKESA) Assembly 
Genome Assembly was completed using a [SKESA script](https://github.com/emv6/Coagulase_Negative/blob/main/skesa.sh)

## Genomic Analysis 
### [ABRicate](https://github.com/tseemann/abricate)
```bash
#Virulence Factor Database
abricate --mincov 55 --minid 90 *_contigs.fasta --db VFDB > summary_vfdb.txt
```
```bash
#Resistome
abricate --mincov 55 --minid 90 *_contigs.fasta --db CARD > summary_card.txt
```
### [Prokka](https://github.com/tseemann/prokka) annotatation of bacterial genes in the atypical coagulase-negative 95 isolates. 
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
### Defining *Spa* Types 
*Spa* Types were determined using [SpaTyper](https://github.com/HCGB-IGTP/spaTyper). The list of genomes is made from the contigs.fa created by SKESA. 
```ls *.fa > list_of_genomes.txt ##Creating a list of genomes from all fastq files 
sed -i '1 i\spaTyper  -f ' list_of_genomes.txt
echo "--output spa.xls" &>> list_of_genomes.txt
tr '\n' ' ' < list_of_genomes.txt > spa_command.txt
chmod +x spa_command.txt
./ spa_command.txt
```
### Defining *agr* types
[AGRvate](https://github.com/VishnuRaghuram94/AgrVATE) was used to identify each genomes *agr* type. A conda environment was created then the contig fasta files was used as input for AGRvate. 

### Multilocus Sequence Typing [MLST](https://github.com/tseemann/mlst)
```mlst --scheme saureus Coag_Neg/*_contigs.fasta```

### [FastANI](https://github.com/ParBLiSS/FastANI) was used to determine the mean average nucleotide identity comparing the 22 coagulase-positive *S. aureus* to 95 atypical coagulase-negative *S. aureus* with the visualisation in [R](https://github.com/emv6/Coagulase_Negative/blob/main/CoagNeg_HeatMap.Rmd). 
```#!/bin/bash
#SBATCH -J 12566_FastANI
#SBATCH --time 00:30:00
#SBATCH --mem 10GB
#SBATCH --ntasks=1
#SBATCH --array=0-116
#SBATCH --cpus-per-task=15

# Working directory
cd Coag_Negative/FASTANI/

#Load module
module purge
module load FastANI/1.33-GCC-11.3.0

#Creating the array
MY_FILE_LIST=file_paths.txt
LIST_OF_ALL_FILES=(`cat ${MY_FILE_LIST}`)
ARRAY_ITEM=${LIST_OF_ALL_FILES[$SLURM_ARRAY_TASK_ID]}

#Run FastANI
echo ${ARRAY_ITEM}
fastANI -r ${ARRAY_ITEM} --ql $MY_FILE_LIST -o ${SLURM_ARRAY_TASK_ID}.txt
```
## Coagulase-Negative Tree 
### [Snippy](https://github.com/tseemann/snippy) Generating an alignment comparing the 95 atypical coagulase-negative *S. aureus* to the reference bovine *S. aureus* RF122 genome. 
```
#!/bin/bash -e
#SBATCH --cpus-per-task=20 --mem 50Gb --time 166:00:00 -J 12566_SNIPPY_EV

REF=Staphylococcus_aureus_RF122_NC_007622.1.fasta
INPUT=CC151_All_NZ_International.txt

snippy-multi $INPUT --ref $REF --cpus 16 > CC151_coa.sh

echo CC151_coa.sh has been made

sh ./CC151_coa.sh
```
### [IQ-TREE2](https://github.com/iqtree/iqtree2) Input is an alignment file and output is a phylogenetic tree visualised in [TreeViewer](https://github.com/arklumpus/TreeViewer)
```#!/bin/bash -e
#SBATCH --cpus-per-task=8 --mem 50Gb --time 166:00:00 -J IQTREE_EV

iqtree2 -s clean.full.aln -B 1000 -m JC+G
```
## Studying the Staphylocoagulase (*coa*) gene
Script that analyses Virulome file for matches to the gene coagulase(*coa*) gene - [coa_matches](https://github.com/emv6/Coagulase_Negative/blob/main/coa_match.py) \
Script analyses the coa_match and uses samtools to output the nucleotide sequence for the *coa* match. [Output_Coa_Gene](https://github.com/emv6/Coagulase_Negative/blob/main/Output_coa_gene.sh)

Convert the *coa* gene matches identified on the reverse strand to the reverse complement using seqtk \
`module load seqtk/1.4-GCC-11.3.0` \
`seqtk seq -r samtoolscoord_negative.fa > samtoolscoord_negative_reversecomp.fa` \
`cat samtoolscoord_negative_reversecomp.fa samtoolscoord_positive.fa > coa_sequences.fa` 

[Translate](https://www.bioinformatics.org/sms2/translate.html) *coa* sequences to protein sequences







