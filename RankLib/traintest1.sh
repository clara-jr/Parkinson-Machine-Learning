#/bin/bash
TRAIN=${10}
TEST=${11}
MODEL1=${12}
BAG=${1}
TC=${2}
ESTOP=${3}
MLS=${4}
SRATE=${5}
FRATE=${6}
TREE=${7}
LEAF=${8}
SHRINKAGE=${9}
#1	[ -bag <r> ]	Number of bags (default=300)
#2 	[ -tc <k> ]	Number of threshold candidates for tree spliting. -1 to use all feature values (default=256)
#3 	[ -estop <e> ]	Stop early when no improvement is observed on validaton data in e consecutive rounds (default=100)
#4 	[ -mls <n> ]	Min leaf support -- minimum #samples each leaf has to contain (default=1)
#5 	[ -srate <r> ]	Sub-sampling rate (default=1.0)
#6 	[ -frate <r> ]	Feature sampling rate (default=0.3)
#7 	[ -tree <t> ]	Number of trees in each bag (default=1)
#8 	[ -leaf <l> ]	Number of leaves for each tree (default=100)
#9 	[ -shrinkage <factor> ]	Shrinkage, or learning rate (default=0.1)

PREDICTED=eval/train_devel/$TEST.bag-$BAG-tc-$TC-es-$ESTOP-ml-$MLS-sr-$SRATE-fr-$FRATE-tr-$TREE-le-$LEAF-sh-$SHRINKAGE.pred
MODEL=models/train_devel/${MODEL1}.b-$BAG-tc-$TC-es-$ESTOP-ml-$MLS-sr-$SRATE-fr-$FRATE-tr-$TREE-le-$LEAF-sh-$SHRINKAGE.model
DEP=eval/train_devel/${MODEL1}.b-$BAG-tc-$TC-es-$ESTOP-ml-$MLS-sr-$SRATE-fr-$FRATE-tr-$TREE-le-$LEAF-sh-$SHRINKAGE.dep

echo PREDICTED: $PREDICTED >$DEP
java -jar bin/RankLib.jar -train $TRAIN -ranker 8 -save $MODEL -bag $BAG -tc $TC -estop $ESTOP -mls $MLS -srate $SRATE -frate $FRATE -tree $TREE -leaf $LEAF -shrinkage $SHRINKAGE >>$DEP
rm $PREDICTED
java -jar bin/RankLib.jar -load $MODEL -rank $TEST -ranker 8 -score $PREDICTED >>$DEP
sleep $[ ( $RANDOM % 5 )  + 1 ]s
echo "PREDICTED: $PREDICTED TRAIN:$TRAIN" >> eval/train_devel/results-${MODEL1}.b-$BAG-tc-$TC-es-$ESTOP-ml-$MLS-sr-$SRATE-fr-$FRATE-tr-$TREE-le-$LEAF-sh-$SHRINKAGE.dep
perl score_reg2.pl $TEST $PREDICTED 1 >> eval/train_devel/results-${MODEL1}.b-$BAG-tc-$TC-es-$ESTOP-ml-$MLS-sr-$SRATE-fr-$FRATE-tr-$TREE-le-$LEAF-sh-$SHRINKAGE.dep
