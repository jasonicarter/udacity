# Enron Email Fraud Detection with Machine Learning
**By Jason Carter**

## Summary
The goal of this project is to determine if by using the Enron email and financial dataset, can we create a model,
a Person Of Interest (POI) identifier, which will accurately predict if someone should be a person of interest for fraud. **check this** 
Machine learning is useful in trying to accomplish this goal because of it's ability to find trends, categorize data and learn from
this information in order to apply these learnings to new datasets. 

### Dataset
The Enron dataset is a corpus of information **used correctly?** which was discovered/gathered together due to the 
investigation of massive fraud and the down fall of a company called Enron. The Enron emails and financial information 
 were stitched together by Katie Mo? **check this** from Udacity.
 
### Data Exploration
**add graphs, bullets pts, etc? they did say 1 - 2 paragraphs each**
When exploring the data, there were a number of outliers, some were not relevant while others were. In order to
determine exactly what to do with them more investigation was required. One outlier which was removed from the 
dataset was only representing the total values and not an actual datapoint, while another outlier was kept 
because although it was an outlier, it was very representative of the data and to our overall goal for the project.


## Feature Selection & Engineering
What features did you end up using in your POI identifier, and what selection process did you use to pick them?
Did you have to do any scaling? Why or why not? As part of the assignment,
[relevant rubric items: “create new features”, “properly scale features”, “intelligently select feature”]
Both feature selection and engineering were performed and tested in creating the final model. 
The final features utilized in the model are: 

[salary, total_payments, bonus, score: 28.672077', total_stock_value,
exercised_stock_options, shared_receipt_with_poi, to_poi_fraction]

These features were used with the application of scaling **add in here**

### Feature Selection
used scaling, wasn't planning too (got rid of outliers) 
In your feature selection step, if you used an algorithm like a decision tree,
please also give the feature importances of the features that you use,
and if you used an automated feature selection function like SelectKBest,
please report the feature scores and reasons for your choice of parameter values.

### Feature Engineering
Three features were engineered for testing of the model. Only one was determined of substantially useful enough for 
during tuning. The engineered features are:

['to_poi_fraction', 'from_poi_fraction', 'salary_bonus_fraction']

**why these features above?**

Utilizing SelectKBest, the top 7 features were selected via GridSearchCV. Below is a table of features and their scores:

feature: salary, score: 14.837246
feature: total_payments, score: 8.376996
feature: bonus, score: 28.672077
feature: deferred_income, score: 8.064642
feature: total_stock_value, score: 10.005174
feature: exercised_stock_options, score: 9.184393
feature: long_term_incentive, score: 7.967361
feature: restricted_stock, score: 7.449035
feature: shared_receipt_with_poi, score: 9.683072
feature: to_poi_fraction, score: 14.572074


## ML Model
What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?
[relevant rubric item: “pick an algorithm”]
The POI identifier model uses the Logistic Regression algorithm as it provided the best validation results. 
The other main algorithms used were Decision Tree, Random Forest and GaussianNB, all of which performed adequately in one 
aspect or another. For example, Random Forest provided the best accuracy score but not the best Precision and Recall score.
**add a little more**

### Tuning
Tuning the parameters of algorithm is simply the process of changing, testing and updating the parameters in order to get the
right mix or settings where once completed, the parameters are optimized to produce the best results. Most ML algorithms have parameters 
and in some cases there are defaulted values, so it's no always necessary to "tune" an algorithm but in a lot of cases it is. 
If you do tune your algorithm but not very well, you could end up with a model that seems correct but is actually providing false data.
For example, I had an issue where my accuracy score was very high during tuning but in validation the precision and recall were less than 0.1
I eventually realized that I was using "accuracy score" as the benchmark for my tuning but my validation tests were using the F1-score

In the case of my final model, I used the GridSearchCV function to determine the optimized parameters. Given a set of parameters, 
this function evaluates (fit, transforms) all of the possible combinations and scores, then returns a classifier, that provides the best score.

The parameters below show my Pipeline and their parameters (pipeline: MinMax_Scaling, SelectKBest, Logistic Regression)

>Pipeline(steps=[
>>      ('minmax_scaler', MinMaxScaler(copy=True, feature_range=(0, 1))), 
>       ('feature_selection', SelectKBest(k=6, score_func=<function f_classif at 0x102c00d70>)), 
>       ('logistic_reg', LogisticRegression(C=3, class_weight='balanced', dual=False,
>           fit_intercept=True, intercept_scaling=1, max_iter=100,
>           multi_class='ovr', n_jobs=1, penalty='l2', random_state=None,
>           solver='liblinear', tol=0.0001, verbose=0, warm_start=False))
> ])
            
### Validation
What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?
[relevant rubric item: “validation strategy”]

overfitting, using all of the data for training and testing
test.py, compared against other models

### Model Results
Give at least 2 evaluation metrics and your average performance for each of them.
Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance.
[relevant rubric item: “usage of evaluation metrics”]

1. Define precision, recall and F1-score
2. Results can be in table
3. Interpret the results to human-understandable terms (convert to %)


Accuracy: 0.76540	Precision: 0.31168	Recall: 0.62850	F1: 0.41671	F2: 0.52231
Total predictions: 15000	True positives: 1257	False positives: 2776	False negatives:  743	True negatives: 10224

Accuracy: 0.76540	Precision: 0.31168	Recall: 0.62850	F1: 0.41671	F2: 0.52231
Total predictions: 15000	True positives: 1257	False positives: 2776	False negatives:  743	True negatives: 10224

sss training changed from folds 100 to default
Accuracy: 0.76380	Precision: 0.30213	Recall: 0.58900	F1: 0.39939	F2: 0.49500
Total predictions: 15000	True positives: 1178	False positives: 2721	False negatives:  822	True negatives: 10279

sss training changed from folds 100 to 1000 (similar to validation test)
Classifier tuning: 109.27
Accuracy: 0.76260	Precision: 0.30894	Recall: 0.63100	F1: 0.41479	F2: 0.52213
Total predictions: 15000	True positives: 1262	False positives: 2823	False negatives:  738	True negatives: 10177

sss training changed from folds 1000 to 100
Classifier tuning: 13.695
Accuracy: 0.76540	Precision: 0.31168	Recall: 0.62850	F1: 0.41671	F2: 0.52231
Total predictions: 15000	True positives: 1257	False positives: 2776	False negatives:  743	True negatives: 10224