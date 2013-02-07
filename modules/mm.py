# -*- coding: utf-8 -*-
class Module:
  def __init__(self):
    self.module_name = 'mm'

  def on_message(self, msg):
    if msg.Body == 'mm': msg.Chat.SendMessage('mm')
