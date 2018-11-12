How to run these runs from scratch:

1) Build a template input .xml file
2) Go into matk_ats.py or some variant and edit the filenames of the parameters you wish to vary through simulation
***NOTE: If the parameter you wish to vary is a FILENAME (i.e. a mesh file or a checkpoint file), you'll want to put them all in one folder, 
append a suffix to the filename that identifies the simulation, and point matk_ats.py to that file within the folder.
3) Edit job_submission_script.sh to point to the proper matk_ats.py script
4) qsub job_submission_script.sh
***to check status: qstat -u oconnormt
5) When it errors, run Rename_Last_Checkpoint_File.sh to pull the last checkpoint file from each run directory into one single directory that
new simulations will point to
6) To figure out where the runs errored, run ReadLastTime.sh
