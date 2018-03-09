#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','exercised_stock_options', 'total_stock_value', 'bonus', 'salary'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
data_dict.pop('LOCKHART EUGENE E')
### Task 3: Create new feature(s)
for user in data_dict:
    if data_dict[user]['bonus']=='NaN':
        data_dict[user]['bonus_salary_ratio'] = 'NaN'
    else:
        data_dict[user]['bonus_salary_ratio'] = float(data_dict[user]['bonus'])/float(data_dict[user]['salary'])
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing

data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

# 朴素贝叶斯
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
print '朴素贝叶斯'

# KNN算法，参数调整，GridSearchCV
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.model_selection import GridSearchCV
#parameters = {
#        'weights':['uniform', 'distance'],
#        'n_neighbors': [5,10,15]
#        }
#cls = KNeighborsClassifier()
#clf = GridSearchCV(cls, parameters)
#
##clf = KNeighborsClassifier()
#print 'KNN'


# 决策树
#from sklearn import tree
#clf = tree.DecisionTreeClassifier()
#print '决策树'

# 支持向量机
#from sklearn import svm
#clf = svm.SVC()
#print '支持向量机'

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.model_selection import StratifiedShuffleSplit
cv = StratifiedShuffleSplit(n_splits=1000, test_size=0.3, random_state = 42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0
for train_idx, test_idx in cv.split(features, labels):
    features_train = []
    features_test = []
    labels_train = []
    labels_test = []
    for ii in train_idx:
        features_train.append(features[ii])
        labels_train.append(labels[ii])
    for jj in test_idx:
        features_test.append(features[jj])
        labels_test.append(labels[jj])
    
#     特征缩放
#    from sklearn.preprocessing import StandardScaler
#    scaler = StandardScaler()
#    scaler.fit(features_train)
#    features_train_transform = scaler.transform(features_train)
#    features_test_transform = scaler.transform(features_test) 
#
#    clf.fit(features_train_transform,labels_train)
#    predictions = clf.predict(features_test_transform)
    
#    非特征缩放    
    clf.fit(features_train, labels_train)
    predictions = clf.predict(features_test)
    
    for prediction, truth in zip(predictions, labels_test):
        if prediction == 0 and truth == 0:
            true_negatives += 1
        elif prediction == 0 and truth == 1:
            false_negatives += 1
        elif prediction == 1 and truth == 0:
            false_positives += 1
        elif prediction == 1 and truth == 1:
            true_positives += 1
        else:
            print "Warning: Found a predicted label not == 0 or 1."
            print "All predictions should take value 0 or 1."
            print "Evaluating performance for processed predictions:"
            break
            
precision = 1.0*true_positives/(true_positives+false_positives)
recall = 1.0*true_positives/(true_positives+false_negatives)
print 'precision：', precision
print 'recall：', recall

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)