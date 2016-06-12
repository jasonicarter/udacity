#!/usr/bin/python
# coding=utf-8

import sys
import pickle

from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
from time import time


sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier


# Load the dictionary containing the dataset
print '########## Load Dataset ##########'
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    print 'data_dict of length %d loaded successfully' % len(data_dict)

# Data Exploration and Removal of Outliers
print '########## Data Exploration ##########'
# exploreData(data_dict)
# TODO: Add data_exploration.py here

# Store to my_dataset for easy export below.
my_dataset = data_dict


# Feature Selection
print '########## Feature Selection ##########'

# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive',
                 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person',
                 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']


def kbest_feature_list_selection(feats, lbls):
    # featureSelection.py - featureListSelection(old_feature_list, data_dict) returns new_feature_list, feature_names

    # Retain only the top x features with the best score then fit and transform data
    # Get the indices of the feat_list which were kept
    kbest = SelectKBest(k=10)
    kbfeatures = kbest.fit_transform(feats, lbls)
    indices = kbest.get_support(True)

    # feature_list must start with labels
    feats_list = ['poi']

    # Get actual feature names
    for index in indices:
        feats_list.append(features_list[index])
        print '%s: %f' % (features_list[index], kbest.scores_[index])

    return feats_list, kbfeatures, kbest


def build_classifier_pipeline(classifier_type):
    # featureSelection.py - classifierTest(feature_list, clf,...) return clf, etc..
    # was using kb transform data for splitting and still using it in pipeline causing very high precision and recall
    # very off target from test.py

    data = featureFormat(my_dataset, features_list, sort_keys=True)
    labels, features = targetFeatureSplit(data)

    sss = StratifiedShuffleSplit(labels, 100, test_size=0.3, random_state=42)

    # build pipeline
    kbest = SelectKBest()
    classifier = set_classifier(classifier_type)
    pipeline = Pipeline(steps=[('feature_selection', kbest), (classifier_type, classifier)])

    # Set parameters for random forest
    parameters = []
    if classifier_type == 'random_forest':
        parameters = dict(feature_selection__k=[5, 10],
                          random_forest__n_estimators=[25, 50, 75, 100],
                          random_forest__min_samples_split=[2, 3, 4, 5],
                          random_forest__criterion=['gini', 'entropy'])

    # Get best optimized parameters
    cv = GridSearchCV(pipeline, param_grid=parameters, scoring='f1', cv=sss)

    # Fit, predict and report
    t0 = time()
    cv.fit(features, labels)
    print 'Random Forest tuning: %r' % round(time() - t0, 3)

    return cv


def run_cross_val_score(classifier_type):
    import sklearn.ensemble

    clf = set_classifier(classifier_type)
    score = sklearn.cross_validation.cross_val_score(clf, kb_features, labels, scoring='f1')
    print score


def set_classifier(x):
    # switch statement Python replacement - http://stackoverflow.com/a/103081
    return {
        'random_forest': RandomForestClassifier(),
        'decision_tree': DecisionTreeClassifier(),
        'logistic_reg': LogisticRegression(),
        'gaussian_nb': GaussianNB()
    }.get(x)


# Pre-processing removal of columns for model
# Removed 'email_address' to prepare for ML algorithm

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)


# Having so many features invites problems with overfitting,
# and don’t need all 3 thousand features to capture the patterns in my dataset.
# This is a perfect use case for feature selection,
# which is supported in scikit-learn by e.g. SelectKBest(),
# which will do univariate feature selection to get the k features
# (where k is a number which I have to tell the algorithm).


# Select the best features and return new features with transform
kb_features_list, kb_features, kb = kbest_feature_list_selection(features, labels)
features_list = kb_features_list


# Cross_val_score testing to pick and test classifier then use picked clf for pipeline
# Categorical models not linear...
run_cross_val_score('decision_tree')  # [ 0.42857143  0.15384615  0.25      ]
run_cross_val_score('random_forest')  # [ 0.          0.22222222  0.28571429]
run_cross_val_score('logistic_reg')   # [ 0.          0.46153846  0.36363636]
run_cross_val_score('gaussian_nb')    # [ 0.22727273  0.25531915  0.22222222]


# Test classifiers
print '########## Test and Tune Classifiers ##########'
# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# cross_val = build_classifier_pipeline('random_forest')
# print cross_val.best_params_
# clf = cross_val.best_estimator_

# See test results
# t0 = time()
# test_classifier(clf, my_dataset, features_list, folds=100)
# print 'Random forest fitting time: %rs' % round(time() - t0, 3)

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.
# dump_classifier_and_data(clf, my_dataset, features_list)


# References kept here for now
# https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html
# http://scikit-learn.org/stable/modules/pipeline.html
# https://civisanalytics.com/blog/data-science/2015/12/17/workflows-in-python-getting-data-ready-to-build-models/
