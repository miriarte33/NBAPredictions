**All-Stars and MVP Candidates: Analysis of Classification and
Regression Performance on NBA Statistics**

Manrique Iriarte

Professor Weiss

December 13, 2019

miriarte\@fordham.edu

*Abstract*--- NBA All-Star rosters and MVP voting has always been a
subject of debate amongst basketball fans and professional sports
analysts. Who deserved that final All-Star roster spot? Who should have
gained more consideration for the MVP award? The questions never end,
nor will they. For eons people have argued whether stats matter most, or
if contributing to the team's overall success is more important than
putting up great individual numbers; a very select few of these people
have even made great careers for themselves talking about these topics
on television. Using classification and regression methods, this study
attempts to answer those questions and evaluate how well said methods
can predict NBA All-Star rosters and MVP vote shares based only on
personal stats.

Keywords---regression, classification

Introduction
============

Every year around February, twenty-four distinguished NBA athletes are
selected by fans, media, and coaches to represent their respective teams
and conferences in the All-Star game. At the end of the season, the
media votes on who they think deserves the prestigious MVP Award. This
study will use Data Mining techniques in order to try and determine what
makes an All-Star or MVP candidate. Data was gathered from the season
beginning in 1976 thru the season ending in 2016 in order to predict
2017 MVP vote share and All-Stars. MVP vote share will be treated as a
regression problem since vote share is a continuous value between 0 and
1, whilst predicting the All-Stars will be treated as a classification
problem since there are only two possible values, 1 or 0.

Methodologies
=============

Dataset
-------

As mentioned in the introduction, the training set contains statistical
data from 1976 thru 2016 and the test set is the statistical data from
the 2016-2017 NBA season. The features included in the datasets are a
merge of the advanced and per-game statistics found in
<https://www.basketball-reference.com/>. These statistics include Win
Shares, Points Per Game, Assists Per Game, Rebounds Per Game, Box Plus
Minus, Player Efficiency Rating, etc. There are fifty-two features in
total. For detailed explanations on each of these fifty-two features,
visit the linked basketball reference website and look at the per game
and advanced statistics for any season. Hovering over the column name on
the table will give a definition of what that statistic means. There is
a 1 in the All-Star column for those who played in the All-Star game and
a 0 for those who did not. Those who were selected to an All-Star game
but didn't play because of injury, suspension, or any other reason have
a 0 in the All-Star column as well. This was done to prevent our model
from selecting more than 24 all stars. The Shares column is the MVP vote
shares, normalized between 0 and 1 as it is on the basketball reference
website.

Tools Used
----------

This project was created in Python with the help of some indispensable
third-party libraries. BeautifulSoup was used to parse the basketball
reference website in order to gather the data. Pandas was used to store
said data in a csv file and manipulate it accordingly for the various
models. Matplotlib was used to plot the ROC curve of our classification
model. Lastly, Scikit Learn was used to create, test, and evaluate the
models.

Algorithms
----------

MVP Vote Shares was the most challenging of the two to predict. Three
different algorithms were used, which will be compared in the Results
section. Decision Tree was one of those algorithms. Decision Trees ask
at every node which feature(s) to split on and at the end comes up with
a decision for the class variable based on those splits (Yiu). Multiple
Linear Regression was used as well. Multiple Linear Regression describes
the relationship between a dependent variable (the class variable, All
Star or Shares) and multiple independent variables (the features) and
expresses it using the linear equation (Chauhan). Lastly, Random Forest
was also used, which essentially creates several decision trees that
each give out a class prediction, and the class with the most votes from
all the decision trees becomes the prediction for the Random Forest
(Yiu). Random Forest, because of its robustness to noise, was extremely
useful in predicting All-Stars.

Evaluation Metrics
------------------

