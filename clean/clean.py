#!/usr/bin/env python
########################################
# Description: Clean resource exchange #
# Mantainer: Ilyin.V.V          ########
# Date: 26.01.2021              #
#################################

import sys
import os
from datetime import datetime
import time
import shutil
sys.path.append('../conf/')
import config
import logger

class Core(object):
 def __init__(self):
  self.name = "Core"
  self.date = datetime.strftime(
   datetime.now(),'%Y-%m-%d')

 def find_res(self,res_path,old_path,res_day):
  find_obj = Core()
  for root,dirs,files in os.walk(res_path,topdown = False):
   for name in files:
    file_mtime = find_obj.get_mtime(os.path.join(root,name))
    old_res = find_obj.filter(os.path.join(root,name),
     file_mtime[0],file_mtime[1],res_day)
    if old_res:
     new_root = root[len(res_path):]
     find_obj.create_folder(old_path,new_root)
     find_obj.move_file(os.path.join(root,name),old_path,new_root)
     find_obj.set_mtime(old_path+new_root+'/'+name)
   for name in dirs:
     find_obj.remove_dir(os.path.join(root,name))

 def find_trash(self,old_path,trash_day):
  find_obj = Core()
  for root,dirs,files in os.walk(old_path,topdown = False):
   for name in files:
    file_mtime = find_obj.get_mtime(os.path.join(root,name))
    old_res = find_obj.filter(os.path.join(root,name),
     file_mtime[0],file_mtime[1],trash_day)
    if old_res:
     find_obj.remove_file(os.path.join(root,name))
   for name in dirs:
     find_obj.remove_dir(os.path.join(root,name))

 def get_mtime(self,dir_file):
  file_mtime = os.stat(dir_file).st_mtime
  date_change = datetime.fromtimestamp(
   int(file_mtime)).strftime('%d-%m-%Y')
  return (file_mtime,date_change)

 def filter(self,name,mtime,date_change,day):
  if mtime < time.time() - (int(day) * 86400):
   obj_log = logger.Logger()
   msg = "File "+name+" change "+ \
    date_change+" more "+day+" days"
   print msg; obj_log.log_logged(msg)
   return True
  return False

 def create_folder(self,old_path,create_path):
  obj_log = logger.Logger()
  if not os.path.exists(old_path+create_path):
   os.makedirs(old_path+create_path)
   obj_log.log_logged("Create directory "+
    old_path+create_path)
  else:
   obj_log.log_logged("Directory exists "+
    old_path+create_path)

 def move_file(self,src,dst,new_path):
  if src and dst and new_path:
   obj_log = logger.Logger()
   obj_log.log_logged("Move file "+src+
    " => "+dst+new_path)
   shutil.move(src,dst+new_path)

 def set_mtime(self,file):
  if file:
   os.utime(file,(time.time(),time.time()))

 def remove_file(self,path):
  obj_log = logger.Logger()
  if path:
   if os.path.exists(path):
    os.remove(path)
    obj_log.log_logged("File "+path+
     " remove trash")
   else:
    obj_log.log_logged("File "+path+
     " does not exist")

 def remove_dir(self,path):
  obj_log = logger.Logger()
  if path:
   if os.listdir(path):
    obj_log.log_logged("Directory "+path+
     " not empty skip")
   else:
    shutil.rmtree(path)
    obj_log.log_logged("Directory "+path+
     " empty remove")

if __name__ == "__main__":
 clean_daemon = Core()
 obj_log = logger.Logger()
 config = config.Configuration()
 obj_log.log_logged("Clean exchange operation"+
  " ========================================"+
  "========================================>")
 # Clear exchange
 clean_daemon.find_res(
  config.res_exchange_path,
  config.res_old_exchange_path,
  config.res_exchange_clean)
 # Clear old_exchange
 obj_log.log_logged("Clean trash operation"+
  " ========================================"+
  "========================================>")
 clean_daemon.find_trash(
  config.res_old_exchange_path,
  config.res_old_exchange_clean)
