#!/usr/bin/python
# coding=utf-8

import sys
import pickle
import sklearn

from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

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
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
                 'exercised_stock_options', 'long_term_incentive', 'restricted_stock']


def featureListSelection(feats, lbls):
    # featureSelection.py - featureListSelection(old_feature_list, data_dict) returns new_feature_list, feature_names

    # Retain only the top 5 features with the best score, fit and transform data
    # Get the indices of the feat_list which were kept
    kbest = SelectKBest(k=5)
    ktransform = kbest.fit_transform(feats, lbls)
    indices = kbest.get_support(True)

    # feature_list must start with labels
    feats_list = ['poi']

    # Get actual feature names
    for index in indices:
        feats_list.append(features_list[index])
        print '%s: %f' % (features_list[index], kbest.scores_[index])

    return feats_list, ktransform, kbest


def buildClassifierPipeline(classifier_type):
    # featureSelection.py - classifierTest(feature_list, clf,...) return clf, etc..

    # TODO: GridSearchCV

    # build switch statement
    classifier = setClassifier(classifier_type)
    return Pipeline(steps=[('kBest', kb), (classifier_type, classifier)])


def setClassifier(x):
    # switch statement Python replacement - http://stackoverflow.com/a/103081
    return {
        'random_forest': RandomForestClassifier(n_estimators=1, bootstrap=False),
        'decision_tree': RandomForestClassifier(n_estimators=10, bootstrap=False),
    }.get(x)


# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)


# Select the best features and return new features with transform
f_list, kb_transform, kb = featureListSelection(features, labels)
features_list = f_list


# Test classifiers
print '########## Test and Tune Classifiers ##########'
# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
clf = buildClassifierPipeline('random_forest')

# TODO: test classifier pipeline before using test.py - use the gridsearchcv from katie

#test_classifier(clf, my_dataset, features_list, folds=100)


# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.
# dump_classifier_and_data(clf, my_dataset, features_list)


# References kept here for now
# https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html
# http://scikit-learn.org/stable/modules/pipeline.html
