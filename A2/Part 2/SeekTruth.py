# SeekTruth.py : Classify text objects into two categories
#
# Code Developed by: snannap
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import time
def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    occ_cnt = dict()
    truth = "truthful"
    decpt = "deceptive"
    len_train_data = len(train_data["objects"])
    len_test_data = len(test_data["objects"])
    for i in range(len_train_data):
        try:
            read_line = train_data["objects"][i]
        except IndexError:
            read_line = 'null'
        parse_data = read_line.strip().lower().split()

        for words in parse_data:
            if words not in occ_cnt:
                occ_cnt[words] = {}
            if train_data["labels"][i] == truth:

                if truth not in occ_cnt[words]:
                    occ_cnt[words][truth] = 0
                occ_cnt[words][truth] += 1
            else:

                if decpt not in occ_cnt[words]:
                    occ_cnt[words][decpt] = 0
                occ_cnt[words][decpt] += 1

    final_res = []  
    for i in range(len_test_data):
        try:
            line_test = test_data["objects"][i]
        except IndexError:
            line_test = 'null'
        parse_test_data = line_test.strip().lower().split()
        truth_decpt_ratio = 1  
        for word in parse_test_data:

            if word not in occ_cnt:
                continue  
            else:
                if truth not in occ_cnt[word] or decpt not in occ_cnt[word]:
                    continue  

                else:
                    truth_decpt_ratio *= occ_cnt[word][truth] / occ_cnt[word][decpt]  
        if (truth_decpt_ratio > 1):  
            final_res.append(truth)
        else:
            final_res.append(decpt)

    return final_res
    #return [test_data["classes"][0]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
