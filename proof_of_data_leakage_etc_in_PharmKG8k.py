# -*- coding: utf-8 -*-
import pandas as pd
from split_and_entity_functions import check_entity_overlap, check_edge_overlap

base_url = 'https://raw.githubusercontent.com/biomed-AI/PharmKG/master/data/PharmKG-8k/'

train = pd.read_table(base_url+'train.tsv', names=["head", "relation", "tail"])
test = pd.read_table(base_url+'test.tsv', names=["head", "relation", "tail"])
valid = pd.read_table(base_url+'valid.tsv', names=["head", "relation", "tail"])

#Get internal duplicates count
train_dups = len(train)-len(train.drop_duplicates())
test_dups = len(test)-len(test.drop_duplicates())
valid_dups = len(valid)-len(valid.drop_duplicates())

#Drop duplicates
train.drop_duplicates(inplace = True)
test.drop_duplicates(inplace = True)
valid.drop_duplicates(inplace = True)

#Print relevant info
print(f'Internal full duplicate edges:\nTrain: {train_dups}\nTest: {test_dups}\nTrain: {valid_dups}\n')
print('Entity overlaps:')
check_entity_overlap(train, test, valid)
print('\nEdge overlaps:')
check_edge_overlap(train, test, valid)