output.py
Gestern
Mo. 23:10
S
Sie haben ein Element bearbeitet
Text
output.py
Letzten Monat
27. Sept.
S
Sie haben ein Element hochgeladen
Text
output.py

import sqlite3
import time
import create_db
import init

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D




def print_table(table_name, db_name=init.db_name):
    start_time = time.time()

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sql_command_to_select = "SELECT * FROM " + table_name
    c.execute(sql_command_to_select)
    array=c.fetchall()
    print(array)
    print("Finished to print the table. Process took %0.3fs" % (time.time() - start_time))



def test_print_table(table_name='time', db_name='data.db'):
    print('testing: print_table')
    print_table(table_name, db_name)



def get_table(table_name, db_name=init.db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sql_command_to_select = "SELECT * FROM " + table_name
    c.execute(sql_command_to_select)
    array=c.fetchall()

    return array




def test_get_table(table_name='time', db_name='data.db'):
    print('testing: get_table')
    start_time = time.time()
    array = get_table(table_name, db_name)
    print(array)
    print("Finished to get the table. Process took %0.3fs" % (time.time() - start_time))



def visualize_frame_from_db(frame_no, source_table):
    conn = sqlite3.connect(init.db_name)
    c = conn.cursor()
    data_array = []
    # comprise multiple frames for better results
    for i in range(init.frame_comprise):
        # get data from 'moving' table for each frame
        c.execute("SELECT * FROM moving WHERE frame_no=:i_frame",{'i_frame': frame_no+i})
        data_array += c.fetchall()

    frame=np.asarray(data_array)
    x = frame[:,2]
    y = frame[:,3]
    z = frame[:,4]
    print(frame[1,:]) #DEBUG


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=x, ys=y, zs=0, zdir='z', s=20, c=None, depthshade=True)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()



    
def test_visualize_frame_from_db(frame_no = 1, source_table='moving'):
    print('testing: visualize_frame')
    start_time = time.time()
    visualize_frame_from_db(frame_no, source_table)
    print("Finished. Process took %0.3fs" % (time.time() - start_time))		
