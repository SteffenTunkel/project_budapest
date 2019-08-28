# init values for parameters

# data path
data_path   = 'raw_data' # Folder w the laser scanner data ## default 'raw_data'
db_name     = 'data.db' ## default 'data.db'


# read in the data
no_frames = 700              # bigger than the actual number    ## default 700
no_points = 36000           # the actual number is not fixed per frame, but smaller than 20000 in any case
no_coordinates = 7          # x,y,z -> 3 coordinates per point
size_threshold = 1520000    # threshold for the detection of defect frames


# find the background
max_azimuth_value=36000 ## default 36000
max_laser_id_value=15
backgnd_tol=0.001	## defalut 0.5

# find point clouds
cloud_tol=0.1
