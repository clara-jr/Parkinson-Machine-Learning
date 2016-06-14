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

def lasso(filename, x_train_orig, x_devel_orig, x_test_orig, lab_train_orig, lab_devel_orig, lab_test_orig):

    # Normalize the data
    scaler_data = preprocessing.StandardScaler().fit(x_train_orig.toarray())
    x_train = scaler_data.transform(x_train_orig.toarray())
    x_devel = scaler_data.transform(x_devel_orig.toarray())
    x_test = scaler_data.transform(x_test_orig.toarray())

    scaler_lab = preprocessing.StandardScaler().fit(lab_train_orig)
    lab_train = scaler_lab.transform(lab_train_orig)
    lab_devel = scaler_lab.transform(lab_devel_orig)
    lab_test = scaler_lab.transform(lab_test_orig)

    # Elastic Net

    clf = ElasticNet(alpha = 0.025, l1_ratio = 0.7)
    clf.fit (x_train, lab_train)
    nz = (clf.coef_ != 0)

    # Se guardan los ficheros de parametros resultantes
    dump_svmlight_file(x_train_orig[:, nz], lab_train_orig, filename+"_elasso.train.libsvm", zero_based=False, comment=None, query_id=None)
    dump_svmlight_file(x_devel_orig[:, nz], lab_devel_orig, filename+"_elasso.devel.libsvm", zero_based=False, comment=None, query_id=None)
    dump_svmlight_file(x_test_orig[:, nz], lab_test_orig, filename+"_elasso.test.libsvm", zero_based=False, comment=None, query_id=None)

# Load the data
version = "leave_half"
version_two = "leave_half_two"
version_all = "leave_half_all"
index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

for pacient in range(len(index_sort)):
    file_train = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_leave_half.train.libsvm"
    file_devel = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_leave_half.devel.libsvm"
    file_test = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_leave_half.test.libsvm"
    filename = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_leave_half"
    x_train_orig, lab_train_orig = load_svmlight_file(file_train)
    x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)
    x_test_orig, lab_test_orig = load_svmlight_file(file_test)
    lasso(filename, x_train_orig, x_devel_orig, x_test_orig, lab_train_orig, lab_devel_orig, lab_test_orig)
for pacient in range(len(index_sort)):
    if pacient != len(index_sort)-1:
        file_train = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version_two+".train.libsvm"
        file_devel = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version_two+".devel.libsvm"
        file_test = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version_two+".test.libsvm"
        filename = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version_two
        x_train_orig, lab_train_orig = load_svmlight_file(file_train)
        x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)
        x_test_orig, lab_test_orig = load_svmlight_file(file_test)
        lasso(filename, x_train_orig, x_devel_orig, x_test_orig, lab_train_orig, lab_devel_orig, lab_test_orig)
file_train = "../data/Experiment_New_Data_"+version_all+".train.libsvm"
file_devel = "../data/Experiment_New_Data_"+version_all+".devel.libsvm"
file_test = "../data/Experiment_New_Data_"+version_all+".test.libsvm"
filename = "../data/Experiment_New_Data_"+version_all
x_train_orig, lab_train_orig = load_svmlight_file(file_train)
x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)
x_test_orig, lab_test_orig = load_svmlight_file(file_test)
lasso(filename, x_train_orig, x_devel_orig, x_test_orig, lab_train_orig, lab_devel_orig, lab_test_orig)
