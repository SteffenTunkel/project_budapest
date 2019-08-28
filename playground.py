import sqlite3
import time
import init
print('test start')
conn = sqlite3.connect(init.db_name)
c = conn.cursor()

db_time = time.time()
c.execute("SELECT * FROM main")
data_array = c.fetchall()
print('db time:'+ str(time.time()-db_time))

sort_time=time.time()
sort_array = sorted(data_array, key=lambda x: x[7])

print('sort time: ' + str(time.time()-sort_time))
#sorted(data_array, key=data_array[3])
#sort_array.index(n,0,100)
#sort_array.index()
print(str(sort_array[2]))
exit_flag, exit_flag_2 = 0, 0
n=0
for i_azimuth in range(init.max_azimuth_value):
	temp_array = []
	temp2_array = []
	exit_flag = 0
	while exit_flag == 0:
		if sort_array[n][7] == i_azimuth:
			temp_array.append(sort_array[n])
			n = n + 1
			if n == len(sort_array):
				print("error")
		else:
			exit_flag = 1
	for i_laser_id in range(0, init.max_laser_id_value+1):
		temp2_array = []
		for m in range(len(temp_array)):
			if sort_array[m][6] == i_laser_id:
				temp2_array.append(temp_array[m])
		print(temp2_array)
print('end')

def find(searchList, elem):
	return [[i for i, x in enumerate(searchList) if x == e] for e in elem]


