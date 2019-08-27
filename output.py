import sqlite3
import time
import create_db
import init



def print_table(table_name, db_name=init.db_name):
    start_time = time.time()

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sql_command_to_select = "SELECT * FROM " + table_name
    c.execute(sql_command_to_select)
    array=c.fetchall()
    print(array)
    print("Finished to print the table. Process took %0.3fs" % (time.time() - start_time))



def test_print_table(db_name='data.db', table_name='time'):
    print('test function')
    print_table(db_name, table_name)



def print_get(db_name, table_name):
    start_time = time.time()

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sql_command_to_select = "SELECT * FROM " + table_name
    c.execute(sql_command_to_select)
    array=c.fetchall()

    print("Finished to get the table. Process took %0.3fs" % (time.time() - start_time))



def test_get_table(db_name='data.db', table_name='time'):
    print('test function')
    print_table(db_name, table_name)

#def get_table(table_name):

#def visualize_frame(frame_no, source_table):
