#!/usr/bin/env python
# Write log file
from datetime import datetime
import config

class Logger():
 def __init__(self):
  self.name = 'Logger'
  self.daemon = 'Clean_Exchange'
  self.date = datetime.strftime(datetime.now(),
   '%d:%m:%Y-%H:%M:%S')

 def log_logged(self,data):
  obj_log = config.Configuration()
  file_path = obj_log.path+'/log/log.log'
  file = open(file_path, 'a')
  data = self.date+' '+data
  file.write(data +"\n")
  file.close()

 def tmp_file(self,data):
  obj_tmp = config.Configuration()
  file_path = obj_tmp.path+'/tmp/clean.tmp'
  file = open(file_path, 'w')
  file.write(data +"\n")
  file.close()
