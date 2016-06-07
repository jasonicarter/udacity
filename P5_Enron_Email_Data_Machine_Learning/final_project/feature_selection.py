#!/usr/bin/python
# coding=utf-8


# Feature selection
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".


def featureListSelection():
    # featureSelection.py - featureListSelection(old_feature_list, data_dict) returns new_feature_list, feature_names
    print 'return features_list, feature_names'


def classifierTest(type_of_classifier):
    # featureSelection.py - classifierTest(feature_list, clf,...) return clf, etc..
    # some pipeline stuff here
    print 'return clf'


def classifier():
    # featureSelection.py - classifier(...) return clf, etc
    print 'return clf'



# Store to my_dataset for easy export below.
my_dataset = data_dict

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

from sklearn.feature_selection import SelectKBest
kbest = SelectKBest(k=5)  # retain only the top 5 features with the best score
ktransform = kbest.fit_transform(features, labels)  # fit and transform the data
indices = kbest.get_support(True)  # get the indices of the features_list which were kept

print ktransform.shape
print ktransform[0]

# Table this maybe with actual score values
f_list = ['poi']
for index in indices:
    f_list.append(features_list[index])
    print '%s: %f' % (features_list[index], kbest.scores_[index])

features_list = f_list
features = ktransform