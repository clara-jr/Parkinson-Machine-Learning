#!/bin/sh
rm pruebas.dep
#set -x


# path to your feature directory (libsvm files)
feat_dir=../data

# directory where svr models will be stored
model_dir=./models/train_devel
mkdir -p $model_dir

# directory where evaluation results will be stored
eval_dir=./eval/train_devel
mkdir -p $eval_dir

# feature file basename
feat_name=ComParE2015_Parkinson_mfc18_elasso_f20

# path to Weka's jar file
#weka_jar=../../../weka-3-7-11/weka.jar
weka_jar=/autofs/home/gth/apps/weka-3-7-12/weka.jar
#test -f $weka_jar || exit -1

if [ ! -f "$weka_jar" ]; then
  echo "Weka could not be found in $weka_jar! Aborting"
  exit 1
fi

# memory to allocate for the JVM
jvm_mem=4096m
#-Xmx$jvm_mem

# svr complexity constant
I=$1
test -z "$I" && I=100

#epsilon-intensive loss
S=$2
test -z "$S" && S=1

lab=6375

train_libsvm=$feat_dir/$feat_name.train.libsvm
devel_libsvm=$feat_dir/$feat_name.devel.libsvm
test_libsvm=$feat_dir/$feat_name.test.libsvm

# model file name
svr_model_name=$model_dir/$feat_name.train.RandomForest.I$I.S$S.model

# train svr using Weka's SMOreg, using FilteredClassifier wrapper to ignore first attribute (instance name)
#if [ ! -f "$svr_model_name" ]; then
     echo "training model" >> pruebas.dep
     java -Xmx$jvm_mem -classpath $weka_jar weka.classifiers.meta.FilteredClassifier -v -o -no-cv -c last -t "$train_libsvm" -d "$svr_model_name" -F "weka.filters.unsupervised.attribute.Remove -R 1" -W weka.classifiers.trees.RandomForest -- -I $I -K 0 -S $S || exit 1
#fi

echo "finished train model" >> pruebas.dep

# evaluate svr and write predictions
pred_file=$eval_dir/$feat_name.RandomForest.I$I.S$S.pred
#if [ ! -s "$pred_file" ]; then
    java -Xmx$jvm_mem -classpath $weka_jar weka.classifiers.meta.FilteredClassifier -o -c last -l "$svr_model_name" -T "$devel_libsvm" -p 0 -distribution > "$pred_file" || exit 1
#fi

echo "finished evaluate svr and write predictions" >> pruebas.dep

ref_libsvm=$feat_dir/$feat_name.devel.libsvm
if [ -f "$ref_libsvm" ]; then
    echo "Found reference libsvm: $ref_libsvm" >> pruebas.dep
    # calculate classification scores
    result_file=$eval_dir/`basename $pred_file .pred`.result
#    if [ ! -f $result_file ]; then
        perl score_reg4.pl $ref_libsvm $pred_file $lab | tee $result_file >> pruebas.dep
#    else
#        cat $result_file
#    fi
fi

tail -2 $result_file
echo "Finish" >> pruebas.dep
exit 0
