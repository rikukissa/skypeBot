# -*- coding: utf-8 -*-
class Module:
  def __init__(self):
    self.moduleName = 'ping'

  def onMessage(self, msg):
    if msg.Body is '!ping':
      msg.Chat.SendMessage('pong')