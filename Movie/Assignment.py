# /home/sungho/Downloads
import csv
import pandas as pd
import numpy as np
import os

PATH = "/home/sungho/Downloads/"

# # create the sparse matrix
from scipy import sparse
from scipy.sparse import csr_matrix

### TODO: Sungho, Yiting BEGIN

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from datetime import datetime

sparseMatrixTrain = u_u_sim_sparse = sparse.load_npz(PATH+"spareMatrixTrain.npz")
sparseMatrixTest = u_u_sim_sparse = sparse.load_npz(PATH+"sparseMatrixTest.npz")
us,mv = sparseMatrixTrain.shape
elem = sparseMatrixTrain.count_nonzero()
print("Sparsity of Training matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )
us,mv = sparseMatrixTest.shape
elem = sparseMatrixTest.count_nonzero()
print("Sparsity of Testing matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )

# Computing User-User Similarity matrix
# def compute_user_similarity(sparse_matrix, compute_for_few=False, top=100, verbose=False, verb_for_n_rows=20):
#     no_of_users, _ = sparse_matrix.shape
#     row_ind, col_ind = sparse_matrix.nonzero()
#     row_ind = sorted(set(row_ind))
#     time_taken = list()
#
#     rows, cols, data = list(), list(), list()
#     if verbose: print("Computing top", top, "similarities for each user..")
#
#     start = datetime.now()
#     temp = 0
#
#     for row in row_ind[:top] if compute_for_few else row_ind:
#         temp = temp + 1
#         prev = datetime.now()
#
#         sim = cosine_similarity(sparse_matrix.getrow(row), sparse_matrix).ravel()
#         top_sim_ind = sim.argsort()[-top:]
#         top_sim_val = sim[top_sim_ind]
#
#         rows.extend([row] * top)
#         cols.extend(top_sim_ind)
#         data.extend(top_sim_val)
#         time_taken.append(datetime.now().timestamp() - prev.timestamp())
#         if verbose:
#             if temp % verb_for_n_rows == 0:
#                 print("computing done for {} users [  time elapsed : {}  ]"
#                       .format(temp, datetime.now() - start))
#
#     if verbose: print('Creating Sparse matrix from the computed similarities')
#     return sparse.csr_matrix((data, (rows, cols)), shape=(no_of_users, no_of_users)), time_taken



no_of_users, _ = sparseMatrixTrain.shape
row_ind, col_ind = sparseMatrixTrain.nonzero()
row_ind = sorted(set(row_ind))
top = 100

rows, cols, data = list(), list(), list()
print("Computing top", top, "similarities for each user..")

temp = 0
for row in row_ind[:top]:
    temp = temp + 1
    sim = cosine_similarity(sparseMatrixTrain.getrow(row), sparseMatrixTrain).ravel()
    top_sim_ind = sim.argsort()[-top:]
    top_sim_val = sim[top_sim_ind]
    rows.extend([row] * top)
    cols.extend(top_sim_ind)
    data.extend(top_sim_val)
    if temp % 20 == 0:
        print("computing done for "+str(temp)+" users")

print('Creating Sparse matrix from the computed similarities')
u_u_sim_sparse = sparse.csr_matrix((data, (rows, cols)), shape=(no_of_users, no_of_users))

# u_u_sim_sparse, _ = compute_user_similarity(sparseMatrixTrain, compute_for_few=True, top = 100, verbose=True)
sparse.save_npz(PATH+"u_u_sim_sparse.npz", u_u_sim_sparse)
u_u_sim_sparse = sparse.load_npz(PATH+"u_u_sim_sparse.npz")
print('u_u_sim_sparse shape', u_u_sim_sparse.shape)

# Computing Movie-Movie Similarity matrix
m_m_sim_sparse = cosine_similarity(sparseMatrixTrain.T, dense_output=False)
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
print("\nIt has {} Ratings.".format(sparseMatrixTrain[:,mv_id].getnnz()))
print("\nWe have {} movies which are similar to this movie".format(m_m_sim_sparse[:,mv_id].getnnz()))

### TODO: Sungho, Yiting END
