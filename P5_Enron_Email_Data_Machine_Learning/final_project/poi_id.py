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
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.preprocessing import MinMaxScaler
from time import time

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier


# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
# Removed 'email_address' (string) to prepare for ML algorithm
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive',
                 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person',
                 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']


def scatter_plot(data_dict, x_feature, y_feature):
    features = ['poi', x_feature, y_feature]
    data = featureFormat(data_dict, features)

    import matplotlib.pyplot as plt
    for point in data:
        x = point[1]
        y = point[2]
        if point[0]:
            plt.scatter(x, y, color="r", marker="*")
        else:
            plt.scatter(x, y, color='b', marker=".")
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    plt.show()


def fill_nan_values():
    # Update NaN values with 0 except for email address
    people_keys = data_dict.keys()
    feature_keys = data_dict[people_keys[0]]
    nan_features = {}
    # Get list of NaN values and replace them
    for feature in feature_keys:
        nan_features[feature] = 0
    for person in people_keys:
        for feature in feature_keys:
            if feature != 'email_address' and \
                data_dict[person][feature] == 'NaN':
                data_dict[person][feature] = 0
                nan_features[feature] += 1

    return nan_features


def poi_missing_email_info():
    # POI with missing or no to/from email information
    poi_count = 0
    poi_keys = []
    for person in data_dict.keys():
        if data_dict[person]["poi"]:
            poi_count += 1
            poi_keys.append(person)

    poi_missing_emails = []
    for poi in poi_keys:
        if (data_dict[poi]['to_messages'] == 'NaN' and data_dict[poi]['from_messages'] == 'NaN') or \
            (data_dict[poi]['to_messages'] == 0 and data_dict[poi]['from_messages'] == 0):
            poi_missing_emails.append(poi)

    return poi_count, poi_missing_emails


def salary_bonus_bonanza():
    # 4 more outliers in scatter plot to investigate
    # Makes over 5M in bonus
    bonanza = []
    people_keys = data_dict.keys()
    for person in people_keys:
        if data_dict[person]["bonus"] > 5000000 or data_dict[person]["salary"] > 1000000:
            bonanza.append(person)

    return bonanza


def people_with_all_nan():
    people_keys = data_dict.keys()
    feature_keys = data_dict[people_keys[0]]

    nan_people = []
    for person in people_keys:
        existing_value = 0
        for feature in feature_keys:
            if data_dict[person][feature] != 'NaN':
                existing_value += 1
        if not existing_value:
            nan_people.append(person)

    return nan_people


# TODO: need to review and create new features
def create_new_features():
    # https: // github.com / grace - pehl / enron / blob / master / Project / poi_id.py
    # Give emails to/from POIs as a proportion of total emails
    for person in data_dict.keys():
        to_poi = float(data_dict[person]['from_this_person_to_poi'])
        to_all = float(data_dict[person]['from_messages'])
        if to_all > 0:
            data_dict[person]['fraction_to_poi'] = to_poi / to_all
        else:
            data_dict[person]['fraction_to_poi'] = 0
        from_poi = float(data_dict[person]['from_poi_to_this_person'])
        from_all = float(data_dict[person]['to_messages'])
        if from_all > 0:
            data_dict[person]['fraction_from_poi'] = from_poi / from_all
        else:
            data_dict[person]['fraction_from_poi'] = 0

    # Add new feature to features_list
    features_list.extend(['fraction_to_poi', 'fraction_from_poi'])


# TODO: break up function
def explore_data():

    # Top 3 POI payments and stock value
    # Top 3 non-POI payments and stock value

    # May have to fix up total_payments
    # Look for users with all NaN values
    # Look for 'weird' user names

    people_keys = data_dict.keys()
    feature_keys = data_dict[people_keys[0]]
    poi_cnt, poi_missing_emails = poi_missing_email_info()

    print 'Number of people in dataset: %d' % len(people_keys)
    print 'Number of features for each person: %d' % len(feature_keys)
    print 'Number of Persons of Interests (POIs) in dataset: %d out of 34 total POIs' % poi_cnt
    print 'Number of non-POIs in dataset: %d' % (len(people_keys) - poi_cnt)
    print 'POIs with zero or missing to/from email messages in dataset: %d' % len(poi_missing_emails)
    print poi_missing_emails

    print '########## Removing Outliers ##########'
    # Update nan values in features, not good for numeric comparisons like > < ==
    features_with_nan = fill_nan_values()
    people_with_nan = people_with_all_nan()
    print 'Updating NaN values in features'
    print features_with_nan
    print 'People with all NaN values'
    print people_with_nan

    # Outlier at 26M in salary -> 'total
    # scatter_plot(data_dict, 'salary', 'bonus')
    # Remove outlier 'total'
    print(data_dict['TOTAL'])

    #TODO: look for other "bed" people person

    # Update dataset and re-plot
    data_dict.pop('TOTAL')
    # scatter_plot(data_dict, 'salary', 'bonus')

    high_salary_bonus = salary_bonus_bonanza()
    print 'Salary Bonus Bonanza (1M+ and 5M+): \n', high_salary_bonus

    # Create new features
    print '########## Create Features ##########'
    create_new_features()


