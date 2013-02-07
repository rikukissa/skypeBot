# -*- coding: utf-8 -*-
from settings import *
import Skype4Py
import time
import os
import imp
import re

def import_module(module_name):
  try:
    module = imp.load_source('module', MODULE_PATH + module_name + '.py')
    loaded_modules.append(module.Module())
    return True
  except IOError:
    return False

def load_module(msg, module_name):
  if msg.FromHandle not in ADMINS:
    msg.Chat.SendMessage('Don\'t tell me what to do! (lalala)')
    return 
  for module in loaded_modules:
    if module.module_name == module_name:
      msg.Chat.SendMessage('Module ' + module_name + ' is already loaded')
      return
  if import_module(module_name):
    msg.Chat.SendMessage('Loaded module: ' + module_name)
  else:
    msg.Chat.SendMessage('Couldn\'t load module: ' + module_name)

def unload_module(msg, module_name):
  for i in range(len(loaded_modules)):
    if loaded_modules[i].module_name == module_name:
      del loaded_modules[i]
      msg.Chat.SendMessage('Unloaded module: ' + module_name)
      return
  msg.Chat.SendMessage('Module ' + module_name + ' is not loaded')

def promote(msg, user):
  ADMINS.append(user)
  msg.Chat.SendMessage('User ' + user + ' is now an admin')
# Load modules on startup
loaded_modules = []
for module in LOAD_MODULES:
  import_module(module)

class SkypeBot(object):   
  def __init__(self):
    self.skype = Skype4Py.Skype(Events=self)
    self.skype.Attach()

  def AttachmentStatus(self, status):
    if status == Skype4Py.apiAttachAvailable:
      self.skype.Attach()

  def MessageStatus(self, msg, status):
    if status != Skype4Py.cmsReceived: # Message is received
      return

    # Parse commands
    for regexp, target in self.commands.items():
      match = re.match(regexp, msg.Body, re.IGNORECASE)
      if match:      
        target(msg, *match.groups())
    
    # Transmit events to modules
    for module in loaded_modules:
      if hasattr(module, 'onMessage'):
        module.on_message(msg)

  commands = {
    '!loadModule (.+)': load_module,
    '!unload_module (.+)': unload_module,
    '!promote (.+)': promote
  }

bot = SkypeBot()

while True:
  time.sleep(1.0)
