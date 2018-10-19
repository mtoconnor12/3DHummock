#!/bin/bash

#PBS -q batch
#PBS -M jana@ornl.gov  ### my ornl email
#PBS -A ccsi ### project
#PBS -W group_list=cades-ccsi ### don’t change
#PBS -m be a   ### email notifications at the beginning, ending, and abort
#PBS -N Crun2R22 ### name of the job, same as the input file (doesn’t have to be)
###PBS -j oe
#PBS -l nodes=1:ppn=32 ### requested number of processors 
#PBS -l walltime=48:00:00 ### wall time (max time = 48h)

cd $PBS_O_WORKDIR

myApp="/lustre/or-hydra/cades-ccsi/ahmadjan/arctic/ats-debug/ats-0.87/install-debug/bin/ats --xml_file=../inputfiles/Crun2R22.xml"

echo $myApp > out.log
mpirun –np 4 $myApp >>out.log

qsub subjobs.pbs ### this is the command in the command prompt to run