import create_db
import output
import statistics
import sqlite3
import time
import init

def find_background(db_name):
	tot_time = time.time() #DEBUG
	R_time=time.time() #DEBUG

	# open db and create a new table
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	sql_command_to_drop = "DROP TABLE IF EXISTS background" 
	c.execute(sql_command_to_drop)  
	sql_command_to_create = """CREATE TABLE background(
				azimuth INTEGER NOT NULL,
	laser_id INTEGER NOT NULL,
				median_dist REAL,
	PRIMARY KEY(azimuth, laser_id)
	)"""
	c.execute(sql_command_to_create)
	conn.commit()

	# get values from main
	c.execute("SELECT * FROM main")
	data_array = c.fetchall()

	print('R time: ' + str(time.time()-R_time)) #DEBUG
	A_time=time.time() #DEBUG

	# sort main array by azimuth
	sort_array = sorted(data_array, key=lambda x: x[7])

	print('A time: ' + str(time.time()-A_time)) #DEBUG

	break_flag = False
	main_id = 0
	t = 500 #DEBUG
	five_time=time.time() #DEBUG
	for i_azimuth in range(init.max_azimuth_value):
		if i_azimuth == t: #DEBUG
			print(str(i_azimuth) + '\t' + str(time.time()-five_time)) #DEBUG
			t = t + 500 #DEBUG
			five_time=time.time() #DEBUG

		same_az_array = []
		same_azimuth_flag = True
		while same_azimuth_flag == True:
			if sort_array[main_id][7] == i_azimuth:
				same_az_array.append(sort_array[main_id])
				main_id = main_id + 1
				if main_id == len(sort_array):
					break_flag = True
					break
			else:
				same_azimuth_flag = False

		if break_flag == True:
			break

		for i_laser_id in range(0, init.max_laser_id_value+1):
			same_lid_array = []
			for m in range(len(same_az_array)):
				if same_az_array[m][6] == i_laser_id:
					same_lid_array.append(same_az_array[m])




			# calculate the median
			distance_array = []
			median_distance = 0
			for j in range(len(same_lid_array)):
				distance_array.append(same_lid_array[j][8])
			try:
				median_distance = statistics.median(distance_array)
			except:
				median_distance = 0.0
			# write the median into the new table
			if median_distance != 0.0:
				sql_command_to_fill = 'INSERT INTO background VALUES('
				sql_command_to_fill += str(i_azimuth) + ','
				sql_command_to_fill += str(i_laser_id) + ','
				sql_command_to_fill += str(median_distance) + ')'
			else:
				sql_command_to_fill = 'INSERT INTO background VALUES('
				sql_command_to_fill += str(i_azimuth) + ','
				sql_command_to_fill += str(i_laser_id) + ','
				sql_command_to_fill += "NULL" + ')'		
			
			c.execute(sql_command_to_fill)		
	conn.commit()
		#print('F time: ' + str(time.time()-E_time))

	print('total time:'+ str(time.time()-tot_time)) #DEBUG







def compare_with_background(db_name):
	tot_time = time.time() #DEBUG

	# connect to the database
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	
	# create a new table for the not background, means moving objects
	sql_command_to_drop = "DROP TABLE IF EXISTS moving"
	c.execute(sql_command_to_drop)
	sql_command_to_create = """
				CREATE TABLE moving(
				id INTEGER PRIMARY KEY,
				frame_no INTEGER,
				x REAL,
				y REAL,
				z REAL, 
				intensity REAL,
				laser_id INTEGER,
				azimuth INTEGER,
				distance_m REAL,
				object_no INTEGER
				)"""
	c.execute(sql_command_to_create)
	conn.commit()





	# get values from main
	R_time=time.time() #DEBUG
	c.execute("SELECT * FROM main")
	main_array_unsorted = c.fetchall()

	print('R time: ' + str(time.time()-R_time)) #DEBUG
	A_time=time.time() #DEBUG

	# sort main array by azimuth
	main_array = sorted(main_array_unsorted, key=lambda x: x[7])

	print('A time: ' + str(time.time()-A_time)) #DEBUG'


	# get values from background
	R_time=time.time() #DEBUG
	c.execute("SELECT * FROM background")
	background_array = c.fetchall()

	print('R time: ' + str(time.time()-R_time)) #DEBUG




	same_azimuth_flag = True
	break_flag = False
	i_azimuth = 0
	i_laser_id = 0
	i_key = 0
	n = 0
	t = 500 #DEBUG
	five_time=time.time() #DEBUG
	for i in range (len(background_array)):

		
		#B_time = time.time()
		i_az = background_array[i][0]
		i_lid = background_array[i][1]
		median = background_array[i][2]

		if i_az == t: #DEBUG
			print(str(i_az) + '\t' + str(time.time()-five_time)) #DEBUG
			t = t + 500 #DEBUG
			five_time=time.time() #DEBUG


		same_az_array = []
		same_azimuth_flag = True
		
		while same_azimuth_flag == True:
			if main_array[n][7] == i_azimuth:
				same_az_array.append(main_array[n])
				n = n + 1
				if n == len(main_array):
					break_flag = True
					break
			else:
				same_azimuth_flag = False

		if break_flag == True:
			break

		for i_laser_id in range(init.max_laser_id_value+1):
			same_lid_array = []
			for m in range(len(same_az_array)):
				if same_az_array[m][6] == i_laser_id:
					same_lid_array.append(same_az_array[m])
	
			# compare the distance of each record with the median
			for n in range(len(same_lid_array)):

				if abs( same_lid_array[n][8] - median) != 0:
					print(abs( same_lid_array[n][8] - median))

				#print(abs( same_lid_array[n][8] - median)) #DEBUG
				if abs( same_lid_array[n][8] - median) >= init.backgnd_tol:
					
					# copy the data from the main record to the moving one. But with a new key.
					sql_command_to_fill = 'INSERT INTO moving VALUES('
					sql_command_to_fill += str(i_key) + ','
					sql_command_to_fill += str(main_array[n][1]) + ','
					sql_command_to_fill += str(main_array[n][2]) + ','
					sql_command_to_fill += str(main_array[n][3]) + ','
					sql_command_to_fill += str(main_array[n][4]) + ','
					sql_command_to_fill += str(main_array[n][5]) + ','
					sql_command_to_fill += str(main_array[n][6]) + ','
					sql_command_to_fill += str(main_array[n][7]) + ','
					sql_command_to_fill += str(main_array[n][8]) + ','
					sql_command_to_fill += "NULL" + ')'
					c.execute(sql_command_to_fill)					
					i_key = i_key + 1

		#print('B time: ' + str(time.time()-B_time)) #DEBUG'
	conn.commit()
	print('total time:'+ str(time.time()-tot_time)) #DEBUG
						
def test_find_background(db_name=init.db_name):
	print('testing: find_background')
	find_background(db_name)

	# conn = sqlite3.connect(db_name)
	# c = conn.cursor()

	# c.execute(sql_command_to_select)
	# array=c.fetchall()
	# print(array)

def test_compare_with_background(db_name=init.db_name):
	print('testing: compare_with_background')

	compare_with_background(db_name)

	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	
	#output.print_table('moving')
	# sql_command_to_select = "SELECT * FROM " + "background WHERE azimuth=12 AND laser_id=5"
	# c.execute(sql_command_to_select)
	# array=c.fetchall()
	# print(array)
