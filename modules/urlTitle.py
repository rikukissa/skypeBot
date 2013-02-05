# -*- coding: utf-8 -*-
import requests
import BeautifulSoup
import re

class Module:
  def __init__(self):
    self.moduleName = 'urlTitle'
    self.urlRegex = '(https?|ftp):\/\/(([\w\-]+\.)+[a-zA-Z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?(\/([\w\-~.#\/?=&;:+%!*\[\]@$\()+,|\^]+)?)?'

  def onMessage(self, msg):
    if re.match(self.urlRegex, msg.Body, re.IGNORECASE):
      try:
        r = requests.get(msg.Body)
        if r.status_code == 200:
          soup = BeautifulSoup.BeautifulSoup(r.text)
          msg.Chat.SendMessage(soup.title.string)
      except:
        pass