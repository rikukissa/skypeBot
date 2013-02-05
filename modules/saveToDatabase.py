# -*- coding: utf-8 -*-
import pymongo

class Module:
  def __init__(self):
    self.moduleName = 'saveToDatabase'
    self.conn = pymongo.Connection('mongodb://localhost:27017')
    self.db = self.conn['skype']

  def onMessage(self, msg):
    self.db.messages.insert({
      'id': msg.Id,
      'timestamp': msg.Timestamp,
      'body': msg.Body,
      'displayName': msg.FromDisplayName,
      'username': msg.FromHandle
    })