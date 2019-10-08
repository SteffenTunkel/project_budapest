import init
import math
import sqlite3
import output
import numpy as np
import time

def find_point_clouds(db_name):
	tot_time = time.time() #DEBUG	


	# connect to the database
	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	# "for each frame"
	for f in range(init.no_frames):
    		
		# get data from 'moving' table for each frame
		c.execute("SELECT * FROM moving WHERE frame_no=:i_frame",{'i_frame': f})
		data_array = c.fetchall()
		
		# check that the frame actually exists
		if data_array != []:
			
			obj_counter = 0
			temp_array = np.asarray(data_array)
			id_array = temp_array[:,0]
			key_array = np.zeros(len(data_array))
			for i in range(len(data_array)):
				if key_array[i] == 0:
					obj_counter = obj_counter + 1
					key_array[i] = obj_counter					
					obj_key = key_array[i]					
				else:
					obj_key = key_array[i]


				for j in range(len(data_array)-i):
					
					# calculate the distance between two points
					x1=data_array[i][2]
					x2=data_array[i+j][2]
					y1=data_array[i][3]
					y2=data_array[i+j][3]
					z1=data_array[i][4]
					z2=data_array[i+j][4]
					# 3 dim Pythagoras
					s = math.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )

					# if the distance is lower than tolerance, put give them the same number
					if s <= init.cloud_tol:
						if key_array[i+j] == 0:
							key_array[i+j] = obj_key

						# if the other object already has a number, change the number of the new object and all conected.
						else:
							obj_key_wrong = obj_key
							obj_key = (key_array[i+j])
							for p in range(i+j):
								if (key_array[p]) == obj_key_wrong:
									(key_array[p]) = obj_key

			# write all the object numbers back to the database
			for i in range(len(data_array)):
				c.execute("UPDATE moving SET object_no=:i_obj WHERE id=:i_id"
				, {"i_obj": key_array[i], "i_id": id_array[i]})
			conn.commit()



	print('total time:'+ str(time.time()-tot_time)) #DEBUG



def test_find_point_clouds(db_name=init.db_name):
	print('testing: find_point_clouds')
	find_point_clouds(db_name)


	#output.print_table('moving')

	#def sort_clouds():
	#    exit
	# the frames have to be sticked togehter

	#def find_focus():
	#    exit


	# def all the test functions
