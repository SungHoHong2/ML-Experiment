# /home/sungho/Downloads
import csv
import pandas as pd
import numpy as np
import os

PATH = ""
current_movie = None
with open('total_data.csv','w',newline='') as total_data:
    csv_writer = csv.writer(total_data, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    files = ['./combined_data_1.txt','./combined_data_2.txt','./combined_data_3.txt', './combined_data_4.txt']
    for file in files:
        print("reading " + file)
        with open(file) as current_file:
            for current_row in current_file:
                current_row = current_row.strip()
                if current_row[-1] == ":":
                    current_movie = current_row[:len(current_row)-1]
                else:
                    new_row = [current_movie]
                    for element in current_row.split(","):
                        new_row.append(element)
                    csv_writer.writerow(new_row)
        print("completed " + file +"\n")