Metrics used to evaluate the classification model were accuracy,
precision, recall, F-measure, and AUC. Accuracy is the number of correct
predictions, which can be misleading in this case because this data set
suffers from severe class imbalance (Evaluating a Classification Model).
There are 15917 of NBA Players from 1976-2016, and only about 950 of
them were All-Stars. Therefore, if our model were to predict 0 every
single time, it would have an extremely high accuracy and still be a
terrible model, which is why the model needs good precision, recall,
F-measure, and AUC scores. Precision is evaluated as True Positive
predictions / True Positive predictions + False Positive predictions, in
other words, precision is how often a prediction is correct when a
positive value is predicted (Evaluating a Classification Model). Recall
is how often the prediction is correct when the actual value is
positive, evaluated as True Positive predictions / True Positive
predictions + False Negative predictions (Evaluating a Classification
Model). These improve the ability to evaluate models such as this
because if our model were to always predict 0, precision and recall
would both be 0 even though technically our accuracy would still be
extremely high. F-measure is 2\*(Precision\*Recall/Precision+Recall), so
it is a balance of precision and recall and much more useful than
accuracy for evaluating models on imbalanced datasets like this one
(Shung). The probability threshold was decreased to 0.43 so that our
model would predict someone was an All-Star if it believed it was 43%
probable. This was to give us a good balance between precision and
recall by making sure it only predicts 24 All-Stars, no more and no
less. Lastly, but perhaps most importantly, AUC is the area under the
ROC curve expressed as a percentage, which tells us if the model is
actually good at distinguishing between players who are All-Stars and
players who are not (Narkhede). An AUC score of 1.0 is considered
perfect, and AUC is considered one of the best ways to evaluate
classifiers on unbalanced datasets.

Mean Absolute Error, Mean Squared Error, and R2 Score were the
evaluation metrics used to evalue the regression models. Mean Absolute
Error is the sum of the distances between all of the data points and the
line that fits through the data points (Karbhari). Mean Squared Error is
the same as the Mean Absolute Error, but it is the sum of the squared
differences between the data points and the line (Karbhari). The R2
score creates a horizontal line between the data points and calculates
the Mean Squared Error of that line, which essentially evaluates to 1
--- (Error from Linear Regression Model/Simple average model)
(Karbhari).

Results
=======

All-Stars
---------

The top twenty stats in order of importance, according to our model, can
be viewed in Figure 1. Figure 2 is a list of the actual predictions and
the confusion matrix. As you can see from the confusion matrix, out of
twenty four All-Stars, we only had six false positive predictions and
six false negative predictions. In other words, our model predicted 6
people should have been All-Stars that were left out of the game in real
life. That gave us an accuracy of 97%, which is not hard to get, as
previously mentioned. A little more impressive are the precision,
recall, and F-measure scores, which are all 75%. The fact that we have
even precision and recall scores means that our model is not predicting
too many positives to achieve a higher recall but is not predicting too
little positives to achieve a higher precision. We are predicting the
same number of All-Stars as there are in real life. Figure 3 show the
ROC curve of our model, which is extremely good, as it shows that we
have achieved an AUC score of 0.9889, close to a perfect score. That is
really impressive, because it means that our model has an extremely high
true positive rate if the probability threshold is low enough. However,
lowering our threshold would have resulted in too many positive
predictions, which would make our model less precise.

The six false positive predictions were Bradley Beal, Mike Conley, CJ
McCollum, Andrew Wiggins, Karl Anthony-Towns, and Damian Lillard. Damian
Lillard, Mike Conley, and Bradley Beal in particular have been
underrated most of their careers, and it is no surprise our model
believes they should have been All-Stars. The other three, although they
are good, were probably not All-Star caliber players in 2017. Those
three players in particular highlight an important limitation of our
model that will be discussed later.

Those six were chosen in favor of Marc Gasol, Klay Thompson, Draymond
Green, DeAndre Jordan, Paul Millsap, and Carmelo Anthony. Carmelo
Anthony only made the All-Star game because another player, Kevin Love,
was injured. However, the model did not predict Kevin Love either so
nevertheless, that is a legitimate false negative. It's hard to argue
that Marc Gasol, Klay Thompson, and Draymond Green did not deserve to be
All-Stars that year, so our model was blatantly wrong with those three.
DeAndre Jordan didn't have All-Star stats, which is why we can't expect
our model to predict him, but he was well known among fans as being a
walking highlight reel with his dunks and overall athleticism. Millsap
had a good year, and maybe he wasn't predicted because of the same
reasons Andrew Wiggins and Anthony-Towns were predicted, but again, that
as well as other limitations will be discussed in the conclusion.

MVP Vote Share
--------------

These results, although not as positive as the All-Star predictions,
show us a lot about how MVP is actually chosen compared to what the
stats think, but more on that later. We achieve good MAE and MSE rates,
but since Vote Share is a value between 0 and 1, they are not
particularly useful in evaluating our models because the difference is
going to be very small between the prediction and the actual number of
shares (Drakos). Therefore, we will be evaluating the model based on R2
score, which compares our model to the simplest possible model that
always predicts the mean (Drakos). The results are not great.

