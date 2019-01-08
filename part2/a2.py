#!/usr/bin/env python2
##########################################################################################################################################################
# Problem Statement : Tweet Classification
# a2.py
# Author : araghuv-sgodshal-rojraman
# 
# Implemented a Naive Bayes classifier to predit the location of the tweet based on the words given in the tweet. 
# Given: training data set : tweets.train.txt  , test data set : tweets.test1.txt
# To remove ascii special character used following commands and created 2 files tweets.test1.clean.txt  and tweets.train.clean.txt
# 
# cat tweets.test1.txt | tr '\200-\377' '*' | tr '\r' ' '   > tweets.test1.clean.txt
# cat tweets.train.txt | tr '\200-\377' '*' | tr '\r' ' '   > tweets.train.clean.txt
#
# Approach :  
# Loaded in the training File and estimated the needed probabilities to build a Bayesian model, and applied them to each tweet in the testing File.
# We selected the city which had maximum value for P(L=l|w1,w2,w3....wn)
# P(L=l|w1,w2,w3....wn) can be calculated using Bayes theorem =>  P(w1,w2,w3....wn|L=l) * P(L=l)/P(w1,w2,w3....wn)
# The denominator is ignored as it remains same for all the cities
# P(w1,w2,w3....wn|L=l) = P(w1|L=l) * P(w2|L=l) * P(w3|L=l) * ...... P(wn|L=l) 
# We have also used Laplace Smoothening to avoid divide by zero error.
# The accuracy on the given training and test data is 66.0%
#
#References: https://monkeylearn.com/blog/practical-explanation-naive-bayes-classifier/
##########################################################################################################################################################
from collections import Counter
import fileinput,math,sys
import operator


#reading data from the training file
def read_data(filename):
    data={}
    tweet_list = {}
    for line in fileinput.input(filename):
    	for i in fillers :
    	  	line = line.replace(i, " ")
        temp=line.lower().split()
        if temp[0] not in data.keys():
            data[temp[0]]=[]
            tweet_list[temp[0]]=[]
        temp_list =  filter(lambda i: i not in filler_2 and len(i) > 1, temp[1:])
        tweet_list[temp[0]].append(temp_list)
        data[temp[0]].extend(temp_list)
    return data,tweet_list

#reading data from the testing file
def read_test_data(filename):
    tweet_list = []
    test_city_list = []
    data = {}
    for line in fileinput.input(filename):
    	for i in fillers:
    	  	line = line.replace(i, " ")
        temp=line.lower().split()
        if temp[0] not in data.keys():
            data[temp[0]]=[]
        temp_list = filter(lambda i: i not in filler_2 and len(i) > 1, temp[1:])
        tweet_list.append(temp_list)
        test_city_list.append(temp[0])
        data[temp[0]].extend(temp_list)
    return tweet_list,test_city_list,data

#calculating the location probability: number of tweets of that location/ total number of tweets
def calculate_probability(training_data):
	probability_dictionary={}
	total_number_of_words_in_tweets=0
	for city,words in training_data.iteritems():
		total_words = len(words)
		total_number_of_words_in_tweets = total_number_of_words_in_tweets + total_words
		probability_dictionary[city] = total_words
	for city,probability in probability_dictionary.iteritems():
		probability_dictionary[city] = probability/float(total_number_of_words_in_tweets)
	return probability_dictionary

#calculating the frequency of each word in each city tweets and in total
def word_list_probablity(training_data): 
	word_probability = {}
	word_dict = []
	thesaurus = {}
	for city,words in training_data.iteritems():
		word_frequency_list = Counter(words)
		word_dict.extend(words)
		word_probability[city] = word_frequency_list
	thesaurus = Counter(word_dict)
	return word_probability,thesaurus

#applying the bayes theorem on the test data. Calculating the probability of all city given the word and then selecting the city with maximum probability value
def calculate_city(testing_tweet_list,word_probability,thesaurus,city_probability):
	city_output_list = []
	for tweet in testing_tweet_list:
		city_probability_list = dict(city_probability.items())
		for city,probability in city_probability_list.iteritems():
			city_probability_list[city] = probability
			city_name=city.split(",")[0].split("_")
			number_of_words = sum(word_probability[city].values())
			if city_name[len(city_name)-1] in tweet:
				city_probability_list[city] = 1.0
				break
			for word in tweet:
				city_probability_list[city] = city_probability_list[city] * ((word_probability[city][word]+1)/float(number_of_words+len(thesaurus)))
		city_output_list.append(max(city_probability_list.iteritems(), key=operator.itemgetter(1))[0])
	return city_output_list

training_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]
#filler words and characters that needs to be removed from data
fillers = ['\n' ,'\r','w/','(',')','@','-', '#' ,'&amp','?','.','*','!','__']
filler_2 = ['&amp;','',"i'm",'in','at','a','and','the','an','as','i','to','for','of','this','my','you','our','with','so','on'] 
#reading training data
training_data,training_data_tweet_list=read_data(training_file) 
#calculating city probability
city_probability = calculate_probability(training_data)
#calculating word probability
word_probability,thesaurus= word_list_probablity(training_data)
#reading test data
testing_tweet_list,test_city_list,testing_data= read_test_data(test_file)
#calculating city 
city_output_list=calculate_city(testing_tweet_list,word_probability,thesaurus,city_probability)
count = 0
#writing in the output file
file = open(output_file,"w")  
for x in range(len(test_city_list)):
	if test_city_list[x] == city_output_list[x]:
		count = count + 1
	file.write(city_output_list[x] + " " + test_city_list[x] + " " + ' '.join(testing_tweet_list[x]) + "\n")
#calculating the accuracy
print "Accuracy: " + str((count/float(len(city_output_list))) * 100) + "%" 
file.close() 
test_list_counter,test_thesaurus = word_list_probablity(testing_data)
for city,words in test_list_counter.iteritems() :
	newA = dict(sorted(words.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
	print city + ": " + str(newA)
