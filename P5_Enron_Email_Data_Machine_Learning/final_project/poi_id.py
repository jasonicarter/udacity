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
# Removed 'Other' as this this quite ambiguous in nature
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                 'expenses', 'exercised_stock_options', 'long_term_incentive',
                 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person',
                 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']


########################################################################################################################
# Function definition starts here...
########################################################################################################################


def scatter_plot(x_feature, y_feature):
    # Create scatter plot, save to local path
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
    pic = x_feature + y_feature + '.png'
    plt.savefig(pic, transparent=True)
    # plt.show()


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
    # Find total count and values of POI with missing or no to/from email information
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
    # Identify salary or bonus outliers
    bonanza = []
    people_keys = data_dict.keys()
    for person in people_keys:
        if data_dict[person]["bonus"] > 5000000 or data_dict[person]["salary"] > 1000000:
            bonanza.append(person)

    return bonanza


def create_new_features():
    # Create new features for possible use in feature selection
    people_keys = data_dict.keys()

    for person in people_keys:
        to_poi = float(data_dict[person]['from_this_person_to_poi'])
        from_poi = float(data_dict[person]['from_poi_to_this_person'])
        to_msg_total = float(data_dict[person]['to_messages'])
        from_msg_total = float(data_dict[person]['from_messages'])

        if from_msg_total > 0:
            data_dict[person]['to_poi_fraction'] = to_poi / from_msg_total
        else:
            data_dict[person]['to_poi_fraction'] = 0

        if to_msg_total > 0:
            data_dict[person]['from_poi_fraction'] = from_poi / to_msg_total
        else:
            data_dict[person]['from_poi_fraction'] = 0

        # fraction of your salary represented by your bonus (or something like that)
        person_salary = float(data_dict[person]['salary'])
        person_bonus = float(data_dict[person]['bonus'])
        if person_salary > 0 and person_bonus > 0:
            data_dict[person]['salary_bonus_fraction'] = data_dict[person]['salary'] / data_dict[person]['bonus']
        else:
            data_dict[person]['salary_bonus_fraction'] = 0

    # Add new feature to features_list
    features_list.extend(['to_poi_fraction', 'from_poi_fraction', 'salary_bonus_fraction'])


def explore_data():
    # main data exploration function
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
    print 'Updating NaN values in features'
    print features_with_nan

    # Outlier at 26M in salary -> 'total
    # scatter_plot('salary', 'bonus')
    # Remove outlier 'total'
    print 'Scatter plot shows large outlier at 26M in salary'
    print 'Outlier is "Total" value and should be removed'

    # Investigate other high salary or bonuses for outliers
    high_salary_bonus = salary_bonus_bonanza()
    print 'Salary Bonus Bonanza (1M+ and 5M+): \n', high_salary_bonus

    # Only 146 values, can visually review names
    print 'Look for other "odd" values to remove'
    # print people_keys
    print 'Found name: "THE TRAVEL AGENCY IN THE PARK" '

    # Remove outlier and odd person value
    print 'Removing two values: Total, The Travel Agency In The Park'
    data_dict.pop('TOTAL')
    data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
    # scatter_plot('salary', 'bonus')

    # Create new features
    print '\n'
    print '########## Create Features ##########'
    create_new_features()
    print 'Updated features_list: \n', features_list


def build_classifier_pipeline(classifier_type):
    # Build pipeline and tune parameters via GridSearchCV

    data = featureFormat(my_dataset, features_list, sort_keys=True)
    labels, features = targetFeatureSplit(data)

    # Using stratified shuffle split cross validation because of the small size of the dataset
    sss = StratifiedShuffleSplit(labels, 500, test_size=0.45, random_state=42)

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
        parameters = dict(feature_selection__k=range(4, 7),
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


########################################################################################################################
# Main starts here...
########################################################################################################################


# Load the dictionary containing the dataset
print '\n'
print '########## Load Dataset ##########'
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    print 'data_dict of length %d loaded successfully' % len(data_dict)


# Data Exploration and removal of outliers
print '\n'
print '########## Data Exploration ##########'
explore_data()
my_dataset = data_dict


# Feature selection
print '\n'
print '########## Feature Selection ##########'
# Using SelectKBest() which will do uni-variate feature selection to get the k best features
# MinMaxScaling, SelectKBest performed as part of classifier pipeline

# Below used for Testing Only
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

skbest = SelectKBest()
features_new = skbest.fit_transform(X_train, y_train)
indices = skbest.get_support(True)
print 'Testing scores from SelectKBest:'
print skbest.scores_

for index in indices:
    # need to map index (training without POI) back to feature_list so +1 index
    print 'feature: %s, score: %f' % (features_list[index + 1], skbest.scores_[index])


# Test classifiers
print '\n'
print '########## Test and Tune Classifiers ##########'
# Tune your classifier to achieve better than .3 precision and recall using our testing script.
cross_val = build_classifier_pipeline('logistic_reg')
print 'Best parameters: ', cross_val.best_params_
clf = cross_val.best_estimator_

# Validate model precision, recall and F1-score
test_classifier(clf, my_dataset, features_list)


# Dump classifier, dataset and features_list
print '\n'
print '########## Dump Classifiers, dataset and features_list ##########'
# Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.
dump_classifier_and_data(clf, my_dataset, features_list)
print 'Successfully created clf, my_dataset and features_list pkl files'

# References
print '########## References ##########'
print 'https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/ \n' \
        'http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html \n' \
        'http://scikit-learn.org/stable/modules/pipeline.html \n' \
        'https://civisanalytics.com/blog/data-science/2015/12/17/workflows-in-python-getting-data-ready-to-build-models/'
