# -*- coding: utf-8 -*-
import requests
import re

class Module:
  def __init__(self):
    self.module_name = 'urlTitle'
    self.url_regex = '(https?|ftp):\/\/(([\w\-]+\.)+[a-zA-Z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?(\/([\w\-~.#\/?=&;:+%!*\[\]@$\()+,|\^]+)?)?'

  def on_message(self, msg):
    if re.match(self.url_regex, msg.Body, re.IGNORECASE):
      try:
        r = requests.get(msg.Body)
      except requests.RequestException:
        print requests.RequestException.Message
        return

      title = re.search('<title>(.*?)</title>', r.text)
      if title:
        msg.Chat.SendMessage(title.group(1))
