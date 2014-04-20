ExtractDataset
==============

Extract Dataset Metadata from Literatures

PaperToText.py: convert pdf to txt, and tokenize converted texts.
Position.py: extract dataset description texts from article refined texts.
ExtractWords.py: generate word-freq map, and sort in desc order.
BuildFeatures.py: get top-500 words as features, each word has two entry: freq and avg dist. Thus, there are total 1000 features for each dataset. Then generate a feature vector for each dataset name. For each sentence contains dataset, consider it with its next sentence as context to extract features to avoid sparsity.
