# Enron Email Fraud Detection with Machine Learning
##### By Jason Carter

## Summary
*1.Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. 
As part of your answer, give some background on the dataset and how it can be used to answer the project question. 
Were there any outliers in the data when you got it, and how did you handle those?
[relevant rubric items: “data exploration”, “outlier investigation”]*

The goal of this project is to determine if by using the Enron email and financial dataset, can we create a model,
a Person Of Interest (POI) identifier, which will accurately predict if someone should be a person of interest for fraud.
Machine learning is useful in trying to accomplish this goal because of it's ability to find trends, categorize data and learn from
this information in order to apply these learnings to new datasets. 

### Dataset
Enron was one of the largest companies in the United States. By 2002, it collapsed into bankruptcy due to widespread corporate fraud, 
and during a federal investigation the Enron corpus, emails and financial information,  which was retrieved/gathered together was released
to the public. The dataset used for this project was preprocessed and stitched together by Katie Malone from Udacity.
 
### Data Exploration
Data exploration was the first step, determining size of data set, number of features, etc. 
When exploring the data, a number of outliers were discovered, some were not relevant while others were. In order to
determine next steps, more data analysis was required. 

Extreme outliers were removed from the dataset. One was a data point representing the total values and not an actual observation,
and the other was listed as "The Travel Agency In The Park". This outlier seems to be the account of a company.
Other outliers were kept because although they were outliers, it was very representative of the data and to our overall goal for the project.
Incompleteness was also a problem with the dataset. Below is an overview of the data, missing values and interesting data points.

**Data Overview**

* Number of people in dataset: 146
* Number of features for each person: 21
* Number of Persons of Interests (POIs) in dataset: 18 out of 34 total POIs
* Number of non-POIs in dataset: 128
* POIs with zero or missing to/from email messages in dataset: 4
    * Kopper Michael J
    * Fastow Andrew S
    * Yeager F Scott
    * Hirko Joseph
    
Salary vs Bonus (before and after) dropping outliers:

![alt text](./salarybonus_w_outliers.png "Salary vs Bonus with outliers")
![alt text](./salarybonus_wo_outliers.png "Salary vs Bonus without outliers")

Salary Bonus Bonanza (Employees receiving a salary or bonus of 1M+ and 5M+, respectively):
* Lavorato John J
* Lay Kenneth L
* Belden Timothy N
* Skilling Jeffrey K
* Total ('grand total' entry in data - data point removed)
* Frevert Mark A

Incomplete data - NaN values in features:

Feature | # of NaN | | Feature | # of NaN
--- | --- | --- | --- | --- | ---
salary | 51 | - | to_messages | 60
deferral_payments | 107 | - | total_payments | 21
loan_advances | 142 | - | bonus | 64 
email_address | 0 | - | restricted_stock_deferred | 128
total_stock_value | 20 | - | shared_receipt_with_poi | 60
long_term_incentive | 80 | - | exercised_stock_options | 44
from_messages | 60 | - | other | 53
from_poi_to_this_person | 60 | - | from_this_person_to_poi | 60
poi | 0 | - | deferred_income | 97
expenses | 51 | - | restricted_stock | 36
director_fees | 129


## Feature Selection & Engineering
*2.What features did you end up using in your POI identifier, and what selection process did you use to pick them? 
Did you have to do any scaling? Why or why not? As part of the assignment, 
you should attempt to engineer your own feature that does not come ready-made in the dataset -- 
explain what feature you tried to make, and the rationale behind it. 
(You do not necessarily have to use it in the final analysis, only engineer and test it.) 
In your feature selection step, if you used an algorithm like a decision tree, 
please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, 
please report the feature scores and reasons for your choice of parameter values.
[relevant rubric items: “create new features”, “properly scale features”, “intelligently select feature”]*

Both univariate feature selection and engineering were performed and used in tested when creating the final model. 
Feature scaling was also utilized as there were a number of outliers which could screw the results (be used as a primary predictor) but 
due to the validity of the data, these points could not be removed. Although performance was tested
with and without feature scaling as a reassurance to the process, the final model does not utilized feature scaling.

### Feature Selection

Feature selection was performed by SelectKBest obtain the the best Precision and Recall scores during numerous testing. No features used were manually picked.
Train test sets were created with the use of Stratified Shuffle Split cross validation due to small size of the data and that of the POI list.
The final features utilized in the model are: 

* salary 
* bonus
* deferred_income 
* exercised_stock_options 
* total_stock_value
* to_poi_fraction score
* shared_receipt_with_poi 
* total_payments
* expenses score
* from_poi_fraction score 

### Feature Engineering
Three features were engineered for testing of the model. 

* to_poi_fraction - a fraction of the total 'to' emails that were sent to a POI 
* from_poi_fraction - a fraction of the total 'from' emails that were received from a POI
* salary_bonus_fraction - a fraction of salary to bonus money

