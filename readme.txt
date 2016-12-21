

Items
====
1 career level
2 employment
? discipline_id
? title
? industry_id
? country
? region
? tags

Details about the job postings that were and should be recommended to the users.

id anonymized ID of the item (referenced as item_id in the other datasets above)
title concepts that have been extracted from the job title of the job posting (numeric IDs)
career_level career level ID (e.g. beginner, experienced, manager):
0 = unknown
1 = Student/Intern
2 = Entry Level (Beginner)
3 = Professional/Experienced
4 = Manager (Manager/Supervisor)
5 = Executive (VP, SVP, etc.)
6 = Senior Executive (CEO, CFO, President)
discipline_id anonymized IDs represent disciplines such as "Consulting", "HR", etc.
industry_id anonymized IDs represent industries such as "Internet", "Automotive", "Finance", etc.
country code of the country in which the job is offered
region is specified for some users who have as country de. Meaning of the regions: see below.
latitude latitude information (rounded to ca. 10km)
longitude longitude information (rounded to ca. 10km)
employment the type of employment:
0 = unknown
1 = full-time
2 = part-time
3 = freelancer
4 = intern
5 = voluntary
tags concepts that have been extracted from the tags, skills or company name
created_at a Unix time stamp timestamp representing the time when the interaction got created
active_during_test is 1 if the item is still active (= recommendable) during the test period and 0 if the item is not active anymore in the test period (= not recommendable)