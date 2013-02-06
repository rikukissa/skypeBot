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
    self.sentTime = 0
    self.hintsGiven = 0
    self.hintSent = 0
    self.maxHints = 4

  def isCorrect(self, answ, reset = True):
    if answ.lower() == self.answer.lower():
      if reset:
        self.hintsGiven = 0
      return True
    return False

  def sendHint(self, chat):
    if self.hintsGiven >= self.maxHints:
      chat.SendMessage('Ei enempää vihjeitä.')
      return
    if time.time() - self.hintSent < 10:
      chat.SendMessage('Viimeisestä vihjeestä on alle 10 sekuntia (facepalm)')
      return

    self.hintsGiven += 1
    charsVisible = int(math.floor(len(self.answer) / self.maxHints) * self.hintsGiven)
    chat.SendMessage('Vihje: ' + self.answer[0:charsVisible])
    self.hintSent = time.time()

class Module:
  def __init__(self):
    self.moduleName = 'triviaBot'
    
    self.running = False
    self.chatRoom = None
    self.currentQuestion = None 
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

  def selectQuestion(self):
    index = random.randint(0, len(self.questions)) # Random index from questions list
    return self.questions[index]

  def newQuestion(self):    
    self.currentQuestion = self.selectQuestion()
    self.currentQuestion.sentTime = time.time()
    self.currentQuestion.hintSent = 0
    self.sendQuestion()

  def sendQuestion(self):
    self.chatRoom.SendMessage('Kysymys ' + str(self.currentQuestion.id) + ': ' + self.currentQuestion.question)

  def sendStats(self):
    if len(self.players) == 0:
      self.chatRoom.SendMessage('Kukaan ei ole vielä saanut pisteitä')   
      return

    for player in self.players:
      self.chatRoom.SendMessage(player.username + ': ' + str(player.points))

  def getPlayer(self, username):
    for i in range(len(self.players)):
      if self.players[i].username == username:
        return self.players[i]

    player = Player(username)
    self.players.append(player)
    return player

  def onMessage(self, msg):
    if msg.Body == '!trivia start' and not self.running:
      self.running = True
      
      if self.chatRoom is None:
        self.chatRoom = msg.Chat # Get the correct chatroom from skype
      
      self.chatRoom.SendMessage('Tervetuloa pelaamaan eeppistä Skype triviaa!')
      self.newQuestion()
      return

    if self.running:
      player = self.getPlayer(msg.FromHandle)

      if msg.Body == '!trivia stop':
        self.running = False
        return 

      if msg.Body == '!trivia stats':
        self.sendStats()
        return

      if msg.Body == '!trivia next':
        self.chatRoom.SendMessage('Kukaan ei arvannut oikeaa vastausta. Oikea vastaus oli: ' + self.currentQuestion.answer)
        self.newQuestion()
        return
      
      if msg.Body == '!trivia hint' or msg.Body == '!trivia vihje':
        self.currentQuestion.sendHint(self.chatRoom)
        return

      if self.currentQuestion.isCorrect(msg.Body):
        self.chatRoom.SendMessage(player.username + ' arvasi oikein! Oikea vastaus oli: ' + self.currentQuestion.answer)
        player.points += 1
        self.newQuestion()
        return
      if time.time() - self.currentQuestion.sentTime > 60:
        self.chatRoom.SendMessage('Kukaan ei arvannut oikeaa vastausta. Oikea vastaus oli: ' + self.currentQuestion.answer)
        self.newQuestion()