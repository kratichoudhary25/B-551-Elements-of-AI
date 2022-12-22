###################################
# CS B551 Fall 2022, Assignment #3
#
# Code by:
# Krati Choudhary : krachoud
# Prabhruti Chaudhary : prabchau
# Sai Tanishq : snannap
# (Based on skeleton code by D. Crandall)
#


import random
import math


class Solver:
    global base
    base = 0.000000145
    
    
    word_tag_count = {} # Dictionary to store different tags for any word of the sentence
    tag_occ_count = {} # Dictionary to store count for each tag's occurance
    sentence_start_prob = {} # Dictionary to store the probabilities that a particular tag appears at the beginning of the sentence
    emission_prob = {} # Dictionary to store emission probabilities
    transmission_prob = {} # Dictionary to store transmission probabilities
    
    # We will determine the posterior probability of a given sentence by computing its log
    def posterior(self, model, sentence, label):
        # --------------- For Bayes Model ------------------
        if model == "Simple":
            posterior_prob = 0
            tag_count_sum = sum(self.tag_occ_count.values())
            for word in range(len(sentence)):
                if sentence[word] in self.word_tag_count:
                    if label[word] in self.word_tag_count[sentence[word]]:
                        prob_tag = self.tag_occ_count[label[word]]/tag_count_sum
                        posterior_prob += math.log(self.emission_prob[sentence[word]][label[word]]*prob_tag,10)
                    else:
                        max_occuring_tag = max(self.tag_occ_count, key=self.tag_occ_count.get)
                        val = self.tag_occ_count[max_occuring_tag]
                        posterior_prob += math.log(val/tag_count_sum,10)

            return posterior_prob
        # --------------------- For Viterbi Hidden Markov Model ----------------
        elif model == "HMM":
            posterior_prob = 0
            # Here we will calculate probability for first word using HMM
            if sentence[0] in self.emission_prob and label[0] in self.emission_prob[sentence[0]]:
                posterior_prob += math.log((self.sentence_start_prob[label[0]] * self.emission_prob[sentence[0]][label[0]]),10)
            else:
                posterior_prob += math.log((base * self.sentence_start_prob[label[0]]),10)
            
            # Estimating the probability of the remaining words to determine the final log posterior probabilities
            for i in range(1, len(sentence)):
                prob_tag = self.tag_occ_count[label[i]]/sum(self.tag_occ_count.values())
                if sentence[i] in self.emission_prob and label[i] in self.emission_prob[sentence[i]]:
                    posterior_prob += math.log((self.emission_prob[sentence[i]][label[i]]),10)
                else:
                    posterior_prob += math.log(base,10)
                if (label[i], label[i-1]) in self.transmission_prob:
                    posterior_prob += math.log((self.transmission_prob[(label[i], label[i-1])] * prob_tag),10)
                else:
                    posterior_prob += math.log(base * prob_tag,10)
            return posterior_prob

        # ------------------ For Montecarlo Marcov Chain Model -------------------- 
        elif model == "Complex":
            posterior_prob = 0
            # Calculating the probability of POS being the first word
            if sentence[0] in self.emission_prob:
                if label[0] in self.emission_prob[sentence[0]]:
                    posterior_prob += math.log(self.sentence_start_prob[label[0]] * self.emission_prob[sentence[0]][label[0]],10)
                    posterior_prob += math.log(self.tag_occ_count[label[0]]/sum(self.tag_occ_count.values()),10)
            else:
                posterior_prob += math.log(base * self.sentence_start_prob[label[0]],10)
                posterior_prob += math.log(self.tag_occ_count[label[0]]/sum(self.tag_occ_count.values()),10)
            
            # Estimating the probability of the remaining words, except the final word
            for word in range(1, len(sentence)-1):    
                prob_tag = self.tag_occ_count[label[word]]/sum(self.tag_occ_count.values())
                if sentence[word] in self.emission_prob:
                    if label[word] in self.emission_prob[sentence[word]]:
                        posterior_prob += math.log(self.emission_prob[sentence[word]][label[word]],10)
                
                else:
                    posterior_prob += math.log(base,10)
                
                # If probability of current word was correctly determined we update the value of posterior probability
                if((label[word], label[word-1]) in self.transmission_prob):
                    posterior_prob += math.log(self.transmission_prob[(label[word], label[word-1])] * prob_tag,10)
                else:
                    posterior_prob += math.log(base * prob_tag,10)
                    
            # Estimating the probability of the last word using the last word and the word before it
            if sentence[-1] in self.emission_prob:
                if label[-1] in self.emission_prob[sentence[-1]]:
                    posterior_prob += math.log(self.emission_prob[sentence[-1]][label[-1]],10)
            else:
                posterior_prob += math.log(base,10)

            if label[-1] in self.transmission_prob and label[-2] in self.transmission_prob:
                posterior_prob += math.log(self.transmission_prob[(label[-1], label[-2])],10)
                posterior_prob += math.log(self.tag_occ_count[label[-1]]/sum(self.tag_occ_count.values()),10)
            else:
                posterior_prob += math.log(base,10)
                posterior_prob += math.log(self.tag_occ_count[label[-1]]/sum(self.tag_occ_count.values()),10)
            
            if (label[-1], label[0]) in self.transmission_prob:
                posterior_prob += math.log(self.transmission_prob[(label[-1], label[0])],10)
                posterior_prob += math.log(self.tag_occ_count[label[0]]/sum(self.tag_occ_count.values()),10)
            else:
                posterior_prob += math.log(base,10)
                posterior_prob += math.log(self.tag_occ_count[label[0]]/sum(self.tag_occ_count.values()),10)
            
            return posterior_prob

        else:
            print("Unknown algo!")


    def train(self, data):
        for i in range(len(data)):
            words, sent_pos_tag = data[i]
    
            start = sent_pos_tag[0]
            
            if start in self.sentence_start_prob:
                temp = self.sentence_start_prob[start]
                temp += 1
                self.sentence_start_prob[start] = temp
            
            elif start not in self.sentence_start_prob:
                self.sentence_start_prob[start] = 1    
            
            for w in range(len(words)):
                # Each word and its matching POS in a loop.
                word = words[w]
                tag = sent_pos_tag[w]         

                # Estimating the probability that two words will appear one after the other
                if w+1 < len(words):
                    if (sent_pos_tag[w+1], tag) not in self.transmission_prob:
                        self.transmission_prob[(sent_pos_tag[w+1], tag)] = 1
                    
                    else:
                        self.transmission_prob[(sent_pos_tag[w+1], tag)] += 1

                if word not in self.word_tag_count:
                    self.word_tag_count[word] = {tag:1}
                else:
                    if tag not in self.word_tag_count[word]:
                        self.word_tag_count[word].update({tag:1})
                    else:
                        tag_count1 = self.word_tag_count[word][tag]
                        tag_count1 += 1
                        self.word_tag_count[word][tag] = tag_count1

                if tag not in self.tag_occ_count:
                    self.tag_occ_count[tag] = 1
                else:
                    tag_count2 = self.tag_occ_count[tag]
                    tag_count2 += 1
                    self.tag_occ_count[tag] = tag_count2
        
        # Computing all the initial probabilities
        for tags in self.sentence_start_prob:
            self.sentence_start_prob[tags] = self.sentence_start_prob[tags]/len(data)
        
        # Computing all the transition probabilities
        for tprobs in self.transmission_prob:
            self.transmission_prob[tprobs] = self.transmission_prob[tprobs]/self.tag_occ_count[tprobs[1]]

        # Computing all the emission probabilities        
        self.emission_prob = self.word_tag_count
        for w in self.emission_prob:
            for pos in self.emission_prob[w]:
                self.emission_prob[w][pos] = self.emission_prob[w][pos]/self.tag_occ_count[pos]

