# reddit-predictor
A naive Bayes classifier written in Python with the intent to predict the popularity of a post to the social media website Reddit. Parses a .csv file to obtain links to posts, separates the links into training and test sets, then obtains data from the post using an external library to interact with Reddit's API. The classifier then uses the data from the training set to determine the likelihood that a post from the test set is popular.

`publicdata.py` retrieves the desired attributes from Reddit using a massive collection of posts given in `publicvotes.csv` and writes them to the file `lotsdata.csv`.

`naive_bayes.py` implements a Naive Bayes Classifier with the collected data.
