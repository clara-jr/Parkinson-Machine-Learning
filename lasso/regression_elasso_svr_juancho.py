import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy

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
from scipy import stats
from scipy.stats import pearsonr
from scipy.stats import spearmanr

#file_train = sys.argv[1]
#file_devel = sys.argv[2]
#file_pred = sys.argv[3]

# 1. Load the data
x_train_orig, lab_train_orig = load_svmlight_file("../lsvm/ComParE2015_Parkinson_mfc18_elasso_f20.train.libsvm")
##x_train_orig, lab_train_orig = load_svmlight_file(file_train)
x_devel_orig, lab_devel_orig = load_svmlight_file("../lsvm/ComParE2015_Parkinson_mfc18_elasso_f20.devel.libsvm")
##x_devel_orig, lab_devel_orig = load_svmlight_file(file_devel)

# 2. Normalize the data
scaler_data = preprocessing.StandardScaler().fit(x_train_orig.toarray())
x_train = scaler_data.transform(x_train_orig.toarray()) 
x_devel = scaler_data.transform(x_devel_orig.toarray()) 

scaler_lab = preprocessing.StandardScaler().fit(lab_train_orig)
lab_train = scaler_lab.transform(lab_train_orig) 
lab_devel = scaler_lab.transform(lab_devel_orig) 

# 3a. Elastic Net

#clf = ElasticNet(alpha = 0.025, l1_ratio = 0.7)
#clf.fit (x_train, lab_train)

#print "Coeficientes Elastic Lasso"
#print np.size(clf.coef_[clf.coef_ != 0])
#np.savetxt('coefsEN.out', clf.coef_, delimiter=',', fmt='%.2f')

#nz = (clf.coef_ != 0)
#x_train_red = x_train[:, nz]
#x_devel_red = x_devel[:, nz]

# Se guardan los ficheros de parametros resultantes
#dump_svmlight_file(x_train_orig[:, nz], lab_train_orig, "../lsvm/train.libsvm", zero_based=False, comment=None, query_id=None)
#dump_svmlight_file(x_devel_orig[:, nz], lab_devel_orig, "../lsvm/devel.libsvm", zero_based=False, comment=None, query_id=None)


# 3b. SVR

# Como ya se leen directamente el conjunto reducido de parametros, no hace falta hacer el Elastic Lasso
x_train_red = x_train
x_devel_red = x_devel

# Mejor resultado con SVR con el conjunto reducido
clf = svm.SVR(C=.3, epsilon=1, kernel='poly', degree=1, gamma = 0.01, cache_size=250007, verbose=True)


# 4. Model training

clf.fit (x_train_red, lab_train)

# 5. Predictions computation

pred = clf.predict(x_devel_red)
pred_orig = scaler_lab.inverse_transform(pred)
pred_orig[pred_orig < 0] = 1


# 6. Correlation computations

print scipy.stats.stats.pearsonr(lab_devel, pred)[0]
print scipy.stats.stats.spearmanr(lab_devel, pred)[0]
print scipy.stats.stats.pearsonr(lab_devel_orig, pred_orig)[0]
print scipy.stats.stats.spearmanr(lab_devel_orig, pred_orig)[0]


# 7. Predictions storage
file_pred = "ComParE2015_Parkinson_mfc18_elasso_f20.devel.pred"
np.savetxt(file_pred, pred_orig, delimiter=',', fmt='%.2f')


# 8. Plot labels and predictions
plt.scatter(lab_devel_orig, pred_orig, color='blue')
plt.axis([0, 100, 0, 100])
#plt.xticks(())
#plt.yticks(())
plt.show()

