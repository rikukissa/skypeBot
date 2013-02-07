# -*- coding: utf-8 -*-

# Trivia bot for SkypeBot
# 
# Commands:
# !trivia start - Start trivia
# !trivia stop  - Stop trivia
# !trivia next  - Skip the current question
# !trivia stats - Echo current players and points
# !trivia (hint|vihje)  - Hint for the current question 

import json, urllib, random, math, time

class Player:
  def __init__(self, username):
    self.username = username
    self.points = 0

class Question:
  def __init__(self, question, answer, index):
    self.question = question
    self.answer = answer
    self.id = index
    self.sent_time = 0
    self.hints_given = 0
    self.hint_sent = 0
    self.max_hints = 4

  def is_correct(self, answ, reset=True):
    if answ.lower() == self.answer.lower():
      if reset:
        self.hints_given = 0
      return True
    return False

  def send_hint(self, chat):
    if self.hints_given >= self.max_hints:
      chat.SendMessage('Ei enempää vihjeitä.')
      return
    if time.time() - self.hint_sent < 10:
      chat.SendMessage('Viimeisestä vihjeestä on alle 10 sekuntia (facepalm)')
      return

    self.hints_given += 1
    chars_visible = int(math.floor(len(self.answer) / self.max_hints) * self.hints_given)
    chat.SendMessage('Vihje: ' + self.answer[0:chars_visible])
    self.hint_sent = time.time()

class Module:
  def __init__(self):
    self.module_name = 'triviaBot'
    self.running = False
    self.chat_room = None
    self.current_question = None 
    self.players = []

    # Load questions
    # Might be better to store these in a database instead of a JSON file
    self.questions = [] 
    json_data = open('lib/trivia.json')
    data = json.load(json_data)
    index = 0
    for entry in data:
      index += 1
      self.questions.append(Question(entry['q'], entry['a'], index))

  def select_question(self):
    index = random.randint(0, len(self.questions)) # Random index from questions list
    return self.questions[index]

  def new_question(self):    
    self.current_question = self.select_question()
    self.current_question.sent_time = time.time()
    self.current_question.hint_sent = 0
    self.send_question()

  def send_question(self):
    self.chat_room.SendMessage('Kysymys ' + str(self.current_question.id) + ': ' + self.current_question.question)

  def send_stats(self):
    if len(self.players) == 0:
      self.chat_room.SendMessage('Kukaan ei ole vielä saanut pisteitä')   
      return

    for player in self.players:
      self.chat_room.SendMessage(player.username + ': ' + str(player.points))

  def get_player(self, username):
    for i in range(len(self.players)):
      if self.players[i].username == username:
        return self.players[i]

    player = Player(username)
    self.players.append(player)
    return player

  def on_message(self, msg):
    if msg.Body == '!trivia start' and not self.running:
      self.running = True
      
      if self.chat_room is None:
        self.chat_room = msg.Chat # Get the correct chatroom from skype
      
      self.chat_room.SendMessage('Tervetuloa pelaamaan eeppistä Skype triviaa!')
      self.new_question()
      return

    if self.running:
      player = self.get_player(msg.FromHandle)

      if msg.Body == '!trivia stop':
        self.running = False
        return 

      if msg.Body == '!trivia stats':
        self.send_stats()
        return

      if msg.Body == '!trivia next':
        self.chat_room.SendMessage('Kukaan ei arvannut oikeaa vastausta. Oikea vastaus oli: ' + self.current_question.answer)
        self.new_question()
        return
      
      if msg.Body == '!trivia hint' or msg.Body == '!trivia vihje':
        self.current_question.send_hint(self.chat_room)
        return

      if self.current_question.is_correct(msg.Body):
        self.chat_room.SendMessage(player.username + ' arvasi oikein! Oikea vastaus oli: ' + self.current_question.answer)
        player.points += 1
        self.new_question()
        return
      if time.time() - self.current_question.sent_time > 60:
        self.chat_room.SendMessage('Kukaan ei arvannut oikeaa vastausta. Oikea vastaus oli: ' + self.current_question.answer)
        self.new_question()