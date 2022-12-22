###################################
# CS B551 Fall 2022, Assignment #3
#
# Code by:
# Krati Choudhary : krachoud
# Prabhruti Chaudhary : prabchau
# Sai Tanishq : snannap
# (Based on skeleton code by D. Crandall)
#
import copy

from PIL import Image
import math
import sys
import operator

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
global TRAIN_LETTERS
global arrow
arrw = "-->"
TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

#In order to improve accuracy, the opposite color correct performance needs to be valued more if the ratio is high
# i.e. if the test file is corrupted with a lot of blacks, increase the white correct weight and decrease the black correct weight
#and vice versa if the test file is corrupted with a lot of whites
class black_test:
    def black_test(self,test_letters):
            black_test,test_sum = 0,0
            for lttr in test_letters:
                for l in lttr:
                    for c in l:
                        test_sum += 1
                        if c != '*':
                            continue
                        else:
                            black_test += 1

            return [black_test,test_sum]


    def black_train(self,train_letters):
        black_train,train_sum = 0,0
        for lttr in train_letters:
            for l in train_letters[lttr]:
                for c in l:
                    train_sum += 1
                    if c != '*':
                        continue
                    else:
                        black_train += 1

        return [black_train,train_sum]

# Read in the text training data
def read_text():
    inpt_data = []
    file = open(train_txt_fname, 'r');
    for line in file:
        dat = [wrds + ' ' for wrds in line.split()]

        inpt_data.append(dat)

    return inpt_data


# Initial state probabilities
def start_state():
    inpt = read_text()
    init_state = {}

    for l in inpt:
        for wrds in l:
            if wrds[0] not in TRAIN_LETTERS:
                continue
            else:
                if wrds[0] in init_state:
                    init_state[wrds[0]] += 1
                else:
                    init_state[wrds[0]] = 1

    # Percent of all wrdss that start with each letter
    intit_prob = {}
    for lttr in init_state:
        intit_prob[lttr] = init_state[lttr] / float(sum(init_state.values()))

    return intit_prob

def totaltransition(transition_letters):
    trnst_cnt = {}
    for i in range(len(TRAIN_LETTERS)):
        cnt = 0

        # Loop through transitions dict and count appearances for each letter
        for lttr in transition_letters:
            if (TRAIN_LETTERS[i] == lttr.split('-->')[0]):
                cnt = cnt + transition_letters[lttr]
            else:
                continue

        # Save final count
        if cnt < 0:
            raise Exception("Count can't be negetive")
        else:
            trnst_cnt[TRAIN_LETTERS[i]] = cnt


    # Create count percentages as count / total count
    sum_cnt = sum(trnst_cnt.values())
    for lttr in trnst_cnt:
        trnst_cnt[lttr] = trnst_cnt[lttr] / sum_cnt


    # Create transition probabilities dict to find % that letter B follows letter A
    # i.e. 10 total appearances of "T", 7 of which are followed by "h", so T-->h = 0.7
    transt_prob = {}
    for lttr in transition_letters:
        transt_prob[lttr] = (transition_letters[lttr]) / (float(trnst_cnt[lttr.split(arrw)[0]]))


    prob_total = {}
    trans_total = sum(transt_prob.values())
    for p in transt_prob:
        prob_total[p] = transt_prob[p] / float(trans_total)

    return prob_total
    


# transition probabilities
def transition():
    dta = read_text()
    transt_lttrs = {}

    # Output the number of transitions for specific letter pairs
    for l in dta:
        for wrds in l:
            for i in range(len(wrds) - 1):
                if (wrds[i] in TRAIN_LETTERS and wrds[i + 1] in TRAIN_LETTERS):
                    transt_lttrs[wrds[i] + arrw + wrds[i + 1]] = 1
                
                else:
                    if (wrds[i] in TRAIN_LETTERS and wrds[i + 1] in TRAIN_LETTERS) and (
                        wrds[i] + arrw + wrds[i + 1]) in transt_lttrs:
                        transt_lttrs[wrds[i] + arrw + wrds[i + 1]] += 1  
                    else: 
                        continue
    return totaltransition(transt_lttrs)
    


# Emission probabilities

