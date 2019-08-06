import create_db
import os
from pathlib import Path

database_file= 'data.db'
#if database_file.is_file():
 #   print('Jop')
name=os.getcwd() + '\\' + database_file
temp=os._exists(name)
print(name)
print(temp)
#if os.exists(database_file)==1:
 #   print('Hell Yeah!')
