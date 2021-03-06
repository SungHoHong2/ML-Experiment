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
#     files = [PATH+'combined_data_1.txt']
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

# create the sparse matrix
from scipy import sparse
from scipy.sparse import csr_matrix
spareMatrixTrain = sparse.csr_matrix((train_data.currentRating.values, (train_data.userId.values,train_data.movieId.values)),)
sparse.save_npz(PATH+"sparseMatrixTrain.npz", spareMatrixTrain)
us,mv = spareMatrixTrain.shape
elem = spareMatrixTrain.count_nonzero()
print("Sparsity Of Training matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )
sparseMatrixTest = sparse.csr_matrix((test_data.currentRating.values, (test_data.userId.values,test_data.movieId.values)))
sparse.save_npz(PATH+"sparseMatrixTest.npz", sparseMatrixTest)
us,mv = sparseMatrixTest.shape
elem = sparseMatrixTest.count_nonzero()
print("Sparsity of Testing matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from datetime import datetime

# Computing User-User Similarity matrix
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
    return sparse.csr_matrix((data, (rows, cols)), shape=(no_of_users, no_of_users)), time_taken

u_u_sim_sparse, _ = compute_user_similarity(spareMatrixTrain, compute_for_few=True, top = 100, verbose=True)
sparse.save_npz(PATH+"u_u_sim_sparse.npz", u_u_sim_sparse)
u_u_sim_sparse = sparse.load_npz(PATH+"u_u_sim_sparse.npz")
print('u_u_sim_sparse shape', u_u_sim_sparse.shape)

# Computing Movie-Movie Similarity matrix
m_m_sim_sparse = cosine_similarity(spareMatrixTrain.T, dense_output=False)
sparse.save_npz(PATH+"m_m_sim_sparse.npz", m_m_sim_sparse)
m_m_sim_sparse = sparse.load_npz(PATH+"m_m_sim_sparse.npz")
print('m_m_sim_sparse shape', m_m_sim_sparse.shape)

# Finding most similar movies using similarity matrix
# movie_ids = np.unique(m_m_sim_sparse.nonzero()[1])
# similar_movies = dict()
# for movie in movie_ids:
#     sim_movies = m_m_sim_sparse[movie].toarray().ravel().argsort()[::-1][1:]
#     similar_movies[movie] = sim_movies[:100]
# testing simlilar movies for movie 20
# print(similar_movies[20])

# example predicting similar movies id =40
movie_titles = pd.read_csv(PATH+"movie_titles.csv", sep=',', header = None,
                           names=['movie_id', 'year_of_release', 'title'], verbose=True,
                      index_col = 'movie_id', encoding = "ISO-8859-1")
mv_id = 40
print("\nMovie ----->",movie_titles.loc[mv_id].values[1])
print("\nIt has {} Ratings.".format(spareMatrixTrain[:,mv_id].getnnz()))
print("\nWe have {} movies which are similar to this movie".format(m_m_sim_sparse[:,mv_id].getnnz()))
