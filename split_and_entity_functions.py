# -*- coding: utf-8 -*-
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
    import pandas as pd
    moved_pairs = set()
    split_dataframe = set()
    pharm_kg_no_relation = dataframe[['head','tail']]
    pharm_kg_list = list(pharm_kg_no_relation.itertuples(index=False, name=None))
    i = - 1
    for ind in dataframe.index:
        i = i+1
        if i%1000 == 0:
            print(f'{i} out of {split_size} done')
        head_tail = (dataframe.iat[ind,0],dataframe.iat[ind,2])
        head_relation_tail = (dataframe.iat[ind,0],dataframe.iat[ind,1],dataframe.iat[ind,2])
        tail_head = (dataframe.iat[ind,2],dataframe.iat[ind,0])
        if head_tail in moved_pairs or tail_head in moved_pairs:
            continue
        split_dataframe.add(head_relation_tail)
        moved_pairs.add(head_tail)
        moved_pairs.add(tail_head)
        indexes = [index for index, value in enumerate(pharm_kg_list) if value == head_tail]
        for index in indexes:
            split_dataframe.add((dataframe.iat[index,0],dataframe.iat[index,1],dataframe.iat[index,2]))
        indexes = [index for index, value in enumerate(pharm_kg_list) if value == tail_head]
        for index in indexes:
            split_dataframe.add((dataframe.iat[index,0],dataframe.iat[index,1],dataframe.iat[index,2]))
        if len(split_dataframe) >= split_size:
            break
    df = pd.DataFrame(split_dataframe, columns =['head', 'relation', 'tail'])
    return df

def get_diff_between_entity_lists(df1,df2):
    df1_head = set(df1["head"])
    df1_tail = set(df1["tail"])
    entities_df1 = df1_head.union(df1_tail)
    df2_head = set(df2["head"])
    df2_tail = set(df2["tail"])
    entities_df2 = df2_head.union(df2_tail)
    print()
    return entities_df1-entities_df2

def find_rows_to_move(from_df,to_df,entities):
    head = from_df['head']
    tail = from_df['tail']
    index_list = []
    i=-1
    for value in head:
        i = i+1
        if value in entities:
            index_list.append(i)
    i = -1
    for value in tail:
        i = i+1
        if value in entities:
            index_list.append(i)
    index_list=list(dict.fromkeys(index_list))
    return index_list

def move_rows(from_df, to_df, index_to_move):
    import pandas as pd
    for index in index_to_move:
        if index in from_df.index:
            # Get the row from from_df
            row_to_move = from_df.loc[index]

            # Remove the row from from_df
            from_df = from_df.drop(index)

            # Add the row to to_df
            to_df = pd.concat([to_df, row_to_move.to_frame().T])

    # Reset the index of to_df
    to_df = to_df.reset_index(drop=True)

    return from_df, to_df

def can_be_moved_pharm(train_P):
    import pandas as pd
    #getting train without relation
    train_P_without_relation = train_P[["head", "tail"]]
    #swapping around the head and tial of train without relation
    train_tail_head_without_relation = train_P_without_relation.rename(columns = {"head":"tail", "tail":"head"})
    train_tail_head_without_relation = train_tail_head_without_relation[["head", "tail"]]
    #deleting all that train and train head tial swaped have in commen, so that what is left only is the entity combinationes that have one occurrences 
    inner_train_P_x_train_tail_head = pd.concat([train_tail_head_without_relation, train_P_without_relation], join="outer").drop_duplicates(keep = False)
    #finding the intercestion between all the edges that are unique combination and the original train. 
    #what is left is all unique edge, that can be moved without causing overlaps between train, test and valid, since they are unique. 
    can_be_moved = pd.merge(inner_train_P_x_train_tail_head, train_P, on=("head","tail"), how = "inner")
    can_be_moved = can_be_moved[["head","relation","tail"]]
    return can_be_moved

def count_values(lst):
    from collections import Counter
    count_dict = Counter(lst)
    count_dict = dict(count_dict)
    return count_dict

def finding_can_be_moved(train, number_to_be_moved, can_be_moved_edges_train):
    import pandas as pd
    print(f'Moving {number_to_be_moved} edges out of {len(can_be_moved_edges_train)} possible edges')
    train_entites = list(train['head'].append(train['tail']))
    entity_Count = count_values(train_entites)
    
    entity_count_df = pd.DataFrame(entity_Count.items(), columns=['entity', 'count'])
    
    entity_count_df = entity_count_df.sort_values(by = 'count', ascending = False).reset_index(drop = True)
    
    entity_count_df = entity_count_df[entity_count_df['count'] > 1]
    
    can_be_moved = pd.DataFrame(columns = ['head','relation','tail'])
    for index in can_be_moved_edges_train.index: 
        if index% 100 == 0: 
            print(f'Done with {index} out of {number_to_be_moved}')
        if can_be_moved_edges_train.iat[index,0] in list(entity_count_df['entity']) and can_be_moved_edges_train.iat[index,2] in list(entity_count_df['entity']):
            # Retrieve the row index where the first value and second value is found
            row_index_1 = entity_count_df[entity_count_df['entity'] == can_be_moved_edges_train.iat[index, 0]].index[0]
            row_index_2 = entity_count_df[entity_count_df['entity'] == can_be_moved_edges_train.iat[index, 2]].index[0]
            # Decrement the count for the first entity and second entity
            entity_count_df.at[row_index_1, 'count'] -= 1
            entity_count_df.at[row_index_2, 'count'] -= 1
            entity_count_df = entity_count_df[entity_count_df['count'] > 1]
            can_be_moved = can_be_moved.append(can_be_moved_edges_train.iloc[index])
            if len(can_be_moved) >= number_to_be_moved:
                break
    return can_be_moved

