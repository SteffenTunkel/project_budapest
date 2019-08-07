import create_db
import statistics

def find_background(db_name):
    max_azimuth_value=36000
		max_laser_id_value=15
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		
		#sql_command_to_select= "SELECT * FROM main WHERE priority=?"
    #c.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
 
    #rows = cur.fetchall()
		
		for i_azimuth in range(max_azimuth_value):
			for i_laser_id in range(-max_laser_id_value, max_laser_id_value):	
				c.execute('SELECT * FROM main WHERE azimuth=? AND laser_id=?', (i_azimuth, i_laser_id)
				points = c.fetchall()
				print(points)
				#ToDo auf distance zugreifen
				#median_distance=statistics.median(points)
				
