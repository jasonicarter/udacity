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

    # build pipeline
    classifier = set_classifier(classifier_type)
    pipeline = Pipeline(steps=[('feature_selection', kb), (classifier_type, classifier)])

    # Get train test sets
    features_train, features_test, labels_train, labels_test = \
        train_test_split(kb_features, labels, test_size=0.5, random_state=42)

    # Set parameters for random forest
    parameters = []
    if classifier_type == 'random_forest':
        parameters = dict(feature_selection__k=[5, 10, 'all'],
                          random_forest__n_estimators=[25, 50, 75, 100],
                          random_forest__min_samples_split=[2, 3, 4, 5],
                          random_forest__bootstrap=[True, False],
                          random_forest__criterion=['gini', 'entropy'])

    cv = GridSearchCV(pipeline, param_grid=parameters)

    cv.fit(features_train, labels_train)
    predictions = cv.predict(features_test)
    report = classification_report(labels_test, predictions)

    return report, cv


def run_cross_val_score(classifier_type):
    import sklearn.ensemble

    clf = set_classifier(classifier_type)
    score = sklearn.cross_validation.cross_val_score(clf, kb_features, labels)
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
run_cross_val_score('decision_tree')  # [ 0.83673469  0.79166667  0.83333333]
run_cross_val_score('random_forest')  # [ 0.87755102  0.875       0.875     ]
run_cross_val_score('logistic_reg')   # [ 0.75510204  0.85416667  0.85416667]
run_cross_val_score('gaussian_nb')    # [ 0.30612245  0.27083333  0.27083333]


# Test classifiers
print '########## Test and Tune Classifiers ##########'
# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

rpt, cross_val = build_classifier_pipeline('random_forest')
print cross_val.best_params_
print rpt

# {'feature_selection__k': 10, 'random_forest__n_estimators': 50, 'random_forest__min_samples_split': 4}

# See test results
# selector = SelectKBest(k=10)
# classifier = RandomForestClassifier(n_estimators=50, min_samples_split=4)
# clf = Pipeline(steps=[('feature_selection', selector), ('random_forest', classifier)])
# test_classifier(clf, my_dataset, features_list)


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
