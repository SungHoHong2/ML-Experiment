#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "rb"))

print('number of people: ', len(enron_data.keys()))

ans = list(enron_data.values())
print('number of features: ', len(ans[0]))

ans = 0
for person, features in enron_data.items():

    if person == 'PRENTICE JAMES':
        print('here?')
    # print(person, features)
    if features['poi'] == 1 :
        ans += 1
print('number of pois: ',ans)



