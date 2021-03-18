# /home/sungho/Downloads
import csv
import pandas as pd
import numpy as np
import os

PATH = "/home/sungho/Downloads/"
current_movie = None

# construct a total_data.csv (need to run only once)
# with open(PATH+'total_data.csv','w',newline='') as total_data:
#     csv_writer = csv.writer(total_data, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#     files = [PATH+'combined_data_1.txt',PATH+'combined_data_2.txt',PATH+'combined_data_3.txt', PATH+'combined_data_4.txt']
#     for file in files:
#         print("reading " + file)
#         with open(file) as current_file:
#             for current_row in current_file:
#                 current_row = current_row.strip()
#                 if current_row[-1] == ":":
#                     current_movie = current_row[:len(current_row)-1]
#                 else:
#                     new_row = [current_movie]
#                     for element in current_row.split(","):
#                         new_row.append(element)
#                     csv_writer.writerow(new_row)
#         print("completed " + file +"\n")

data_frame = pd.read_csv(PATH+'/total_data.csv', sep=',', names=['movieId', 'userId','currentRating','date'])
data_frame.date = pd.to_datetime(data_frame.date)
data_frame.sort_values(by='date', inplace=True)

# print out the top 10 rows of the data
for row in data_frame.head(10).itertuples():
    print(row)

# split the data into training and test data
data_frame.iloc[:int(data_frame.shape[0]*0.80)].to_csv(PATH+"train.csv", index=False)
train_data = pd.read_csv(PATH+"train.csv", parse_dates=['date'])
data_frame.iloc[int(data_frame.shape[0]*0.80):].to_csv(PATH+"test.csv", index=False)
test_data = pd.read_csv(PATH+"test.csv")

print("Total Train Data:")
print("Total number of movie ratings in train data = "+str(train_data.shape[0]))
print("Number of unique users in train data = "+str(len(np.unique(train_data["userId"]))))
print("Number of unique movies in train data = "+str(len(np.unique(train_data["movieId"]))))
print("Highest value of a User ID = "+str(max(train_data["userId"].values)))
print("Highest value of a Movie ID = "+str(max(train_data["movieId"].values)))

# create the spares matrix
from scipy import sparse
from scipy.sparse import csr_matrix
spareMatrixTrain = sparse.csr_matrix((train_data.currentRating.values, (train_data.userId.values,train_data.movieId.values)),)
sparse.save_npz(PATH+"spareMatrixTrain.npz", spareMatrixTrain)
us,mv = spareMatrixTrain.shape
elem = spareMatrixTrain.count_nonzero()
print("Sparsity Of Training matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )
sparseMatrixTest = sparse.csr_matrix((test_data.currentRating.values, (test_data.userId.values,test_data.movieId.values)))
sparse.save_npz("sparseMatrixTest.npz", sparseMatrixTest)
us,mv = sparseMatrixTest.shape
elem = sparseMatrixTest.count_nonzero()
print("Sparsity of Testing matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )


