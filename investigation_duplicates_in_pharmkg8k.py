# -*- coding: utf-8 -*-
import pandas as pd

base_url = 'https://raw.githubusercontent.com/biomed-AI/PharmKG/master/data/PharmKG-8k/'

train = pd.read_table(base_url+'train.tsv', names=["head", "relation", "tail"])
test = pd.read_table(base_url+'test.tsv', names=["head", "relation", "tail"])
valid = pd.read_table(base_url+'valid.tsv', names=["head", "relation", "tail"])

train['dup'] = train.duplicated(keep = True)
train_dup = train[train['dup'] == True]

test['dup'] = test.duplicated(keep = True)
test_dup = test[test['dup'] == True]

valid['dup'] = valid.duplicated(keep = True)
valid_dup = valid[valid['dup'] == True]

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

new_train = train[train['head']=='ace']

intersect = train.merge(test,how='inner', on=['head','tail'])


# train_dup = train[train['dup'] == True]

# train_test['dup']=train_test.duplicated()

# train_test_dup = train_test[train_test['dup']==True]

# train_test_dup.to_csv(path+'duplicates/train_test_dups.csv')

# train_dup.to_csv(path+'duplicates/train_dup.csv')





# print(len(train_test)-len(train_test_no_dup))

# print(len(train_validate)-len(train_validate_no_dup))

# print(len(validate_test)-len(validate_test_no_dup))
