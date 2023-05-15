# -*- coding: utf-8 -*-
import pandas as pd

base_url = 'https://raw.githubusercontent.com/biomed-AI/PharmKG/master/data/PharmKG-8k/'

train = pd.read_table(base_url+'train.tsv', names=["head", "relation", "tail"])
test = pd.read_table(base_url+'test.tsv', names=["head", "relation", "tail"])
valid = pd.read_table(base_url+'valid.tsv', names=["head", "relation", "tail"])

def find_duplicates_between_two_sets(df1, df2):
    """
    Find duplicates between two datasets and return two dataframes.

    Args:
        df1 (pandas.DataFrame): The first dataset to compare.
        df2 (pandas.DataFrame): The second dataset to compare.

    Returns:
        all_dups (pandas.DataFrame): 
        A dataframe containing the triples that are involved in a head-tail or tail-head match between df1 and df2. 
        If a tail-head match makes a triple completely identical to another, only one of the triples will be included. 
        The dataframe contains the following columns:
            - head: the head entity of the triple.
            - relation: the relation between the head and tail entities.
            - tail: the tail entity of the triple.
        all_dups_witout_relation (pandas.DataFrame): 
        A dataframe containing the unique combinations of "head, tail" to "head, tail" and "tail,head" to "head,tail". 
        The dataframe contains the following columns:
            - head: the head entity of the duplicate pair.
            - tail: the tail entity of the duplicate pair.

    This function compares two datasets to find the number of duplicates between them. 
    It does this by first finding all the triples that are present in both datasets (i.e., have the same head and tail entities). 
    It then identifies the unique pairs of head-tail entities that have at least one duplicate triple in both datasets. 
    The two resulting dataframes provide different levels of information about the duplicates: 
    all_dups contains the full triples that are duplicated, while all_dups_witout_relation contains only the head-tail entity pairs that are duplicated.

    Example usage:
        train_x_test_dups, train_x_test_without_relation = find_duplicates_between_two_sets(train_set, test_set)
    """
    # Find all the rows in df1 and df2 that have the same head and tail values
    all_inner_head_head_1 = pd.merge(df1, df2, on=["head", "tail"], how="inner")
    all_inner_head_head_2 = pd.merge(df2, df1, on=["head", "tail"], how="inner")
    
    # Swap the head and tail columns in df2 to find any tail-head matches
    df2_head_tail = df2.rename(columns={"head": "tail", "tail": "head"})
    df2_head_tail = df2_head_tail[["head","relation", "tail"]]

    # Find all the rows in df1 that match the swapped df2_head_tail rows, and all the rows in df2_head_tail that match the swapped df1 rows
    all_inner_head_tail_1 = pd.merge(df1, df2_head_tail,  how='inner', on=["head", "tail"])
    all_inner_head_tail_2 = pd.merge(df2_head_tail, df1,  how='inner', on=["head", "tail"])
    
    # Combine all the duplicates found above into a single DataFrame
    with_relation_xy = all_inner_head_head_1.append(all_inner_head_head_2).append(all_inner_head_tail_1).append(all_inner_head_tail_2)
    
    # Get all the different relations for all the entitiy combinations 
    with_relation_x = with_relation_xy[["head", "relation_x", "tail"]].dropna()
    with_relation_x.rename(columns={"relation_x":"relation"}, inplace=True)
    with_relation_y = with_relation_xy[["head", "relation_y", "tail"]].dropna()
    with_relation_y.rename(columns={"relation_y":"relation"}, inplace=True)
    # with_relation = with_relation_xy[["head", "relation", "tail"]].dropna()
    
    # Combine the separate DataFrames into a single DataFrame of all duplicates
    all_dups = with_relation_x.append(with_relation_y).sort_values(["head","relation","tail"]).drop_duplicates()
    
    # Create a DataFrame of the same duplicates as all_dups, but with the relation column removed
    all_dups_without_relation = all_dups[["head", "tail"]].drop_duplicates().sort_values("head")
    
    # Create a DataFrame with all the duplicates caused by head to head and tail to tail
    head_head_dups = all_inner_head_head_1[["head", "tail"]].drop_duplicates()    
    
    # Create a DataFrame with all the duplicates caused by head to tail and tail to head
    head_tail_dups = all_inner_head_tail_1[["tail", "head"]].drop_duplicates()
    
    
    return all_dups, all_dups_without_relation, head_head_dups, head_tail_dups

train['dup'] = train.duplicated(keep = False)
train_dup = train[train['dup'] == True]
train_dup.sort_values(by=['head', 'relation','tail'], inplace = True)

test['dup'] = test.duplicated(keep = False)
test_dup = test[test['dup'] == True]
test_dup.sort_values(by=['head', 'relation','tail'], inplace = True)

valid['dup'] = valid.duplicated(keep = False)
valid_dup = valid[valid['dup'] == True]
valid_dup.sort_values(by=['head', 'relation','tail'], inplace = True)

train_test_all, 




print(f'Train duplicates: {len(train_dup)}\nTest duplicates: {len(test_dup)}\nValid duplicates: {len(valid_dup)}')


# train_test_intersect = train.merge(test,how='inner', on=['head','tail'])

# train_valid_intersect = train.merge(valid,how='inner', on=['head','tail'])

# test_valid_intersect = test.merge(valid,how='inner', on=['head','tail'])


# train_no_dup = train.drop_duplicates()
# test_no_dup = test.drop_duplicates()
# validate_no_dup = validate.drop_duplicates()

# train_test = train_no_dup.append(test_no_dup)

# train_validate = train_no_dup.append(validate_no_dup)

# validate_test = validate_no_dup.append(test_no_dup)


# train_test_no_dup = train_test.drop_duplicates()

# train_validate_no_dup = train_validate.drop_duplicates()

# validate_test_no_dup = validate_test.drop_duplicates()

#train['dup'] = train.duplicated()

# new_train = train[train['head']=='ace']

# intersect = train.merge(test,how='inner', on=['head','tail'])


# train_dup = train[train['dup'] == True]

# train_test['dup']=train_test.duplicated()

# train_test_dup = train_test[train_test['dup']==True]

# train_test_dup.to_csv(path+'duplicates/train_test_dups.csv')

# train_dup.to_csv(path+'duplicates/train_dup.csv')





# print(len(train_test)-len(train_test_no_dup))

# print(len(train_validate)-len(train_validate_no_dup))

# print(len(validate_test)-len(validate_test_no_dup))
