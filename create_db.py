
# This code is for reading out the .csv files and putting them in to 1 3D Array.
# Also the defect data files, in terms of that one frame is split on multiple files, have to be repaired.

import csv
import os
import sqlite3
import time
import os.path    #1234




def read_files(data_path):
    
    start_time = time.time()

    no_frames = 10             # bigger than the actual number    #1234
    no_points = 20000           # the actual number is not fixed per frame, but smaller than 20000 in any case
    no_coordinates = 7          # x,y,z -> 3 coordinates per point
    size_threshold = 1520000    # threshold for the detection of defect frames
    #data_path ='raw_data'  # data_path of the folder with the data -> changed to parameter

    #print([name for name in os.listdir(os.getcwd()+'/'+data_path) if os.data_path.isfile(name)])    # DEBUG 1234

    #no_frames = len([name for name in os.listdir('/'+data_path) if os.data_path.isfile(name)])    #1234
    
    # use of the data type range because integer is not iterable
    Data = [[[0 for k in range(no_coordinates)] for j in range(no_points)] for i in range(no_frames)]

    # array for the timestamps of the frames
    Time = [0 for i in range(no_frames)]

    # initialization values for the loop. All 'false' or 0.
    frame_count, defect_size, defect_line_offset = 0, 0, 0
    defect_1_flag, defect_2_flag = False, False

    # loop for all files in the given directory. That directory should contain only the data.
    for filename in os.listdir(data_path):

        if os.path.isfile(os.path.join(data_path, filename)):

            # measures the size of on file
            size = os.path.getsize(os.path.join(data_path, filename))
            defect_size= defect_size + size     # summation of the size of neighbored defect frames
            if defect_size < size_threshold:
                defect_1_flag = True
                #print(filename) #DEBUG
                #print(size) #DEBUG
            else:
                defect_1_flag = False

            full_path= data_path + '/' + filename
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

    print("Finished to read in the data. Process took %3.3fs" % (time.time() - start_time))

    return [Data,Time]





def test_read_files(data_path='test_data'):
    [data_array, time_array] = read_files(data_path) #DEBUG
    print(data_array[0][3][1]) 
    print(time_array[0])
    
    

    
def create_and_fill_database(data_path):
    
    start_time = time.time()

    print('Started creating the database.')
    
    # fill the data into arrays
    [data_array, time_array] = read_files(data_path)

    # create or connect to the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    sql_command_to_drop = "DROP TABLE IF EXISTS main"
    c.execute(sql_command_to_drop)
    
    sql_command_to_create = """
                CREATE TABLE main(
                id INTEGER PRIMARY KEY,
                frame_no INTEGER,
                x REAL,
                y REAL,
                z REAL, 
                intensity REAL,
                laser_id INTEGER,
                azimuth INTEGER,
                distance_m REAL
                )""" # not used if db exists
    c.execute(sql_command_to_create)

    sql_command_to_drop = "DROP TABLE IF EXISTS time"
    c.execute(sql_command_to_drop)
    
    sql_command_to_create = """
                CREATE TABLE time(
                frame_no INTEGER PRIMARY KEY,
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

    print("Finished to create the database. Process took %0.3fs" % (time.time() - start_time))

    
    
    
def test_create_and_fill_database(db_name='data.db'):
    create_and_fill_database('test_data')
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())


