import create_db
import output
import statistics
import sqlite3
import time
import init

def find_background(db_name):

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


	# for each combination of azimuth and laser_id
	i_azimuth=0
	i_laser_id=0
	for i_azimuth in range(init.max_azimuth_value):
		for i_laser_id in range(-init.max_laser_id_value, init.max_laser_id_value):
			
			# get all the fitting records
			c.execute("SELECT * FROM main WHERE azimuth=:i_azimuth AND laser_id=:i_laser_id"
						, {"i_azimuth": i_azimuth, "i_laser_id": i_laser_id})
			data_array = c.fetchall()

			# calculate the median
			distance_array = []
			median_distance = 0
			for n in range(len(data_array)):
				distance_array.append(data_array[n][8])
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
      




def compare_with_background():

	# connect to the database
	conn = sqlite3.connect('data.db')
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

	i_azimuth = 0
	i_laser_id = 0
	i_key = 0
	for i_azimuth in range(init.max_azimuth_value):
		for i_laser_id in range(-init.max_laser_id_value, init.max_laser_id_value):
			# get all the data for the fitting azimuth/laser_id combination
			c.execute("SELECT * FROM main WHERE azimuth=:i_azimuth AND laser_id=:i_laser_id"
					, {"i_azimuth": i_azimuth, "i_laser_id": i_laser_id})
			main_array = c.fetchall()

			# get the median value
			c.execute("SELECT * FROM background WHERE azimuth=:i_azimuth AND laser_id=:i_laser_id"
					, {"i_azimuth": i_azimuth, "i_laser_id": i_laser_id})
			background_array = c.fetchall()
			median = background_array[0][2]

			# compare the distance of each record with the median
			for n in range(len(main_array)):
				print(abs( main_array[n][8] - median))
				if abs( main_array[n][8] - median) >= init.backgnd_tol:
					
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
	conn.commit()
						
def test_find_background(db_name='data.db'):
	print('testing: find_background')
	find_background(db_name)

	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	sql_command_to_select = "SELECT * FROM " + "background WHERE azimuth=12 AND laser_id=5"
	c.execute(sql_command_to_select)
	array=c.fetchall()
	print(array)

def test_compare_with_background(db_name='data.db'):
	print('testing: compare_with_background')

	compare_with_background()

	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	
	output.print_table('moving')
	# sql_command_to_select = "SELECT * FROM " + "background WHERE azimuth=12 AND laser_id=5"
	# c.execute(sql_command_to_select)
	# array=c.fetchall()
	# print(array)