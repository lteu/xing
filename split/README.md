Extract relevant information
===
- split_items.py split active and disactive items
- split_impressions.py separates impressions by week from total impressions, and saves it in 'impression/weekxxx.csv'
- split_interactions.py similar to previous
- refine_impression_duplication.py removes duplicated items, and aggregate impressions of 40,41,42,43 weeks into the file 'week-40-41-42-43c.csv'
- refine_interactions.py separates interactions of target users from total users. And it save these information into file interaction/weekxxxb.csv
- refine_split_impression.py separates impressions of target users from total users. And it save these information into file impression/weekxxxb.csv
- split_users.py creates file with target users and their profiles.


SVM RANK TEST FILE
====
- svmran_testset.py generates testset for svm rank, in the same time it produces also a json file for feature mapping.
- subtract_target_user_withimpressions.py randomly generates generate k target users who have logs on both interactions and impressions. Users are saved in 'target_users_k.csv'
- subtract_target_users.py randomly generates k target users