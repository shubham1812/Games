 Implemented a Naive Bayes classifier to predit the location of the tweet based on the words given in the tweet. 
 
 Given: training data set : tweets.train.txt  , test data set : tweets.test1.txt
 
 To remove ascii special character used following commands and created 2 files tweets.test1.clean.txt  and tweets.train.clean.txt
 
 cat tweets.test1.txt | tr '\200-\377' '*' | tr '\r' ' '   > tweets.test1.clean.txt
 cat tweets.train.txt | tr '\200-\377' '*' | tr '\r' ' '   > tweets.train.clean.txt

 Approach :  
 
 Loaded in the training File and estimated the needed probabilities to build a Bayesian model, and applied them to each tweet in the testing File.
 
 We selected the city which had maximum value for P(L=l|w1,w2,w3....wn)
 
 P(L=l|w1,w2,w3....wn) can be calculated using Bayes theorem =>  P(w1,w2,w3....wn|L=l) * P(L=l)/P(w1,w2,w3....wn)
 
 The denominator is ignored as it remains same for all the cities
 
 P(w1,w2,w3....wn|L=l) = P(w1|L=l) * P(w2|L=l) * P(w3|L=l) * ...... P(wn|L=l) 
 
 We have also used Laplace Smoothening to avoid divide by zero error.
 
 The accuracy on the given training and test data is 66.0%