# --------------- Function for Simple ,i.e, Bayes Net --------------
    def simplified(self, sentence):
        speech_tag = []
        for word in sentence:
            maxP = 0
            current_pos = ''

            # If the train set does not contain the word from the test set then 
            if word not in self.word_tag_count:
                # The tag with the greatest number of occurrences in a collection will be assigned.
                current_pos = max(self.tag_occ_count, key = self.tag_occ_count.get)
            else:
                 # We will obtain a word's entire tag assignment
                tags = self.word_tag_count[word]
                # Now we will estimate and calculate the total assignment
                total = sum(tags.values())
                for pos in tags:
                    prob = tags[pos]/total
                    if prob > maxP:
                        maxP = prob
                        current_pos = pos
            speech_tag.append(current_pos)
        return speech_tag

# -------------- Function for HMM with viterbi -------------------
    def hmm_viterbi(self, sentence):
        #sent_pos_tag: Final POS tags for the sentence.
        sent_pos_tag = []
        #viterbi: list of dictionaries for each word containing probabilities of all the POS for that word
        viterbi = []
        tmp = {}
        
        # Getting the most probable tag for the first word in the sentence
        for t in self.tag_occ_count:
            if sentence[0] in self.emission_prob:
                if t in self.emission_prob[sentence[0]]:
                    tmp[t] = (self.emission_prob[sentence[0]][t] * self.sentence_start_prob[t], t)
                else:
                    # 2.22044604925e-16 is the lower limit of a floating point number
                    tmp[t] = (2.22044604925e-16, t)
            else:
                tmp[t] = (2.22044604925e-16, t)
        viterbi.append(tmp)
        
        # Traversing through rest of the words in the sentence to get most probable tag for each
        for i in range(1, len(sentence)):
            tmp_dict = {}
            tag_prev = viterbi[i-1]
            for t1 in self.tag_occ_count:
                mx = 0
                current = t1
                for t2 in self.tag_occ_count:
                    val = 0
                    if (t1,t2) in self.transmission_prob:
                        val = self.transmission_prob[(t1,t2)] * tag_prev[t2][0]
                    else:
                        val = 2.22044604925e-16 * tag_prev[t2][0]
                    if val>mx:
                        mx = val
                        current = t2
                if mx == 0:
                    mx = 2.22044604925e-16
                if sentence[i] in self.emission_prob and t1 in self.emission_prob[sentence[i]]:
                    tmp_dict[t1] = self.emission_prob[sentence[i]][t1] * mx, current
                else:
                    tmp_dict[t1] = (2.22044604925e-16 * mx, current)
            viterbi.append(tmp_dict)
        
        # Getting the tag of the last word having maximum probability
        maxP = 0
        prev_tag = ''
        end = ''
        last_col = viterbi[len(sentence)-1]
        for t in last_col:
            prob, prev = last_col[t]
            if prob > maxP:
                maxP = prob
                prev_tag = prev
                end = t
        if len(sentence) > 1:
            sent_pos_tag.append(end)
        sent_pos_tag.append(prev_tag)
        
        #Backtracking to get rest of the tags assigned to the words in the sentence
        for i in range(len(sentence)-2,0,-1):
            col = viterbi[i]
            prob, prev = col[prev_tag]
            sent_pos_tag.append(prev)
            prev_tag = prev
        
        sent_pos_tag.reverse()

        return sent_pos_tag

