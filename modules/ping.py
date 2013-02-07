# -*- coding: utf-8 -*-
class Module:
  def __init__(self):
    self.moduleName = 'ping'

  def on_message(self, msg):
    if msg.Body == '!ping':
      msg.Chat.SendMessage('pong')
