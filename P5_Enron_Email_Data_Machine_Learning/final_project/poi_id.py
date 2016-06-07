#!/usr/bin/python
# coding=utf-8

import sys
import pickle

from data_exploration import exploreData
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


# Data exploration
# exploreData(data_dict)


# Feature engineering
# TODO: select features, create features
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
# features_list = ['poi', 'salary', 'bonus']

features_list = ['poi','salary', 'deferral_payments', 'total_payments',
'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
'exercised_stock_options', 'long_term_incentive', 'restricted_stock']

# TODO: create def to return top x features (e.g kbest)
# TODO: create new feature(s), rerun feature section (e.g kbest)
# TODO: update features_list and my_dataset
# Store to my_dataset for easy export below.
my_dataset = data_dict

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


def test_kbest(features,labels,features_list):

    from sklearn.feature_selection import SelectKBest

    x = 0

    kbest = SelectKBest(k=5)
    kbestrans = kbest.fit_transform(features,labels)

    for f in features_list:
        if x > 0:
            print(f,'KBEST',kbest.scores_[x-1])
        x = x + 1

    return kbest

# Just a test
test_kbest(features, labels, features_list)
from sklearn.feature_selection import SelectKBest
kbest = SelectKBest(k=5)  # retain only the top 5 features with the best score
kbestrans = kbest.fit_transform(features, labels)  # fit and transform the data
indices = kbest.get_support(True)  # get the indices of the features_list which were kept


print kbestrans.shape
print kbest.scores_[0]
print kbestrans[0]
print indices


# Task 4: Try a variety of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
# from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()

# Task 5: Tune your classifier to achieve better than .3 precision and recall 
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info: 
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.

# dump_classifier_and_data(clf, my_dataset, features_list)