def emission(test_letters, train_letters):

    prob_val = {}
    s = black_test()
    testval = s.black_test(test_letters)
    trainval = s.black_train(train_letters)


    # Loop through test letters and train letters of emmision probability
    for test_lttr in range(len(test_letters)):
        prob_val[test_lttr] = {}
        for train_let in train_letters:
            isblack = 0
            iswhite = 0
            dim = CHARACTER_WIDTH * CHARACTER_HEIGHT
            # Need to loop through two levels
            for i in range(len(test_letters[test_lttr])):
                for x in range(len(test_letters[test_lttr][i])):
                    if test_letters[test_lttr][i][x] != train_letters[train_let][i][x] and train_letters[train_let][i][x] != '*':
                        pass
                    else:
                        isblack += 1
                    if test_letters[test_lttr][i][x] != train_letters[train_let][i][x] and train_letters[train_let][i][x] != ' ':   
                        pass
                    else:
                        iswhite += 1

                    # After some testing, for more corrupted files with lots of blacks, lowering black coefficient
                    # improves performance while for more corrupted files with lots of white, increasing black coefficient
                    # improves performance

                    if (testval[0]/testval[1]) < (trainval[0]/trainval[1]):
                        prob_val[test_lttr][train_let] = 0.9 * (isblack / dim) + 0.1 * (iswhite / dim)
                    else:
                        prob_val[test_lttr][train_let] = 0.6*(isblack / dim) + 0.4*(iswhite/dim)

    return prob_val


# Output results from simple bayes net
def simple_bayes(test_letters, train_letters):
    final_text = ''
    prob_emmision = emission(test_letters, train_letters)
    for val in prob_emmision:
        final_text += ''.join(max(prob_emmision[val], key = prob_emmision[val].get))

    return final_text


# Output results from HMM using Viterbi algo
def hmm_viterbi(test_letters, train_letters):

    # Initialize initial state, transition, and emission probs
    intit_state = start_state()
    total_transit = transition()
    prob_emmision = emission(test_letters,train_letters)

    # Initialize final output and viterbi matrix
    output = ['X'] * len(test_letters)
    viterbi = []

    for train_val in range(len(TRAIN_LETTERS)):
        subset_vit = []
        for test_val in range(len(test_letters)):
            subset_vit.append([0,''])
        viterbi.append(subset_vit)


    # Taking top 5 probalities from simple bayes

    # Get initial state using initial state probs
    top5 = dict(sorted(prob_emmision[0].items(), key=lambda x: x[1], reverse=True)[:5])
    for train_val in range(len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[train_val] in intit_state and TRAIN_LETTERS[train_val] in top5 and top5[TRAIN_LETTERS[train_val]] != 0:
            viterbi[train_val][0] = [-math.log(top5[TRAIN_LETTERS[train_val]],10),TRAIN_LETTERS[train_val]]

    # Remainder of states again taking top 5 emissions for each
    for test_val in range(1,len(test_letters)):
        top5 = dict(sorted(prob_emmision[test_val].items(), key=lambda x: x[1], reverse=True)[:5])

        # Loop through each of the top 5 emissions and add them to the viterbi matrix with transition probs added
        for val in top5:
            subset_vit = {}
            for train_val in range(len(TRAIN_LETTERS)):
                if (TRAIN_LETTERS[train_val]+arrw+val) in total_transit and viterbi[train_val][test_val-1][0] != 0:
                    # Adding additional weights to emission probabilities since they performed well previously       
                    subset_vit[val] = -40* math.log(top5[val],10) - 0.009*math.log(total_transit[TRAIN_LETTERS[train_val]+arrw+val],10) - 0.009*math.log(viterbi[train_val][test_val-1][0],10)

            # Create our final viterbi matrix from the sub-viterbi for each state
            maxval=100000
            x = maxval-1
            for key in subset_vit:
                if x < subset_vit[key]:
                    pass
                else:
                    x = subset_vit[key]
                    final_letter = key
                viterbi[TRAIN_LETTERS.index(val)][test_val] = [subset_vit[final_letter],final_letter]


    # Running through the viterbi matrix
    for test_val in range(len(test_letters)):
        # default large num to minimize
        x = maxval-1
        for train_val in range(len(TRAIN_LETTERS)):
            # Minimizing the cost - if the new value has a lower cost than the previous value for each state, replace the output with the new state (letter)
            if train_val < len(TRAIN_LETTERS) and viterbi[train_val][test_val][0] < x and viterbi[train_val][test_val][0] != 0: 
                x = viterbi[train_val][test_val][0]
                output[test_val] = TRAIN_LETTERS[train_val]


    return ''.join(output)



print("Simple: {}".format(simple_bayes(test_letters,train_letters)))
print("HMM: {}".format(hmm_viterbi(test_letters,train_letters)))

