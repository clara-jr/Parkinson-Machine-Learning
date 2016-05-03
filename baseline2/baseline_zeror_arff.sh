#!/bin/sh
rm pruebas.dep
#set -x


# path to your feature directory (ARFF files)
feat_dir=../data

# directory where svr models will be stored
model_dir=./models/train_devel
mkdir -p $model_dir

# directory where evaluation results will be stored
eval_dir=./eval/train_devel
mkdir -p $eval_dir

# feature file basename
feat_name=$1
test -z "$feat_name" && feat_name=ComParE2015_Parkinson

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

lab=6375

train_arff=$feat_dir/$feat_name.train.arff
devel_arff=$feat_dir/$feat_name.devel.arff
test_arff=$feat_dir/$feat_name.test.arff

# model file name
svr_model_name=$model_dir/$feat_name.train.ZeroR.model

# train svr using Weka's SMOreg, using FilteredClassifier wrapper to ignore first attribute (instance name)
#if [ ! -f "$svr_model_name" ]; then
     echo "training model" >> pruebas.dep
     java -Xmx$jvm_mem -classpath $weka_jar weka.classifiers.meta.FilteredClassifier -v -o -no-cv -c last -t "$train_arff" -d "$svr_model_name" -F "weka.filters.unsupervised.attribute.Remove -R 1" -W  weka.classifiers.rules.ZeroR || exit 1
#fi

echo "finished train model" >> pruebas.dep

# evaluate svr and write predictions
pred_file=$eval_dir/$feat_name.ZeroR.pred
#if [ ! -s "$pred_file" ]; then
    java -Xmx$jvm_mem -classpath $weka_jar weka.classifiers.meta.FilteredClassifier -o -c last -l "$svr_model_name" -T "$devel_arff" -p 0 -distribution > "$pred_file" || exit 1
#fi

echo "finished evaluate svr and write predictions" >> pruebas.dep

ref_arff=$feat_dir/$feat_name.devel.arff
if [ -f "$ref_arff" ]; then
    echo "Found reference ARFF: $ref_arff" >> pruebas.dep
    # calculate classification scores
    result_file=$eval_dir/`basename $pred_file .pred`.result
#    if [ ! -f $result_file ]; then
        perl score_reg4.pl $ref_arff $pred_file $lab | tee $result_file >> pruebas.dep
#    else
#        cat $result_file
#    fi
fi

tail -2 $result_file
echo "Finish" >> pruebas.dep
exit 0

# test predictions
pred_test_file=$eval_dir/$feat_name.ZeroR.test.pred

java -Xmx$jvm_mem -classpath $weka_jar weka.classifiers.meta.FilteredClassifier -o -c last -l "$svr_model_name" -T "$test_arff" -p 0 -distribution > "$pred_test_file" || exit 1

echo "Normalized intra-speaker variance: $(perl score_reg5spk.pl XXX $pred_test_file XXX)"
#perl format_pred2.pl <$pred_test_file >$pred_test_file.pred2
#perl score_reg5spk.pl XXX $pred_test_file XXX

echo "finished test"
