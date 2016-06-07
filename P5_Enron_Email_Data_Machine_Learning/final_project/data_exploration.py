#!/usr/bin/python
# coding=utf-8


# financial features: ['salary', 'deferral_payments', 'total_payments', 'loan_advances',
# 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
# 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
# (all units are in US dollars)
#
# email features: ['to_messages', 'email_address', 'from_poi_to_this_person',
# 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']
# (units are generally number of emails messages; notable exception is ‘email_address’,
# which is a text string)
#
# POI label: [‘poi’] (boolean, represented as integer)

import sys
sys.path.append("../tools/")
from feature_format import featureFormat


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


def fill_nan_values(data_dict):
    # Update NaN values with 0 except for email address
    people_keys = data_dict.keys()
    feature_keys = data_dict[people_keys[0]]
    for person in people_keys:
        for feature in feature_keys:
            if feature != 'email_address' and \
                data_dict[person][feature] == 'NaN':
                data_dict[person][feature] = 0


# TODO: break up function
def exploreData(data_dict):
    print '### DATA EXPLORATION ###'
    people_keys = data_dict.keys()
    feature_keys = data_dict[people_keys[0]]

    poi_count = 0
    poi_keys = []
    for person in people_keys:
        if data_dict[person]["poi"]:
            poi_count += 1
            poi_keys.append(person)

    # TODO: move into fill_nan_values and return (or print)
    # Get list of NaN values and replace them
    nan_features = {}
    for feature in feature_keys:
        nan_features[feature] = 0
    for person in people_keys:
        for feature in feature_keys:
            if data_dict[person][feature] == 'NaN':
                nan_features[feature] += 1

    # POI with missing or no to/from email information
    poi_missing_emails = []
    for poi in poi_keys:
        if (data_dict[poi]['to_messages'] == 'NaN' and
                    data_dict[poi]['from_messages'] == 'NaN') or \
            (data_dict[poi]['to_messages'] == 0 and
                     data_dict[poi]['from_messages'] == 0):
            poi_missing_emails.append(poi)

    # Top 3 POI payments and stock value
    # Top 3 non-POI payments and stock value

    # May have to fix up total_payments
    # print data_dict['BELFER ROBERT']['total_payments']
    # Look for users with all NaN values
    # Look for 'weird' user names

    # TODO: calculate percentage allocation of classes poi/all

    print 'Number of people in dataset: %d' % len(people_keys)
    print 'Number of features for each person: %d' % len(feature_keys)
    print 'Number of Persons of Interests (POIs) in dataset: %d out of 34 total POIs' % poi_count
    print 'Number of non-POIs in dataset: %d' % (len(people_keys) - poi_count)
    print nan_features
    print 'POIs with zero or missing to/from email messages in dataset: %d' % len(poi_missing_emails)
    print poi_missing_emails

    print '### REMOVE OUTLIERS ###'
    # Update NaN values
    fill_nan_values(data_dict)  # having nan values messed up numeric comparisons like > < ==

    # outlier at 26m in salary -> 'total
    scatter_plot(data_dict, 'salary', 'bonus')
    # remove outlier 'total'
    print(data_dict['TOTAL'])
    data_dict.pop('TOTAL')
    scatter_plot(data_dict, 'salary', 'bonus')

    # 4 outliers in scatter plot to investigate
    # Makes over 5mil in bonus
    bonus_bonanza = []
    people_keys = data_dict.keys()  # Update after removal of people
    for person in people_keys:
        if data_dict[person]["bonus"] > 5000000 and \
                data_dict[person]["salary"] > 1000000:
            bonus_bonanza.append(person)

    print 'Bonus Bonanza: \n', bonus_bonanza  # ['LAY KENNETH L', 'SKILLING JEFFREY K']

