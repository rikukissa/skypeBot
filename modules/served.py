# -*- coding: utf-8 -*-
class Module:
  def __init__(self):
    self.module_name = 'served'

  def on_message(self, msg):
    if msg.Body == u'ei mitää' or msg.Body == u'ei mitään':
      msg.Chat.SendMessage('(*) SERVED (*)')