def build_classifier_pipeline(classifier_type):
    # TODO: in general - add def comments to all
    # was using kb transform data for splitting and still using it in pipeline causing very high precision and recall
    # very off target from test.py

    data = featureFormat(my_dataset, features_list, sort_keys=True)
    labels, features = targetFeatureSplit(data)

    sss = StratifiedShuffleSplit(labels, 100, test_size=0.4, random_state=42)

    # Build pipeline
    kbest = SelectKBest()
    scaler = MinMaxScaler()
    classifier = set_classifier(classifier_type)
    pipeline = Pipeline(steps=[('minmax_scaler', scaler), ('feature_selection', kbest), (classifier_type, classifier)])

    # Set parameters for random forest
    parameters = []
    if classifier_type == 'random_forest':
        parameters = dict(feature_selection__k=range(2, 10),
                          random_forest__n_estimators=[25, 50, 100],
                          random_forest__min_samples_split=[2, 3, 4],
                          random_forest__criterion=['gini', 'entropy'])
    if classifier_type == 'logistic_reg':
        parameters = dict(feature_selection__k=range(2, 10),
                          logistic_reg__class_weight=['balanced'],
                          logistic_reg__solver=['liblinear'],
                          logistic_reg__C=range(1, 5))

    # Get optimized parameters for F1-scoring metrics
    cv = GridSearchCV(pipeline, param_grid=parameters, scoring='f1', cv=sss)
    t0 = time()
    cv.fit(features, labels)
    print 'Classifier tuning: %r' % round(time() - t0, 3)

    return cv


def set_classifier(x):
    # switch statement Python replacement - http://stackoverflow.com/a/103081
    return {
        'random_forest': RandomForestClassifier(),
        'decision_tree': DecisionTreeClassifier(),
        'logistic_reg': LogisticRegression(),
        'gaussian_nb': GaussianNB()
    }.get(x)


# Load the dictionary containing the dataset
print '########## Load Dataset ##########'
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    print 'data_dict of length %d loaded successfully' % len(data_dict)


# Data Exploration and removal of outliers
print '########## Data Exploration ##########'
explore_data()
my_dataset = data_dict


# Feature selection
print '########## Feature Selection ##########'

# Having so many features invites problems with overfitting,
# and don’t need all 3 thousand features to capture the patterns in my dataset.
# This is a perfect use case for feature selection,
# which is supported in scikit-learn by e.g. SelectKBest(),
# which will do univariate feature selection to get the k features
# (where k is a number which I have to tell the algorithm).

# SelectKBest, MinMaxScaling performed as part of classifier pipeline


# Test classifiers
print '########## Test and Tune Classifiers ##########'
# Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

cross_val = build_classifier_pipeline('logistic_reg')
print cross_val.best_params_
print cross_val.best_score_
clf = cross_val.best_estimator_

# Validate model precision, recall and F1-score
test_classifier(clf, my_dataset, features_list, folds=100)
# {'logistic_reg__solver': 'liblinear', 'feature_selection__k': 7, 'logistic_reg__C': 4, 'logistic_reg__class_weight': 'balanced'}


# Dump classifier, dataset and features_list
print '########## Dump Classifiers, dataset and features_list ##########'
# Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.
dump_classifier_and_data(clf, my_dataset, features_list)


# References
print '########## References ##########'
print 'https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/ \n' \
        'http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html' \
        'http://scikit-learn.org/stable/modules/pipeline.html \n' \
        'https://civisanalytics.com/blog/data-science/2015/12/17/workflows-in-python-getting-data-ready-to-build-models/'
