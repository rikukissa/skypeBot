# -*- coding: utf-8 -*-
import requests
import re

class Module:
  def __init__(self):
    self.moduleName = 'urlTitle'
    self.urlRegex = '(https?|ftp):\/\/(([\w\-]+\.)+[a-zA-Z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?(\/([\w\-~.#\/?=&;:+%!*\[\]@$\()+,|\^]+)?)?'

  def onMessage(self, msg):
    if re.match(self.urlRegex, msg.Body, re.IGNORECASE):
      try:
        r = requests.get(msg.Body)
      except requests.RequestException:
        print requests.RequestException.Message
        return

      title = re.search('<title>(.*?)</title>', r.text)
      if title:
        msg.Chat.SendMessage(title.group(1))