With the project goal of identifying POIs, I believed adding two additional features which calculated the percentage/
relationship of a POI with other employees at the company via their 'to' and 'from' email interaction would have
shed insightful and useful information, allowing the algorithm to use these values as predictors.
e.g if person A sends (or receives) a large portion of their total emails to/from a POI, there may be a greater likelihood that 
person A is also a POI.

Like-wise, after discovering the large salary and bonuses of some of the POIs, I believed knowing the fraction or
multiplier between someone's salary and their bonus would help as a predictor for the algorithm.

GridSearchCV was initially used but being unable to easily identify k best features, I did a number of separate SelectKBest testing,
and viewed their precision and recall scores. With SelectKBest, the number 10 for k was decided upon after a number of performance and tuning 
which determined this to deliver the best mix of performance (timing), precision and recall.

Below is a table of features and their scores:

Feature | Score
--- | --- | ---
bonus | 38.290312
deferred_income | 19.454073
salary | 18.012912
exercised_stock_options | 14.621981
total_stock_value | 14.544973
to_poi_fraction score | 14.271175
shared_receipt_with_poi | 12.597418
total_payments | 11.007505
expenses score | 2.995212
from_poi_fraction score | 1.437558


## ML Model
*3.What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?
[relevant rubric item: “pick an algorithm”]*

The POI identifier model uses the AdaBoost and DecisionTree algorithm as it provided the best validation results. 
The other main algorithms used were Decision Tree (without AdaBoost), Random Forest and GaussianNB, and Logistic Regression 
all of which performed adequately in one aspect or another. For example, Random Forest provided the best accuracy score but had low Precision and Recall scores.


### Tuning
*4.What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?
How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- 
if this is the case for the one you picked, identify and 
briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, 
e.g. a decision tree classifier).  [relevant rubric item: “tune the algorithm”]*

Tuning the parameters of algorithm is simply the process of changing, testing and updating the parameters in order to get the
right mix or settings where once completed, the parameters are optimized to produce the best results. Most ML algorithms have parameters 
and in some cases there are defaulted values, so it's no always necessary to "tune" an algorithm but in a lot of cases it is. 
If you do tune your algorithm but not very well, you could end up with a model that seems correct but is actually providing false data.
For example, I had an issue where my accuracy score was very high during tuning (train test sets) 
but in during validation the precision and recall were less than 0.1. I eventually realized that I was using "accuracy score" as the benchmark 
for my tuning but my validation tests were using the F1-score, Precision and Recall.

In the case of my final model, I used the GridSearchCV function to determine the optimized parameters. Given a set of parameters, 
this function evaluates (fit, transforms) all of the possible combinations, then returns a classifier, that provides the best score.

Algorithm | Precision | Recall | # of Training (StratifiedShuffleSplit folds)
--- | --- | --- | ---
Random Forest | 0.41747 | 0.21750 | 100
Logistic Regression | 0.31064 | 0.60900 | 100
AdaBoost (DecisionTree) | 0.43123 | 0.40600 | 100
            
### Validation
*5.What is validation, and what’s a classic mistake you can make if you do it wrong? 
How did you validate your analysis?  [relevant rubric item: “validation strategy”]*

Validation is the process of checking your model's prediction against data that wasn't used to train your algorithm/model.
A classic mistake of overfitting occurs when you train the algorithm on all available data 
instead of splitting it into training and testing data. Overfitting causing the model to merely memorize classification 
and not 'learn' to generalize and apply this information to new datasets.

The final model used Stratified Shuffle Split cross validation iterator to randomly create multiple train test sets of data. 
This was an ideal approach given the small dataset and even smaller number of POIs within the dataset.

### Model Results
*6.Give at least 2 evaluation metrics and your average performance for each of them.
Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. 
[relevant rubric item: “usage of evaluation metrics”]*

The final model uses Precision, Recall and F1 scores to evaluate how good the model is in predicting POIs.
The raw data can be see below. Each observation is a test, and each test made 15,000 predictions.

Precision | Recall | F1 | # of Training (StratifiedShuffleSplit folds)
--- | --- | --- | --- | ---
0.50000 | 0.45000 | 0.47368 | 10
0.47458 | 0.42000 | 0.44562 | 100
0.43123 | 0.40600| 0.41823 | 1000

* *Precision is the measurement of how many selected items were identified as relevant*
* *Recall is the measurement of how many relevant were selected*

The model's precision is approx. 45% i.e from the people classified as POIs by the model, 45% of them are actual POIs.
However, the model's recall is approx. 40% i.e from the number of actual POIs in the total dataset, the model correctly identifies
40% them. It can be concluded that although the model "spreads a wide net" it will capture over 40% of actual POIs.