# ------------------ Function for Monte Carlo Markov Chain -------------
    def complex_mcmc(self, sentence):
        # Storing counts of different POS for each word
        dictCount={}

        # Initializing 1000 samples for comparing the tags
        samples_tag = [[]] * 1000
        samples_tag[0] = ["verb"] * len(sentence)

        posTags = list(self.tag_occ_count)

        for sple in range(1, 1000):

            samples_tag[sple] = samples_tag[sple - 1]

            # Traversing through every word in sentence
            for words in range(len(sentence)):

                maxTag = ''
                maxProb = 0

                #iterate for every pos
                for pos_iter in range(len(posTags)):
                    # Current POS tag
                    speech = posTags[pos_iter]

                    trans = 1
                    intial = self.sentence_start_prob[speech]
                    emm = base

                    if sentence[words] in self.emission_prob:
                        if speech in self.emission_prob[sentence[words]]:
                            emm = self.emission_prob[sentence[words]][speech]
           
            # --------- If current word is not the first word --------------
                    if words != 0:

                        trans = base
                        intial = base
          
            # ------------ If current word is last word -------------------
                        if words == len(samples_tag) - 1:

                            if (speech, samples_tag[sple][words - 1]) in self.transmission_prob and (
                            speech, samples_tag[sple][0]) in self.transmission_prob:
            
            # ------------- If current word is between the first and last word ----------
                                trans = self.transmission_prob[(speech, samples_tag[sple][words - 1])] * \
                                        self.transmission_prob[(speech, samples_tag[sple][0])]
                            else:
                                
                            # Transmission probabilty
                                if (speech, samples_tag[sple][0]) in self.transmission_prob:
                                    trans = self.transmission_prob[(speech, samples_tag[sple][words - 1])]*base
                                if (speech, samples_tag[sple][words - 1]) in self.transmission_prob:
                                    trans = self.transmission_prob[(speech, samples_tag[sple][words - 1])]*base
                            
                            # Initial probability
                            intial = self.sentence_start_prob[speech] * self.sentence_start_prob[samples_tag[sple][0]]

                        else:
                            trans = base
                            intial = base
                           
                            # Transmission probabilty
                            if (speech, samples_tag[sple][words - 1]) in self.transmission_prob:
                                trans = self.transmission_prob[(speech, samples_tag[sple][words - 1])]
                            
                            # Initial probability
                            intial = self.sentence_start_prob[speech]
                    

                    probab = emm * trans * intial
                    if maxProb < probab:
                        maxProb = probab
                        maxTag = speech

                samples_tag[sple][words] = maxTag

        for sple in range(500,1000):
                for tgs in range(len(samples_tag[sple])):
                    if tgs in dictCount:
                        if samples_tag[sple][tgs] in dictCount[tgs]:
                            dictCount[tgs][samples_tag[sple][tgs]]+=1
                        else:
                            dictCount[tgs][samples_tag[sple][tgs]]=1
                    else:
                        dictCount[tgs]={}
        sent_pos_tag=[]

        for word,val in dictCount.items():
            tag=max(val, key=val.get)
            sent_pos_tag.append(tag)

        return sent_pos_tag

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")