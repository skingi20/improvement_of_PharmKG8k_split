# -*- coding: utf-8 -*-
import pandas as pd

base_url = 'https://raw.githubusercontent.com/biomed-AI/PharmKG/master/data/PharmKG-8k/'

train = pd.read_table(base_url+'train.tsv', names=["head", "relation", "tail"])
test = pd.read_table(base_url+'test.tsv', names=["head", "relation", "tail"])
valid = pd.read_table(base_url+'valid.tsv', names=["head", "relation", "tail"])

dataset = train.append(test).append(valid).drop_duplicates()

#Setting size of each split
train_size = int(len(dataset)*0.8)
test_size = int(len(dataset)*0.1)
valid_size = int(len(dataset)*0.1)

def get_split_for_dataframe(dataframe, split_size):
    """
    get_split_for_dataframe takes a graph as a dataframe and an amount 
    of edges decided by split_size and returns a dataframe. In this dataframe
    it is made sure that if a "head","tail" is added to the dataframe, any 
    other edges with this same "head","tail" or a symmetric edge with the same
    "tail","head" is also added to the return dataframe.

    :param dataframe: A pandas dataframe with the header "head","relation","tail"
    :param split_size: An integer deciding how many edges is wanted in the new dataframe, 
    has to be less or equal to the dataframe size
    :return: A pandas dataframe with the header "head","relation","tail"
    """
    moved_pairs = set()
    split_dataframe = set()
    pharm_kg_no_relation = dataframe[['head','tail']]
    pharm_kg_list = list(pharm_kg_no_relation.itertuples(index=False, name=None))
    i = - 1
    for ind in dataframe.index:
        i = i+1
        if i%1000 == 0:
            print(f'{i} out of {split_size} done')
        head_tail = (dataframe.iat[ind, 0], dataframe.iat[ind, 2])
        tail_head = (dataframe.iat[ind, 2], dataframe.iat[ind, 0])
        if head_tail in moved_pairs or tail_head in moved_pairs:
            continue
        head_relation_tail = (dataframe.iat[ind, 0], dataframe.iat[ind, 1], dataframe.iat[ind, 2])
        split_dataframe.add(head_relation_tail)
        moved_pairs.add(head_tail)
        moved_pairs.add(tail_head)
        start_index = i + 1  # Start checking from the next index
        indexes = [index for index, value in enumerate(pharm_kg_list[start_index:], start=start_index) if
                   value == head_tail or value == tail_head]
        for index in indexes:
            split_dataframe.add((dataframe.iat[index,0],dataframe.iat[index,1],dataframe.iat[index,2]))
        if len(split_dataframe) >= split_size:
            break
    df = pd.DataFrame(split_dataframe, columns =['head', 'relation', 'tail'])
    return df


new_train = get_split_for_dataframe(dataset, train_size)

dataset_no_train = dataset.append(new_train).drop_duplicates(keep=False).reset_index(drop=True)

new_test = get_split_for_dataframe(dataset_no_train, test_size)

new_valid = dataset_no_train.append(new_test).drop_duplicates(keep=False)

new_train.to_csv('improved_split/new_train.tsv', sep="\t", index = False)

new_test.to_csv('improved_split/new_test.tsv', sep="\t", index = False)

new_valid.to_csv('improved_split/new_valid.tsv', sep="\t", index = False)