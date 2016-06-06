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

def exploreData(data_dict):
    # TODO: data exploration, scatterplots, boxplots, NaN, etc

    # How many data points (people) are in the dataset?
    # For each person, how many features are available?
    # How many POIs are there in the E+F dataset? (count where data[person_name]["poi"]==1 )

    people_keys = data_dict.keys()
    feature_keys = data_dict[people_keys[0]]

    poi_count = 0
    for person in people_keys:
        poi_count += data_dict[person]["poi"]

    print 'Number of people in dataset: ', len(people_keys)
    print 'Number of features for each person: ', len(feature_keys)
    print 'Number of Persons of Interests (POIs) in dataset: ', poi_count
    print 'Number of non-POIs in dataset: ', len(people_keys) - poi_count

# Remove outliers
# TODO: remove outliers and fix NaN, null, etc