A huge limitation is made evident right away. As you can see in Figure
4, which shows all correlations greater than 0.1, none of the features
have a strong correlation with the amount of Vote Shares. This is a
problem because it indicates our features are not relevant enough to
predicting MVP Vote Shares, even though we have 52 features. Figures 5,
6, and 7 show how the Decision Tree, Random Forest, and Linear
Regression algorithms respectively all struggled to achieve even a
positive R2 score. Because of this failure, which is often dubbed the
Curse of Dimensionality, the three algorithms were rerun with a smaller
subset of features that were a combination of those with the highest
correlation to the Vote Shares and least correlation to each other.
Those results can be viewed in Figures 8, 9, and 10. The features used
were PTS, TRB, AST, All-Star, FGA, WS, and FG%. R2 scores improved, but
they were still extremely close to 0 and thus, not very good.

Despite all that, the results were not a complete failure, and they
still teach us a lot. Even though the metrics say the models were
horrible at predicting the actual number of vote shares, most of them
actually predicted the top vote getters somewhat accurately, albeit the
ordering might be a bit off (for the actual results, see Figure 11). Two
of the models were able to predict the winner, Russell Westbrook,
correctly, and most of them predicted many of the players who actually
received votes in real life somewhere on the list. A couple models
actually preferred James Harden, which is interesting because many
people felt he should've won the MVP at the time. The argument for
Westbrook was that he averaged a triple double, the first player to do
so in decades, the year after his friend and teammate Kevin Durant left
the Thunder. However, all the models know about is the personal stats,
powerful storylines like this are ignored. Thus, some models felt Harden
deserved the top vote more.

Two things jump out when you look at these results. The first is the
fact that DeAndre Jordan was predicted to win in the Linear regression
model with the smaller subset of features (ironically, this was our best
model in terms of R2 score). This is explained because that feature
included FG% in its small subset, and Jordan was one of the leaders in
FG% that season. The other is how underrated Jimmy Butler was in 2017
according to the stats. He is predicted to be a top five in MVP voting
in four of the six models. Clearly, by the numbers, Jimmy Butler seemed
to have had one of the best individual seasons in the entire NBA in
2017. However, no one was talking about him in the MVP conversation, and
he appeared nowhere in the actual voting. This is likely due to his lack
of team success, which leads us to the conclusion.

Conclusion
==========

Limitations
-----------

One of the biggest issues with the models is the dataset itself. There
are an incredibly overwhelming number of features. This can be just as
hurtful as it is helpful, especially since a lot of the features are
extremely correlated with each other. The most obvious examples being
how tightly coupled Win Shares is with Offensive Win Shares and
Defensive Win Shares, same with Box Plus Minus, Offensive Box Plus
Minus, and Defensive Box Plus Minus. Even though I took measures to try
to mitigate the problem, it was never enough as the MVP Vote Share
results were definitely less than optimal.

There was also a complete lack of standings data in the dataset. Our
model has no knowledge about what conference a player plays in, what
their team's record was that year, how the team performed when they did
not play, etc. Not only did this obviously hurt our MVP Vote Shares
predictions, but it affected our All-Star predictions tremendously.
Sometimes great players do not have the most amazing per game stats
because they are playing on great teams with one or more All-Star
caliber player(s). This explains why, for example, Draymond Green and
Klay Thompson were not predicted to be All-Stars. Everybody knows those
two are amongst the best players for their positions, but they played on
the same team, along with Stephen Curry and Kevin Durant who obviously
stood out more, and thus their stats were worse than they probably
would've been otherwise. Perhaps if our model knew how many games the
Warriors won and their spot in the standings, it probably would have
predicted Klay and Draymond to be All-Stars because of their tremendous
contributions to those victories, in favor of guys who played on bad
teams like Karl Anthony-Towns and Andrew Wiggins. It also might have
actually predicted Paul Millsap if it knew Millsap a top 12 player in
the Eastern conference even though he was arguably not a top 24 player
in the entire NBA. As alluded to earlier, Jimmy Butler likely would not
have been predicted as an MVP candidate either if the models knew how
his team performed.

