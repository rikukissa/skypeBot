# -*- coding: utf-8 -*-
class Module:
  def __init__(self):
    self.module_name = 'ping'

  def on_message(self, msg):
    if msg.Body == '!ping':
      msg.Chat.SendMessage('pong')
