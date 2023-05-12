
# A better split of PharmKG8k

In this GitHub repository an improved split of the PharmKG8k dataset can be found. In the original split found on their [GitHub repository](https://github.com/biomed-AI/PharmKG) several issues exists.

## Issues in the original split

These issues consists of:
1. Duplicates in each individual set, train, test and valid.
2. head, relation, tail combinations existing in both e.g. train and test.
3. head, tail combinations existing in both e.g. train and test.
4. tail, head combinations in e.g. train existing as head, tail in e.g. test.
Proof of these issues can be found in [proof_of_bad_split](https://github.com/skingi20/improvement_of_PharmKG8k_split/tree/main/proof_of_bad_split), and the code to generate these files can be found in *investigation_of_duplicates_in_pharmkg8k.py*

## The better split
This new split have some different goals in mind when creating it. These can be expressed as a math equation. The denotions we use are as mentioned:

$$(h,r,t) = (head,relation,tail)$$

$$P_{tr} = train$$

$$P_{ts} = test$$

$$P_{va} = valid$$

Then the rules can be expressed as such:

$$\forall (h,r,t) \in P_{tr} : \neg(\exists (h',t') \in (P_{ts} \cup P_{va}) : \\
((h = h' \land t = t') \lor (h = t' \land t = h')))$$

*and*

$$\forall (h,r,t) \in P_{ts} : \neg(\exists (h',t') \in (P_{tr} \cup P_{va}) : \\
((h = h' \land t = t') \lor (h = t' \land t = h')))$$

*and*

$$\forall (h,r,t) \in P_{va} : \neg(\exists (h',t') \in (P_{tr} \cup P_{ts}) : \\
((h = h' \land t = t') \lor (h = t' \land t = h')))$$

In other words, the new split is created such that for all edges in the training set there does not exist an edge in either the test set nor the valid set, where the head and the tail is equivalent to the head and the tail in the training set. Nor does there exist edges where the head and tail is equivalent to the tail and head in the training set.
Vice versa for the test and valid sets.

This split can be found in [improved_split](https://github.com/skingi20/improvement_of_PharmKG8k_split/tree/main/improved_split) and the code to generate these can be found in *making_the_split_files.py*. It should be noted that this code is not optimized so it may take several hours to run.