# This script creates the 1D column file that gets fed to test7
cur_dir=`pwd`
cd "../test1/run02_09Oct18/"
python $ATS_SRC_DIR/tools/utils/column_data.py -t 0
mv column_data.h5 ../../init/column_data_run02_09Oct18.h5
echo 'Exp1 Column h5 file successfully created'
