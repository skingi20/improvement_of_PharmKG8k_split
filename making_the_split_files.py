# -*- coding: utf-8 -*-
import pandas as pd
from split_and_entity_functions import *

base_url = 'https://raw.githubusercontent.com/biomed-AI/PharmKG/master/data/PharmKG-8k/'

train = pd.read_table(base_url+'train.tsv', names=["head", "relation", "tail"])
test = pd.read_table(base_url+'test.tsv', names=["head", "relation", "tail"])
valid = pd.read_table(base_url+'valid.tsv', names=["head", "relation", "tail"])

dataset = train.append(test).append(valid).drop_duplicates()

new_train = train
new_test = test
new_valid = valid

#Setting size of each split
train_size = int(len(dataset)*0.8)
test_size = int(len(dataset)*0.1)
valid_size = int(len(dataset)*0.1)

#Making the train set
new_train = get_split_for_dataframe(dataset, train_size)

#Making the test set
dataset_no_train = dataset.append(new_train).drop_duplicates(keep=False).reset_index(drop=True)

new_test = get_split_for_dataframe(dataset_no_train, test_size).reset_index(drop=True)

#Making the valid set
new_valid = dataset_no_train.append(new_test).drop_duplicates(keep=False).reset_index(drop=True)

#Since this code doesn't check if the split is transductive, this code moves edges to make it transductive
new_train, new_test, new_valid = make_transductive(new_train, new_test, new_valid)


#Verifying the results
check_entity_overlap(new_train, new_test, new_valid)
check_edge_overlap(new_train, new_test, new_valid)

new_train.to_csv('improved_split/new_train.tsv', sep="\t", index = False)

new_test.to_csv('improved_split/new_test.tsv', sep="\t", index = False)

new_valid.to_csv('improved_split/new_valid.tsv', sep="\t", index = False)