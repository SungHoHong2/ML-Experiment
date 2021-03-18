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



