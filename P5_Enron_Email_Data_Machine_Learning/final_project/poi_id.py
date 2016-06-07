#!/usr/bin/python
# coding=utf-8

import sys
import pickle

from data_exploration import exploreData

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Data Exploration and Removal of Outliers
# exploreData(data_dict)
# TODO: return data_dict
# my_dataset = exploreData(data_dict) returns updated data_dict

# Feature Selection
# featureSelection.py - featureListSelection(old_feature_list, data_dict) returns new_feature_list, feature_names
# featureSelection.py - classifierTest(feature_list, clf,...) return clf, etc..
# featureSelection.py - classifier(...) return clf, etc


# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
                 'exercised_stock_options', 'long_term_incentive', 'restricted_stock']

# Test classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html


# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

from time import time
from sklearn import tree
from sklearn.metrics import accuracy_score

t0 = time()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

t0 = time()
pred = clf.predict(features_test)
print "predicting time:", round(time()-t0, 3), "s"
print accuracy_score(pred, labels_test)

# training time: 0.004 s
# predicting time: 0.0 s
# 0.863636363636


import sklearn.pipeline

select = sklearn.feature_selection.SelectKBest(k=5)
dt = tree.DecisionTreeClassifier()  # sklearn.ensemble.RandomForestClassifier()

steps = [('feature_selection', select),
        ('decision_tree', dt)]

clf = sklearn.pipeline.Pipeline(steps)

# testing
test_classifier(clf, my_dataset, features_list, folds=100)


X_train, X_test, y_train, y_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# fit your pipeline on X_train and y_train
clf.fit(X_train, y_train)
# call pipeline.predict() on your X_test data to make a set of test predictions
y_prediction = clf.predict(X_test)
# test your predictions using sklearn.classification_report()
report = sklearn.metrics.classification_report(y_test, y_prediction)
# and print the report
print(report)



# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


# Use tester.py here
# TODO: 'make sure [this] poi.py [...] can run on its own. (will need to fix that up)

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.

# dump_classifier_and_data(clf, my_dataset, features_list)


# References kept here for now
# https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html
# http://scikit-learn.org/stable/modules/pipeline.html