def make_transductive(train,test,valid):
    import pandas as pd
    #Move from test to train
    diff_entities = get_diff_between_entity_lists(test,train)
    rows_to_move = find_rows_to_move(test,train,diff_entities)
    almost_test, almost_train = move_rows(test, train, rows_to_move)
    amount_to_move = len(rows_to_move)
    #Find rows in train which can be moved back (Only return edges which can't cause data leakage)
    can_be_moved = can_be_moved_pharm(train)
    #Move from train to test
    to_move = finding_can_be_moved(almost_train, amount_to_move, can_be_moved)
    new_test = pd.concat([almost_test, to_move], join="outer").reset_index(drop = True)
    new_train = pd.concat([almost_train, to_move], join="outer").drop_duplicates(keep=False).reset_index(drop = True)
    #Move from valid to train
    diff_entities = get_diff_between_entity_lists(valid,new_train)
    rows_to_move = find_rows_to_move(valid,new_train,diff_entities)
    almost_valid, almost_train = move_rows(valid, new_train, rows_to_move)
    amount_to_move = len(rows_to_move)
    #Move from train to valid
    can_be_moved = pd.concat([can_be_moved, to_move], join = "outer").drop_duplicates(keep=False).reset_index(drop = True)
    to_move = finding_can_be_moved(almost_train, amount_to_move, can_be_moved)
    new_valid = pd.concat([almost_valid, to_move], join="outer").reset_index(drop = True)
    new_train = pd.concat([almost_train, to_move], join="outer").drop_duplicates(keep=False).reset_index(drop = True)
    return new_train,new_test,new_valid


def check_entity_overlap(train,test,valid):
    train_head = set(train["head"])
    train_tail = set(train["tail"])
    all_train = train_head.union(train_tail)
    test_head = set(test["head"])
    test_tail = set(test["tail"])
    all_test = test_head.union(test_tail)
    valid_head = set(valid["head"])
    valid_tail = set(valid["tail"])
    all_valid = valid_head.union(valid_tail)
    if all_train.issuperset(all_test) == True:
        print('All test entities are in train')
    else:
        print('All test entities are NOT in train')
        diff = len(all_test-all_train)
        print(f'There are {diff} entities in test, that are NOT in train')
    if all_train.issuperset(all_valid) == True:
        print('All valid entities are in train')
    else:
        print('All valid entities are NOT in train')
        diff = len(all_valid-all_train)
        print(f'There are {diff} entities in valid, that are NOT in train')

def check_edge_overlap(train,test,valid):
    train.reset_index(drop = True, inplace = True)
    test.reset_index(drop = True, inplace = True)
    valid.reset_index(drop = True, inplace = True)
    train_edges_head_head = set()
    for index in train.index:
        train_head_tail = (train.iat[index,0],train.iat[index,2])
        train_edges_head_head.add(train_head_tail)
        
    test_edges_head_head = set()
    test_edges_head_tail = set()
    for index in test.index:
        test_head_tail = (test.iat[index,0],test.iat[index,2])
        test_tail_head = (test.iat[index,2],test.iat[index,0])
        test_edges_head_head.add(test_head_tail)
        test_edges_head_tail.add(test_tail_head)
        
    valid_edges_head_head = set()
    valid_edges_head_tail = set()
    for index in valid.index:
        valid_head_tail = (valid.iat[index,0],valid.iat[index,2])
        valid_tail_head = (valid.iat[index,2],valid.iat[index,0])
        valid_edges_head_head.add(valid_head_tail)
        valid_edges_head_tail.add(valid_tail_head)
        
    train_test_intersect_head_head = len(train_edges_head_head.intersection(test_edges_head_head))
    train_test_intersect_head_tail = len(train_edges_head_head.intersection(test_edges_head_tail))
    train_valid_intersect_head_head = len(train_edges_head_head.intersection(valid_edges_head_head))
    train_valid_intersect_head_tail = len(train_edges_head_head.intersection(valid_edges_head_tail))
    valid_test_intersect_head_head = len(valid_edges_head_head.intersection(test_edges_head_head))
    valid_test_intersect_head_tail = len(valid_edges_head_head.intersection(test_edges_head_tail))
    print(f'TRAIN - TEST: head, tail to head, tail intersects: {train_test_intersect_head_head}')
    print(f'TRAIN - TEST: head, tail to tail, head intersects: {train_test_intersect_head_tail}')
    print(f'TRAIN - VALID: head, tail to head, tail intersects: {train_valid_intersect_head_head}')
    print(f'TRAIN - VALID: head, tail to tail, head intersects: {train_valid_intersect_head_tail}')
    print(f'VALID - TEST: head, tail to head, tail intersects: {valid_test_intersect_head_head}')
    print(f'VALID - TEST: head, tail to tail, head intersects: {valid_test_intersect_head_tail}')

