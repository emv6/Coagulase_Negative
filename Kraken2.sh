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
