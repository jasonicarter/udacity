# A/B Testing (title)

## Experiment Summary
At the time of this experiment, Udacity courses currently have two options on the home page: "start free trial", and "access course materials". If the student clicks "start free trial", they will be asked to enter their credit card information, and then they will be enrolled in a free trial for the paid version of the course. After 14 days, they will automatically be charged unless they cancel first. If the student clicks "access course materials", they will be able to view the videos and take the quizzes for free, but they will not receive coaching support or a verified certificate, and they will not submit their final project for feedback.

In the experiment, Udacity tested a change where if the student clicked "start free trial", they were asked how much time they had available to devote to the course. If the student indicated 5 or more hours per week, they would be taken through the checkout process as usual. If they indicated fewer than 5 hours per week, a message would appear indicating that Udacity courses usually require a greater time commitment for successful completion, and suggesting that the student might like to access the course materials for free. At this point, the student would have the option to continue enrolling in the free trial, or access the course materials for free instead. This screenshot shows what the experiment looks like.

![alt final screenshot](/Final Project_ Experiment Screenshot.png)

The hypothesis was that this might set clearer expectations for students upfront, thus reducing the number of frustrated students who left the free trial because they didn't have enough time—without significantly reducing the number of students to continue past the free trial and eventually complete the course. If this hypothesis held true, Udacity could improve the overall student experience and improve coaches' capacity to support students who are likely to complete the course.

The unit of diversion is a cookie, although if the student enrolls in the free trial, they are tracked by user-id from that point forward. The same user-id cannot enroll in the free trial twice. For users that do not enroll, their user-id is not tracked in the experiment, even if they were signed in when they visited the course overview page.


## Experiment Design
### Metric Choice
#### Invariant Metrics
**Number of cookies**: The number of unique cookies to view the course overview page. This is a population sizing metric to be split evenly between the control and the experiment group. It should have no direct affect on the experiment.

**Number of clicks**: The number of unique users/students (unique cookies) that click on the "start free trial" button. Since this button is clicked prior to the free trial screen appearing, this event should not direct affect the experiement and is therefore used as a invariant metric.

**Click-through-probability**: The number of unique cookies to click on the "start free trail" button divided by the number of unique cookies to view the course overview page. The experience should be the same for all users and should not directly affect the experiement.

#### Evaluation Metrics
**Gross conversion**: The number of user-ids that enroll in the free trial divided by the number of unique cookies to click on the "start free trial" button. The number of enrollments can be affected by the experiment and as a result the gross conversion; therefore this will be used as an evaluation metric.

**Retention**: The number of user-ids that stayed enrolled past the 14 day free trial (made a payment) divided by the number of unique cookies that clicked on the "start free trial" button. The number of payments can be affected the experiement and retention values; therefore this will be used as an evaluation metric.

**Net conversion**: The number of user-ids to remain enrolled past the 14 day free trial (made a payment) divided by the number of unique cookies that clicked on the "start free trial" button. The number of payments can be affected by the experiment and as a result the net conversion, this will be used as an evaluation metric. 

### Measuring Standard Deviation
Evaluation Metric | Standard Deviation
--- | ---
Gross Conversion | .0202
Retention | .0549
Net Conversion | .0156

The standard deviation calculated for each sample has a size of 5000 unique cookies visiting the course overview page. Please see [Baseline Values](https://docs.google.com/spreadsheets/d/1MYNUtC47Pg8hdoCjOXaHqF-thheGpUshrFA21BAJnNc/edit#gid=0) - the standard deviations are calcuated using these baseline values.

### Sizing
#### Number of Samples vs. Power
The Bonferroni Correction was not used during the analysis phase. The number of page views required (largest sample size) to conduct this experiment is: 4,741,212

Metric | Pageviews
--- | ---
Gross Conversion | 646,450
Retention | 4,741,212
Net Conversion | 685,325

#### Duration vs. Exposure
Given the low risk and lack of sensitive data being collected, I would divert 100% of the traffic. With approx. 40,000 page views per day, the experiment would take roughly 119 days. However, this time period is too long to conduct an experiment for Udacity. Revising my previous decision, retention will no longer be used as an evaluation metric. 

New evaluation metrics are Gross Conversion and Net Conversion. The new number of page views required is 685,325 and the experiment will now require 18 days to complete. Note that if other experiments need to be conducted simutaneously, the percentage diversion can be reduced.

Metric | Duration
--- | ---
Gross Conversion | 17
Retention | 119
Net Conversion | 18


## Experiment Analysis
[Control and Experiment data](https://docs.google.com/spreadsheets/d/1Mu5u9GrybDdska-ljPXyBjTpdZIUev_6i7t4LRDfXM8/edit#gid=0) provided by Udacity and used throughout this section.
### Sanity Checks
Below is the computed 95% confidence inteval for the listed invariant metrics

Invariant Metric | Lower Bound | Upper Bound | Observed | Pass/Fail
--- | --- | --- | --- | ---
Number of Cookies | .4988 | .5012 | .5006 | Pass
Number of Clicks | .4959 | .5041 | .5005 | Pass
Click-through Probability | .0812 | .0830 | .0822 | Pass

### Result Analysis
#### Effect Size Tests
Below is the computed 95% confidence interval around the difference between the experiment and control groups. 

Evaluation Metric | Lower Bound | Upper Bound | Statisticially or Practically Significant
--- | --- | --- | ---
Gross Conversion | -0.0291 | -0.012 | Yes (statisticially and Practically)
Net Conversion | -0.0116 | .0019 | No (statistically and Practically)

#### Sign Tests
Below is the computed sign test using the day-by-day data.

Evaluation Metric | p-value | Statistically Significant
--- | --- | ---
Gross Conversion | 0.0026 | Yes
Net Conversion | 0.6776 | No

#### Summary
State whether you used the Bonferroni correction, and explain why or why not. If there are any discrepancies between the effect size hypothesis tests and the sign tests, describe the discrepancy and why you think it arose.

### Recommendation
Make a recommendation and briefly describe your reasoning.

## Follow-Up Experiment
Give a high­level description of the follow up experiment you would run, what your hypothesis would be, what metrics you would want to measure, what your unit of diversion would be, and your reasoning for these choices.
