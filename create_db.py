
# This code is for reading out the .csv files and putting them in to 1 3D Array.
# Also the defect data files, in terms of that one frame is split on multiple files, have to be repaired.

import csv
import os
import sqlite3
import time #1234
import os.path    #1234




def read_files(path):
    
    start_time = time.time()

    #no_frames = 10             # bigger than the actual number    #1234
    no_points = 20000           # the actual number is not fixed per frame, but smaller than 20000 in any case
    no_coordinates = 7          # x,y,z -> 3 coordinates per point
    size_threshold = 1520000    # threshold for the detection of defect frames
    #path ='raw_data'  # path of the folder with the data -> changed to parameter

    print len([name for name in os.listdir('.') if os.path.isfile(name)])    # DEBUG 1234
    no_frames = len([name for name in os.listdir('.') if os.path.isfile(name)])    #1234
    
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

            # setup for the next iteration. Depending of if defect correction is necessary.
            if defect_1_flag == True:
                defect_line_offset = defect_line_offset + line_count - 1
                #print(defect_line_offset) #DEBUG
            else:
                defect_line_offset = 0
                defect_size = 0
                frame_count += 1

    print("Finished to read in the data. Process took %3.6fs" % (time.time() - start_time), end='\n\n') #1234

    return [Data,Time]





def test_read_files():
    [data_array, time_array] = read_files() #DEBUG
    print(data_array[0][3][1]) 
    print(time_array[0])
    
    

    
def create_and_fill_database(path):
    
    start_time = time.time()

    print('Started creating the database.')
    
    # fill the data into arrays
    [data_array, time_array] = read_files(path)

    # create or connect to the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    sql_command_to_drop = "DROP TABLE IF EXISTS main"    #1234
    c.execute(sql_command_to_drop)    #1234
    
    sql_command_to_create = """
                CREATE TABLE main(
                id INTEGER PRIMARY KEY,
                frame_no INTEGER,
                x REAL,
                y REAL,
                z REAL, 
                intensity REAL,
                laser_id REAL,
                azimuth REAL,
                distance_m REAL
                )""" # not used if db exists
    c.execute(sql_command_to_create)

    sql_command_to_drop = "DROP TABLE IF EXISTS time"    #1234
    c.execute(sql_command_to_drop)    #1234
    
    sql_command_to_create = """
                CREATE TABLE time(
                frame_no INTEGER,
                timestamp REAL
                )""" # not used if db exists
    c.execute(sql_command_to_create)

    conn.commit()

    no_frames = len(data_array)
    no_points_per_frame = len(data_array[0])   
    # len(data_array[0][0]) => no_coordinates
    
    point_id = 0
    for i_f in range(no_frames): # i_f: index for frames
        for i_ppf in range(no_points_per_frame): # i_ppf: index for points per frame
            if data_array[i_f][i_ppf][0] != 0.0:

                sql_command_to_fill = 'INSERT INTO main VALUES('
                sql_command_to_fill += str(point_id) + ','
                sql_command_to_fill += str(i_f) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ','
                sql_command_to_fill += str(data_array[i_f][i_ppf][0]) + ')'

                c.execute(sql_command_to_fill)
                point_id = point_id + 1
            
        if data_array[i_f][0][0] != 0.0:

            sql_command_to_fill = 'INSERT INTO time VALUES('
            sql_command_to_fill += str(i_f) + ','
            sql_command_to_fill += str(time_array[i_f]) + ')'

            c.execute(sql_command_to_fill)

    conn.commit()
    conn.close()

    print("Finished to create the database. Process took %0.6fs" % (timeit.timeit() - start_time))
    print('Finished to create the database. Process took {:0.6f}s'.format(ende-start), end='\n\n') #1234
    
    
    
def test_create_and_fill_database():
    create_and_fill_database('test_data')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())

test_create_and_fill_database()
