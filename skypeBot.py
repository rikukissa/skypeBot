# -*- coding: utf-8 -*-
from settings import *
import Skype4Py
import time
import os
import imp
import re

def importModule(moduleName):
  try:
    module = imp.load_source('module', MODULE_PATH + moduleName + '.py')
    loadedModules.append(module.Module())
    return True
  except IOError:
    return False

def loadModule(msg, moduleName):
  if msg.FromHandle not in ADMINS:
    msg.Chat.SendMessage('Don\'t tell me what to do! (lalala)')
    return 
  for module in loadedModules:
    if module.moduleName == moduleName:
      msg.Chat.SendMessage('Module ' + moduleName + ' is already loaded')
      return
  if importModule(moduleName):
    msg.Chat.SendMessage('Loaded module: ' + moduleName)
  else:
    msg.Chat.SendMessage('Couldn\'t load module: ' + moduleName)

def unloadModule(msg, moduleName):
  for i in range(len(loadedModules)):
    if loadedModules[i].moduleName == moduleName:
      del loadedModules[i]
      msg.Chat.SendMessage('Unloaded module: ' + moduleName)
      return
  msg.Chat.SendMessage('Module ' + moduleName + ' is not loaded')

def promote(msg, user):
  ADMINS.append(user)
  msg.Chat.SendMessage('User ' + user + ' is now an admin')
# Load modules on startup
loadedModules = []
for module in LOAD_MODULES:
  importModule(module)

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
    for module in loadedModules:
      if hasattr(module, 'onMessage'):
        module.onMessage(msg)


  commands = {
    '!loadModule (.+)': loadModule,
    '!unloadModule (.+)': unloadModule,
    '!promote (.+)': promote
  }

bot = SkypeBot()

while True:
  time.sleep(1.0)
