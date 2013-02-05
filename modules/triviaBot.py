# -*- coding: utf-8 -*-

# Trivia bot for SkypeBot
# 
# Commands:
# !trivia start - Start trivia
# !trivia stop  - Stop trivia
# !trivia next  - Skip the current question
# !trivia hint  - Hint for the current question 
# !trivia stats - Echo current players and points

import json, urllib, random, math

class Player:
  def __init__(self, username):
    self.username = username
    self.points = 1

class Question:
  def __init__(self, q, a):
    self.question = q
    self.answer = a
    self.hintsGiven = 0
    self.maxHints = 4

  def isCorrect(self, answ, reset = True):
    if answ.lower() == self.answer.lower():
      if reset:
        self.hintsGiven = 0
      return True
    return False

  def getHint(self):
    if self.hintsGiven >= self.maxHints:
      return 'Ei enempää vihjeitä.'
    
    self.hintsGiven += 1
    charsVisible = int(math.floor(len(self.answer) / self.maxHints) * self.hintsGiven)
    return self.answer[0:charsVisible]

class Module:
  def __init__(self):
    self.moduleName = 'triviaBot'
    
    self.running = False
    self.chatRoom = None
    self.players = []

    # Index in questions list, could be changed to mongoId or something
    self.questionIndex = 0 

    # Load questions
    # Might be better to store these in a database instead of a JSON file
    self.questions = []
    
    json_data = open('lib/trivia.json')
    data = json.load(json_data)
    for entry in data:
      self.questions.append(Question(entry['q'], entry['a']))

  def selectQuestion(self):
    return random.randint(0, len(self.questions)) # Random index from questions list
  
  def newQuestion(self):
    nextIndex = self.questionIndex

    # Loop as long as the index changes
    while nextIndex is self.questionIndex:
      nextIndex = self.selectQuestion()
    
    self.questionIndex = nextIndex
    self.sendQuestion()

  def sendQuestion(self):
    currentQuestion = self.questions[self.questionIndex]
    self.chatRoom.SendMessage('Kysymys ' + str(self.questionIndex) + ': ' + currentQuestion.question)

  def sendStats(self):
    if len(self.players) == 0:
      self.chatRoom.SendMessage('Kukaan ei ole vielä saanut pisteitä')   
      return

    for player in self.players:
      self.chatRoom.SendMessage(player.username + ': ' + str(player.points))

  def getPlayerIndex(self, username):
    for i in range(len(self.players)):
      if self.players[i].username == username:
        return i

    player = Player(username)
    self.players.append(player)
    return len(self.players) - 1

  def onMessage(self, msg):
    if msg.Body == '!trivia start' and not self.running:
      self.running = True
      
      if self.chatRoom is None:
        self.chatRoom = msg.Chat # Get the correct chatroom from skype
      
      self.chatRoom.SendMessage('Tervetuloa pelaamaan eeppistä trivia-peliä!')
      self.questionIndex = self.selectQuestion()
      self.sendQuestion()
        
    if self.running:
      currentQuestion = self.questions[self.questionIndex]
      playerIndex = self.getPlayerIndex(msg.FromHandle) # Reference or not?
      player = self.players[playerIndex]

      if msg.Body == '!trivia stop':
        self.running = False

      if msg.Body == '!trivia stats':
        self.sendStats()
            
      if msg.Body == '!trivia hint':
        self.chatRoom.SendMessage('Vihje: ' + currentQuestion.getHint())
      
      if msg.Body == '!trivia next':
        self.newQuestion()
      


      if currentQuestion.isCorrect(msg.Body):
        self.chatRoom.SendMessage(player.username + ' arvasi oikein! Oikea vastaus oli: ' + currentQuestion.answer)
        player.points += 1
        self.newQuestion()