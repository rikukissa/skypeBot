# -*- coding: utf-8 -*-
class Module:
  def __init__(self):
    self.module_name = 'served'

  def on_message(self, msg):
    if msg.Body == 'ei mitää' or msg.Body == 'ei mitään':
      msg.Chat.SendMessage('(*) SERVED (*)')
