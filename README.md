# NYT-Movie-Reviews

Natural language processing and text classification using NYT movie reviews gathered from API and website mining.

# Summary

My motivation in working on this project has been to solidify my skillset in API access, website mining and natural language processing.

I am addressing two distinct modeling problems using NYT movie review text:
  1. Given the text of a movie review, can we predict whether the movie is a NYT Critic's Pick? 
  2. Can we identify the author of a review using the review text?

I am interested in these two distinct problems because my intuition is that they depend on different characteristics of text. For the first problem, the model is likely to rely on what words and phrases are used generally in a positive versus negative review. In contrast, for the second problem, the model will rely on syntactical and language differences between writers themselves, classifying based more on style than vocabulary.

To answer these questions, I use natural language processing techniques to prepare the text data for modeling using machine learning classification models.

# Data Gathering and Cleaning

The dataset of 26,000+ reviews was sourced by first making calls to NYT Movie Review API for summary data and url for full review text, and subsequently mining each url to extract the full text of each review. The review publication dates range from 1915 to 6/30/2016. The chart below shows the number of reviews per year:

![alt text](https://github.com/cmgerr/NYT-Movie-Reviews/raw/master/Images/reviews_per_year.png)

As is clear from this chart, there are very few reviews for 2005. This needs further investigation.

To understand the dataset, I also looked at the percent of all reviews each year that designated a film as a Critic's Pick:

![alt text](https://github.com/cmgerr/NYT-Movie-Reviews/raw/master/Images/criticspick%25_per_year.png)

It is clear that either movies have gotten better since the turn of the century, or NYT has become more generous with its scoring!

For modeling, I decided to use only reviews from 2000 onward, so as to limit dataset to reviews with modern language usage. This reduced dataset still has >9000 reviews and so is sufficiently large for model building.

# Model 1: Predicting Critics' Picks

Of the dataset used for modeling, 20.5% are classified as Critics' Picks. Since the target classes are imbalanced, ROC AUC (Receiver Operating Characeristic Area Under the Curve) is the best metric to optimize and evaluate models.

I built pipelines using word stemming and count vectorization along with three different classification models: Multinomial Naive Bayes, K Nearest Neighbors and Support Vector Machine. Model hyperparameters were chosen using GridSearch. A TfidfVectorizer was also tested, but was found to produce a less successful model than the CountVectorizer.

The SVM model performed the best by far, with an ROC AUC score of 0.80 (compared with 0.70 for MultinomialNB and 0.68 for kNN). Shown below is the ROC curve for the SVM model:

![alt text](https://github.com/cmgerr/NYT-Movie-Reviews/raw/master/Images/SVM_Model_ROC_Curve.png)

To help select the model probability threshold to use, the below plot shows the True Positive Rate, False Positive Rate, and Precision plotted against the model's predicted probability of a film being a critic's pick:

![alt text](https://github.com/cmgerr/NYT-Movie-Reviews/raw/master/Images/SVM_Model_P_Threshold.png)

## Next Steps

For further enhancement of this model, I plan to implement a lemmatizer instead of a stemmer to more accurately truncate words, and also to incorporate the month of the review as a model feature. As the graph below shows, there is a seasonal trend in Critic's Pick designations.

![alt text](https://github.com/cmgerr/NYT-Movie-Reviews/raw/master/Images/criticspick%25_per_month.png)

# Model 2: Identifying Review Author

To approach this problem, I first restricted the dataset to the six most common authors, dropping the long tail of 34 others. These authors' names were label encoded as the target variable. With six different target classes, I selected accuracy as the scoring metric. 

Several hundred reviews had the author's name mentioned in the review text, so to eliminate this "giveaway" feature as well as to avoid noisy features with movie stars' and characters' names, I used spaCy to remove all Person entities from every review text before modeling.

For the preliminary model, I gridsearched optimal hyperparameters for a pipeline with word stemming, count vectorization and a SVM model (since the SVM model was most successful in predicting Critics' Picks). This preliminary model is quite accurate, achieving a score of 0.93. Below is the confusion matrix for actual and predicted authors, displaying the very low misclassification numbers.

![alt text](https://github.com/cmgerr/NYT-Movie-Reviews/raw/master/Images/author_svm_confusion_matrix.png)

Despite my initial intuition that the second modeling problem would require a more nuanced style analysis of the reviews to be successful, the SVM model only uses counts of individual words in each review and is still highly accurate. However, I am confident that by incorporating more nuanced features extracted from the text, the accuracy can be further increased.

## Next Steps

As next steps for this second problem, I plan to use topic modeling techniques in order to incorporate topics as features, and to incorporate ratios of part-of-speech tags in reviews. I also plan to build and tune an Artificial Neural Network to compare with the SVM model.