These analyses are somewhat validated by this project, done by Alex
Nussbacher <https://www.slideshare.net/Thinkful/predicting-the-nba-mvp>.
Nussbacher was predicting MVP vote shares as well, but his dataset
included features about team standings, not just personal statistics. As
you can see from his feature-importance table, Overall Losses came in as
the second most important feature when determining MVP vote shares.
Also, as he trimmed his feature list, he achieved better results.
Nussbacher's work leads me to believe that our models would greatly
improve if team stats are added to the dataset.

Final Thoughts
--------------

Aside from the apparent issues already discussed at length in the
previous section, it is important to note just how important player
popularity with fans and media is. It would be extremely difficult for
any model that exists to accurate gauge how popular a player is, so
there will always be outliers and false negatives like DeAndre Jordan
who don't have great stats but are extremely fun to watch. Or why
Russell Westbrook was not chosen as the MVP in any of the models, even
though he averaged a triple double the year after his long-time teammate
Kevin Durant left for a 73-win Warriors team and as a result was one of
the most popular players in the league with all eyes watching him. A
player's touch with fans and media cannot be understated, as it can
often be the difference between winning the MVP and finishing second.

To attempt to answer the question of the paper, based on these findings,
it seems that personal stats don't tell the full story, as our
limitations point out. There is always more to a player than whatever
they're averaging that given year. Many players put up similar numbers,
therefore it is very difficult to distinguish them based on the numbers
alone, especially for MVP honors. Popularity is an important
consideration, but very tough to measure. One cannot simply look at
personal stats and say one player is more likely to be an All Star or
receive MVP votes than another, team stats seem to be just as necessary
to painting the complete picture. As every coach that has ever coached
at any level has always said, what counts doesn't always show up in the
box score, and our models support this idea.

**ALL-STAR CHARTS**

![](media/image1.png){width="2.652083333333333in"
height="5.6625in"}![](media/image2.png){width="2.8472222222222223in"
height="5.263888888888889in"}

![](media/image3.png){width="4.836805555555555in"
height="3.620138888888889in"}

**\
MVP CHARTS**

![](media/image4.png){width="4.111805555555556in"
height="2.8041666666666667in"}![](media/image5.png){width="2.8805555555555555in"
height="6.725694444444445in"}

![](media/image6.png){width="4.111111111111111in"
height="2.5104166666666665in"}

![](media/image7.png){width="4.184722222222222in"
height="2.7840277777777778in"}

**\
MVP CHARTS (CONT)**

![](media/image8.png){width="4.684722222222222in"
height="2.6958333333333333in"}

![](media/image9.png){width="4.760416666666667in"
height="2.852777777777778in"}![](media/image10.png){width="4.759722222222222in"
height="2.673611111111111in"}\
![A screenshot of a cell phone Description automatically
generated](media/image11.png){width="6.361111111111111in"
height="2.6805555555555554in"}

Figure 11

Works Cited

Chauhan, Nagesh Singh. "A Beginner\'s Guide to Linear Regression in
Python with Scikit-Learn." *Medium*, Towards Data Science, 7 Sept. 2019,
towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f.

Drakos, Georgios. "How to Select the Right Evaluation Metric for Machine
Learning Models: Part 1 Regression Metrics." *Medium*, Towards Data
Science, 5 Dec. 2018,
towardsdatascience.com/how-to-select-the-right-evaluation-metric-for-machine-learning-models-part-1-regrression-metrics-3606e25beae0.

"Evaluating a Classification Model." *Ritchieng.github.io*,
[www.ritchieng.com/machine-learning-evaluate-classification-model/](http://www.ritchieng.com/machine-learning-evaluate-classification-model/).

Karbhari, Vimarsh. "How to Evaluate Regression Models?" *Medium*, Acing
AI, 23 Aug. 2019,
medium.com/acing-ai/how-to-evaluate-regression-models-d183b4f5853d.

Narkhede, Sarang. "Understanding AUC - ROC Curve." *Medium*, Towards
Data Science, 26 May 2019,
towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5.

Shung, Koo Ping. "Accuracy, Precision, Recall or F1?" *Medium*, Towards
Data Science, 8 June 2018,
towardsdatascience.com/accuracy-precision-recall-or-f1-331fb37c5cb9.

Yiu, Tony. "Understanding Random Forest." *Medium*, Towards Data
Science, 14 Aug. 2019,
towardsdatascience.com/understanding-random-forest-58381e0602d2.
