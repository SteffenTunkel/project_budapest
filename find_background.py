import create_db
import output
import statistics
import sqlite3
import time

# INTEGER PRIMARY KEY bei der anderen Funktion für frame_no in der time table
	#Laserid und azimuth nicht real sondern int
	#allgemeine einstellungen in eine inidatei auslagern
def find_background(db_name):
	max_azimuth_value=36000
	max_laser_id_value=15
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	
	sql_command_to_drop = "DROP TABLE IF EXISTS background"    #1234
	c.execute(sql_command_to_drop)    #1234
    
	sql_command_to_create = """CREATE TABLE background(
                azimuth INTEGER NOT NULL,
		laser_id INTEGER NOT NULL,
                median_dist REAL,
		PRIMARY KEY(azimuth, laser_id)
		)"""
	c.execute(sql_command_to_create)

	conn.commit()
	
		#sql_command_to_select= "SELECT * FROM main WHERE priority=?"
    #c.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
 
    #rows = cur.fetchall()
	i_azimuth=0
	for i_azimuth in range(max_azimuth_value):
		for i_laser_id in range(-max_laser_id_value, max_laser_id_value):
			#sql_command_to_select = "SELECT * FROM main WHERE "
			c.execute('SELECT * FROM main ')#WHERE laser_id = 5')
			#sql_command_to_select += "azimuth='" + str(i_azimuth)+"'"# + ' AND laser_id=' + str(i_laser_id)
			#c.execute(sql_command_to_select)
			points = c.fetchall()
			print(points)
			# ToDo auf distance zugreifen
			#median_distance=statistics.median(distances)
		
				  
			sql_command_to_fill = 'INSERT INTO background VALUES('
			sql_command_to_fill += str(i_azimuth) + ','
			sql_command_to_fill += str(i_laser_id) + ','
			sql_command_to_fill += str(5) + ')'

			c.execute(sql_command_to_fill)
				  
	conn.commit()


def test_find_background(db_name='data.db'):
	print("test_function")
	find_background(db_name)


#def compare_with_background():
# ähnlich zu background finden, alle durchgehen und die einträge mit passendem wert löschen, Toleranz beachten.				  
				 
find_background('data.db')
