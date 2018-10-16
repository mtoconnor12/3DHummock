# This script creates the 1D column file that gets fed to test7
cur_dir=`pwd`
cd "../test1/15Oct18_AllMineralSpinup/"
python $ATS_SRC_DIR/tools/utils/column_data.py -t 0
mv column_data.h5 ../../init/column_data_15Oct18_AllMineralSpinup.h5
echo 'Exp1 Column h5 file successfully created'
