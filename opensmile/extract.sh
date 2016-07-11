#!/bin/bash

# path to your wav directory (wav files)
wav_dir=wavs
wav_file=${1}

# path to your feature directory (arff files)
feat_dir=features
feat_file=${2}

class=${3}

# openSmile configuration file
# fich_conf=IS13_ComParE_lsvm.conf
fich_conf=IS13_ComParE.conf

openSMILE-2.2rc1/bin/linux_x64_standalone_static/SMILExtract -C $fich_conf -I $wav_dir/$wav_file -O $feat_dir/$feat_file -class $class
