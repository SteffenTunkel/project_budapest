
# This code is for reading out the .csv files and putting them in to 1 3D Array.
# Also the defect data files, in terms of that one frame is split on multiple files, have to be repaired.

import csv
import os
import sqlite3

def read_files():
    no_frames = 700             # bigger than the actual number
    no_points = 20000           # the actual number is not fixed per frame, but smaller than 20000 in any case
    no_coordinates = 7          # x,y,z -> 3 coordinates per point
    size_threshold = 1520000    # threshold for the detection of defect frames
    path ='raw_data'  # path of the folder with the data

    # use of the data type range because integer is not iterable
    Data = [[[0 for k in range(no_coordinates)] for j in range(no_points)] for i in range(no_frames)]

    # array for the timestamps of the frames
    Time = [0 for i in range(no_frames)]

    # initialization values for the loop. All 'false' or 0.
    frame_count, defect_size, defect_line_offset = 0, 0, 0
    defect_1_flag, defect_2_flag = False, False

    # loop for all files in the given directory. That directory should contain only the data.
    for filename in os.listdir(path):

        if os.path.isfile(os.path.join(path, filename)):

            # measures the size of on file
            size = os.path.getsize(os.path.join(path, filename))
            defect_size= defect_size + size     # summation of the size of neighbored defect frames
            if defect_size < size_threshold:
                defect_1_flag = True
                #print(filename) #DEBUG
                #print(size) #DEBUG
            else:
                defect_1_flag = False

            full_path= path + '/' + filename
            with open(full_path) as csv_file:

                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    # first line is different (header)
                    if line_count == 0:
                        line_count += 1
                    else:
                        # filling the timestamp array
                        if line_count == 1:
                            Time[frame_count] = float(row[7])

                        # filling the data array
                        Data[frame_count][line_count+defect_line_offset-1][0]=float(row[0])
                        Data[frame_count][line_count+defect_line_offset-1][1]=float(row[1])
                        Data[frame_count][line_count+defect_line_offset-1][2]=float(row[2])
                        Data[frame_count][line_count+defect_line_offset-1][3]=float(row[3])
                        Data[frame_count][line_count+defect_line_offset-1][4]=float(row[4])
                        Data[frame_count][line_count+defect_line_offset-1][5]=float(row[5])
                        Data[frame_count][line_count+defect_line_offset-1][6]=float(row[6])

                        line_count += 1

            #print(Data[0][3][1]) #DEBUG

            # setup for the next iteration. Depending of if defect correction is necessary.
            if defect_1_flag == True:
                defect_line_offset = defect_line_offset + line_count - 1
                #print(defect_line_offset) #DEBUG
            else:
                defect_line_offset = 0
                defect_size = 0
                frame_count += 1

    print('Finish to read in the data.')

    return [Data,Time]

# program test for DEBUG
#[input_array, time_array] = read_files() #DEBUG
#print(input_array[0][3][1]) #DEBUG
#print(time_array[0]) #DEBUG


conn = sqlite3.connect('data.db')
c = conn.cursor()

sql_command_to_create = """
            CREATE TABLE raw(
            id INTEGER PRIMARY KEY,
            x REAL,
            y REAL,
            z REAL, 
            intensity REAL,
            laser_id REAL,
            azimuth REAL,
            distance_m REAL,
            timestamp REAL
            )""" # not used if db exists
# c.execute(sql_command_to_create)

#sql_command_to_fill = """
#            INSERT INTO raw VALUES("""
#c.execute(sql_command)

conn.commit()
conn.close()

