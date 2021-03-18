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
# for row in data_frame.head(10).itertuples():
#     print(row)

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

# create the similarity matrix
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

def compute_user_similarity(sparse_matrix, compute_for_few=False, top=100, verbose=False, verb_for_n_rows=20):
    no_of_users, _ = sparse_matrix.shape
    row_ind, col_ind = sparse_matrix.nonzero()
    row_ind = sorted(set(row_ind))
    time_taken = list()

    rows, cols, data = list(), list(), list()
    if verbose: print("Computing top", top, "similarities for each user..")

    start = datetime.now()
    temp = 0

    for row in row_ind[:top] if compute_for_few else row_ind:
        temp = temp + 1
        prev = datetime.now()

        sim = cosine_similarity(sparse_matrix.getrow(row), sparse_matrix).ravel()
        top_sim_ind = sim.argsort()[-top:]
        top_sim_val = sim[top_sim_ind]

        rows.extend([row] * top)
        cols.extend(top_sim_ind)
        data.extend(top_sim_val)
        time_taken.append(datetime.now().timestamp() - prev.timestamp())
        if verbose:
            if temp % verb_for_n_rows == 0:
                print("computing done for {} users [  time elapsed : {}  ]"
                      .format(temp, datetime.now() - start))

    if verbose: print('Creating Sparse matrix from the computed similarities')

    # if draw_time_taken:
    #     plt.plot(time_taken, label='time taken for each user')
    #     plt.plot(np.cumsum(time_taken), label='Total time')
    #     plt.legend(loc='best')
    #     plt.xlabel('User')
    #     plt.ylabel('Time (seconds)')
    #     plt.show()

    return sparse.csr_matrix((data, (rows, cols)), shape=(no_of_users, no_of_users)), time_taken

u_u_sim_sparse, _ = compute_user_similarity(spareMatrixTrain, compute_for_few=True, top = 100, verbose=True)



# Predict using similarity matrix

