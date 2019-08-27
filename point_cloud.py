import init
import math

def find_point_clouds():
    KEY = 9
    value = 0
    # connect to the database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for f in range(init.no_frames)
        c.execute("SELECT * FROM moving WHERE frame_no=:i_frame",{'i_frame': f})
        data_array = c.fetchall()

        obj_counter = 0

        for i in range(len(data_array)):
            if data_array[i][KEY] == "NULL":
                data_array[i][KEY] = obj_counter
                obj_key = data_array[i][KEY]
                obj_counter = obj_counter + 1
            else:
                obj_key = data_array[i][KEY]
            
            for j in range(len(data_array)-i):
                x1=data_array[i][2]
                x2=data_array[i+j][2]
                y1=data_array[i][3]
                y2=data_array[i+j][3]
                z1=data_array[i][4]
                z2=data_array[i+j][4]

                # 3 dim Pythagoras
                s = math.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )

                if s <= init.cloud_tol:
                    if data_array[i+j][KEY] == "NULL":
                        data_array[i+j][KEY] = obj_key
                    else:
                        obj_key_wrong = obj_key
                        obj_key = data_array[i+j][KEY]
                        for p in range(i+j):
                            if data_array[p][KEY] == obj_key_wrong:
                                data_array[p][KEY] = obj_key
        
        for i in range(len(data_array)):
            c.execute("UPDATE moving SET object_no=:i_obj WHERE id=:i_id"
                        , {"i_obj": data_array[i][KEY], "i_id": i})

        conn.commit()

def sort_clouds():
    exit
# the frames have to be sticked togehter

def find_focus():
    exit


# def all the test functions


