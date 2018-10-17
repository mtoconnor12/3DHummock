#!/usr/bin/env bash

NUMBERS=$(seq 1 2)
echo ${NUMBERS}
for NUM in ${NUMBERS}

do
   job_name=sim_${NUM}
   file_name=run${NUM}
   dir_name="${file_name}dir"
   echo "Submitting Job: ${NAME}"
   mkdir ${dir_name}
   cd ${dir_name}

   myApp="ats --xml_file=../${file_name}.xml"
   echo ${myApp}

   PBS="#!/bin/bash\n\
   #PBS -q batch\n\
   #PBS -M oconnormt@ornl.gov\n\
   #PBS -A ccsi\n\
   #PBS -W group_list=cades-ccsi\n\
   #PBS -N ${job_name}\n\
   #PBS -l nodes=1:ppn=1\n\
   #PBS -l walltime=24:00:00\n\
   #PBS -o out.${job_name}\n\
   #PBS -e error.${NAME}\n\
   
   cd \$PBS_O_WORKDIR\n\
   module load ats/0.88/Debug\n\
   $myApp"

   echo -e ${PBS} | qsub
   sleep 0.5
   echo "Done."
   cd ..
done
