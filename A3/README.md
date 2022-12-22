# snannap-krachoud-prabchau-a3


# Part 1

## AIM
- The aim is to use three types of Bayes Nets~ Simple, HMM, and MCMC ~ to identify and assign part of speech for each word in the sentence. 
- To run this python code use the following arguments: ./label.py bc.train bc.test

## Trained data stored in following dictionaries
- word_tag_count = Stores separate tags for each word in the sentence.
- tag_occ_count = Stores track the frequency of each tag.
- sentence_start_prob = Keeps track of the chances that a specific tag will appear at the start of the sentence.
- emission_prob = Stores emission probabilities
- transmission_prob = Stores transmission probabilities

## Simplified Model- 
- This model does not include a lot of data. It is simple to create this Bayes network because each observed variable just depends on the current state and hidden variable. The hidden states are not dependent on one another.
- Every time we calculate the emission probabilities for the word with all the potential tags, we do so in order to determine the ideal tag sequence. The tag corresponding to the highest emission probability is chosen, and it is kept as the tag for that term. That is, among all the tags connected to this word, we identify the tag with the highest probability.
- if w contains the tags s 1......s k (For every phrase) = c(w,s i)/c(w,s 1) = p(s i/w) + ... + c(w, s k)
Here, c(w,s i) represents the number of times w/s i appears in the text.
A term or tag is given the most frequent tag in the text if it appears in the test set but not the train set.
- The HMM problem is tackled next using the Viterbi technique.

## Viterbi- 
- The observed variable in this model depends on its hidden variable, and the hidden variable likewise depends on the hidden variable of the previous observed variable. 
- It calculates emission probability using initial probability and transition probability.
- The transition probability is calculated from the input text file. It is stored as a python dictionary. 
- We've kept track of a list that contains a dictionary since viterbi uses the idea of dynamic programming, and the dictionary provides the probabilities for all the POS tags for a given word.
- The best algorithm we can use in this situation is viterbi. When the maximum probability= 0, we conclude that the word is unknown. Assigning speech probability to maximum probability as a result.

## Challenges- 
Fine tuning Viterbi to get best results-
1. When the state value is 0, we assign a very small value. If a state's maximum value is zero when the last state value and transition value are added together, that state's default state value is 1e-10.
2. When the product of the last state value and the transition value is zero, we assign the default tag of "noun" to any state that has a maximum value in that range.

## Complex MCMC- 
- Here, we used Gibbs Sampling. The first sample taken into consideration has all tags set to noun. The first 100 of the 500 samples we produced were burned. Starting with the data, we assume that the starting sentence will have random POS tags. 
- Next, we begin randomizing the POS tags. Using the distribution, we calculate each word's probability given that all the other words have been tagged. Using the following algorithm, we assign this word the highest possible POS tag:

 1. P(W0)=P(Wi/S0)*P(S0) [[[Probability of first word]]
 2. P(Wi/Si)=P(Wi/Si)*P(Si/Si-1)*P(Si-1)*P(Si/S0)*P (S0) [[Probability of last word]]
 
- Every word's likelihood for each sample is determined for each of the 12 parts of speech, and the word is then taken into consideration for the part of speech with the highest probability. 
- 1000 samples are processed where the values of first sample is consists noun for every word in a sentence. 
- The current sample's tag for this word is then modified so that it will be utilized in the following round of samples. A tag count is then stored for each word from the samples when this is completed for 1000 samples.
- The first 500 samples are disregarded while performing this. The final pos tags list will have tags with the highest probability tag value for all the words, since the tag with the highest count for a word will be the final tag for that word.

------------ 
-  Results: ==> So far scored 2000 sentences with 29442 words. 
-                  Words correct:              Sentences correct:                
- 0. Ground Truth            100.00%                     100.00% 
- 1. Simple:                  92.91%                      43.15%
- 2. HMM:                     95.06%                      54.25%
- 3. Complex:                 92.09%                      40.80%
-------------


# Part 2

## AIM
- The aim is to use two types of Simple Bayes Nets, HMM with map inference to extract text from a noisy scanned image of a document. 
- To run this python code use the following arguments: python3 image2text.py courier-train.png bc.train testimages/<<image_name>>.png
## Walk Through of the problem
- We are required to predict two output with simple bayes and HMM. 
- We had used intial and transition probablities. As inorder we need the train data we had reused bc.train file,In order to get the emission probabilities, we compared each training letter to each testing letter and looked at which testing letter matched up closest to the training letter by comparing a ratio of correct black and white characters relative to the total number of characters.
- Using these probabilities, the Simple Bayes net obtained an optimal result for each hidden state (letter). We then implemented the initial state probabilities, transition probabilities, and emission probabilities into a HMM.
- In this matrix, a viterbi matrix was created and backpropagated to find the optimal output using MAP inference.
- Final simple bayes and HMM text outputs will be printed.
## Assumption and Workaround
- First thing we should have a training data inorder to go furhter, we have decided to use the bc.train with POS removal.
- One relatively important assumption we had to make when developing the initial state probabilities was whether we wanted the initial state probabilities to reflect the likelihood that a word starts with a particular letter or whether we wanted the initial state probabilities to reflect the likelihood that a sentence starts with a particular letter. 
- With the first option, we have more instances to train on (more total words than total sentences).
- With the emission probabilities, we decided to use a weighted system since it greatly improved the simple bayes outputs. We decided on the weights (0.6 & 0.4) vs (0.9 & 0.1) after some parameter tuning and testing. 
-  As a result of the emission and transition probs working so accurately in the simple bayes output, we opted to use a weighted-based approach again when incorporating them into the viterbi algorithm, adding transition probs and previous state veribi outputs as additional components to emphasize the emission probability more.
