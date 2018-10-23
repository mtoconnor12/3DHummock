#!/usr/bin/env bash

myApp="python matk_ats.py"
echo ${myApp} > out.log
$myApp >>out.log

PBS=#!/bin/bash\n\
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
module load matk\n\
$myApp
