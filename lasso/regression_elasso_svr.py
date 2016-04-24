import sys
import numpy as np

from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.linear_model import ElasticNet
from sklearn import svm
from sklearn.svm import NuSVR
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer

def lasso(filename, x_train_orig, x_devel_orig, lab_train_orig, lab_devel_orig):

    # Normalize the data
    scaler_data = preprocessing.StandardScaler().fit(x_train_orig.toarray())
    x_train = scaler_data.transform(x_train_orig.toarray())
    x_devel = scaler_data.transform(x_devel_orig.toarray())

    scaler_lab = preprocessing.StandardScaler().fit(lab_train_orig)
    lab_train = scaler_lab.transform(lab_train_orig)
    lab_devel = scaler_lab.transform(lab_devel_orig)

    # Elastic Net

    clf = ElasticNet(alpha = 0.025, l1_ratio = 0.7)
    clf.fit (x_train, lab_train)
    nz = (clf.coef_ != 0)

    # Se guardan los ficheros de parametros resultantes
    dump_svmlight_file(x_train_orig[:, nz], lab_train_orig, filename+"_elasso.train.libsvm", zero_based=False, comment=None, query_id=None)
    dump_svmlight_file(x_devel_orig[:, nz], lab_devel_orig, filename+"_elasso.devel.libsvm", zero_based=False, comment=None, query_id=None)

# Load the data
# parkinson_class = ["updrs", "hoenhyahr", "hoenhyahr_categorise"]
parkinson_class = ["updrs"]
version = "homoupdrs"
n_pacientes = 26
n_grupos = 5
train_devel = ["train", "devel"]
for i in range(len(parkinson_class)):
    file_train = "../data/Experiment_New_Data_all_"+parkinson_class[i]+"_"+version+".train.libsvm"
    file_devel = "../data/Experiment_New_Data_all_"+parkinson_class[i]+"_"+version+".devel.libsvm"
    filename = "../data/Experiment_New_Data_all_"+parkinson_class[i]+"_"+version
    x_train_orig, lab_train_orig = load_svmlight_file(file_train)
    x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)
    lasso(filename, x_train_orig, x_devel_orig, lab_train_orig, lab_devel_orig)
    for n in range(n_grupos):
        file_train = "../data/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+".train.libsvm"
        file_devel = "../data/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+".devel.libsvm"
        filename = "../data/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version
        x_train_orig, lab_train_orig = load_svmlight_file(file_train)
        x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)
        lasso(filename, x_train_orig, x_devel_orig, lab_train_orig, lab_devel_orig)
for pacient in range(n_pacientes):
    if pacient != 2:
        file_train = "../data/Experiment_New_Data_"+str(pacient)+"_leave_one.train.libsvm"
        file_devel = "../data/Experiment_New_Data_"+str(pacient)+"_leave_one.devel.libsvm"
        filename = "../data/Experiment_New_Data_"+str(pacient)+"_leave_one"
        x_train_orig, lab_train_orig = load_svmlight_file(file_train)
        x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)
        lasso(filename, x_train_orig, x_devel_orig, lab_train_orig, lab_devel_orig)
