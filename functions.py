from flask import session
import dns
import pymongo
import os
import datetime
import random
import requests
from string import printable
from werkzeug.security import generate_password_hash, check_password_hash

clientm = pymongo.MongoClient(os.getenv("clientm"))
usersdb = clientm.Users
profilescol = usersdb.Profiles

def addcookie(key, value):
  session[key] = value

def delcookies():
  session.clear()

def getcookie(key):
  try:
    if (x := session.get(key)):
      return x
    else:
      return False
  except:
    return False

def gethashpass(username):
  myquery = { "Username": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return x['Password']
  return False

def getuserid(id):
  myquery = { "_id": int(id) }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return True
  return False

def getuser(username):
  myquery = { "Username": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    if x.get("Deleted", None) == None:
      return x
    return False
  return False

def checkusernamealready(username):
  myquery = { "Username": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return True
  return False

def makeaccount(username, password, passwordagain):
  if len(username) > 25:
    return "Your username cannot have more than 25 letters!"
  if len(username) < 2:
    return "You have to have more than 2 letters in your username!"
  if set(username).difference(printable):
    return "Your username cannot contain any special characters!"
  if username != username.lower():
    return "Your username has to be all lowercase!"
  if checkusernamealready(username) == True:
    return "A user already has this username! Try another one."
  if password != passwordagain:
    return "The two passwords don't match!"
  if len(password) > 25:
    return "Your password cannot have more than 25 letters!"
  if len(password) < 2:
    return "You have to have more than 2 letters in your password!"
  if set(password).difference(printable):
    return "Your password cannot contain any special characters!"
  passhash = generate_password_hash(password)
  document = [{
    "Username": username,
    "Password": passhash,
    "Created": str(datetime.datetime.now()),
    "Money": 0,
    "XP": 0,
    "Daily": [],
    "Block": [0],
    "Description": None
  }]
  profilescol.insert_many(document)
  return True

def makeblockbigger(username):
  user = getuser(username)
  usergrid = user['Block']
  level = str(int(user['XP'])/1000 + 1).split(".")[0]
  lengrid = len(usergrid)
  if int(lengrid) == int(level):
    return "You need to go to the next level to make your block bigger!"
  if lengrid == 1000:
    return "You can't make your block bigger as it's the maximum size that you can make it!"
  if user['Money'] < 10000:
    return "You need ∆10000 to make your block bigger!"
  newmoney = user['Money'] - 10000
  newgrid = usergrid
  newgrid.append(0)
  user2 = user
  del user2['Block']
  user2['Block'] = newgrid
  del user2['Money']
  user2['Money'] = newmoney
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def addmoney(username, amount):
  user = getuser(username)
  money = user['Money']
  newmoney = money + amount
  user2 = user
  del user2['Money']
  user2['Money'] = newmoney
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def addxp(username, amount):
  user = getuser(username)
  xp = user['XP']
  newxp = xp + amount
  user2 = user
  del user2['XP']
  user2['XP'] = newxp
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def rps(username, guess, bet):
  try:
    bet = int(bet)
  except:
    return f"{bet} isn't an integer!"
  if bet < 100:
    return "You have to bet at least ∆100!"
  if bet > 10000:
    return "You cannot bet more than ∆10000!"
  comp = random.choice(['rock', 'paper', 'scissors'])
  if comp == 'rock':
    if guess == 'rock':
      return "It was a draw! You did rock and the computer did rock!"
    if guess == 'paper':
      addmoney(username, bet*2)
      return "You won! You did paper and the computer did rock!"
    if guess == 'scissors':
      addmoney(username, bet*-1)
      return "You lost! You did scissors and computer did rock!"
  if comp == 'paper':
    if guess == 'rock':
      addmoney(username, bet*-1)
      return "You lost! You did rock and the computer did paper!"
    if guess == 'paper':
      return "It was a draw! You did paper and the computer did paper!"
    if guess == 'scissors':
      addmoney(username, bet*2)
      return "You won! You did scissors and the computer did paper!"
  if comp == 'scissors':
    if guess == 'rock':
      addmoney(username, bet*2)
      return "You won! You did rock and the computer did scissors!"
    if guess == 'paper':
      addmoney(username, bet*-1)
      return "You lost! You did paper and the computer did rock!"
    if guess == 'scissors':
      return "It was a draw! You did scissors and the computer did scissors!"

def addxpmoney(username, addxp, addmoney):
  user = getuser(username)
  money = user['Money']
  newmoney = money + addmoney
  user2 = user
  del user2['Money']
  user2['Money'] = newmoney
  xp = user['XP']
  newxp = xp + addxp
  del user2['XP']
  user2['XP'] = newxp
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def cupgame(username, guess, bet):
  try:
    bet = int(bet)
  except:
    return f"{bet} isn't an integer!"
  if bet < 100:
    return "You have to bet at least ∆100!"
  if bet > 10000:
    return "You cannot bet more than ∆10000!"
  answer = random.choice(['1', '2', '3'])
  if guess == answer:
    addmoney(username, bet*3)
    return f"You won! The ball landed in cup {answer}!"
  else:
    addmoney(username, bet*-1)
    return f"You lost! The ball landed in cup {answer} and you wanted it to land in cup {guess}!"
  
def rolldice(username, guess, bet):
  try:
    bet = int(bet)
  except:
    return f"{bet} isn't an integer!"
  if bet < 100:
    return "You have to bet at least ∆100!"
  if bet > 10000:
    return "You cannot bet more than ∆10000!"
  answer = random.choice(['1', '2', '3', '4', '5', '6'])
  if guess == answer:
    addmoney(username, bet*6)
    return f"You won! The dice rolled {answer}!"
  else:
    addmoney(username, bet*-1)
    return f"You lost! The dice rolled {answer} and you wanted it to roll {guess}!"

def flipcoin(username, guess, bet):
  try:
    bet = int(bet)
  except:
    return f"{bet} isn't an integer!"
  if bet < 100:
    return "You have to bet at least ∆100!"
  if bet > 10000:
    return "You cannot bet more than ∆10000!"
  answer = random.choice(['heads', 'tails'])
  if guess == answer:
    addmoney(username, bet*2)
    return f"You won! The coin flipped {answer}!"
  else:
    addmoney(username, bet*-1)
    return f"You lost! The coin flipped {answer} and you wanted it to flip {guess}!"

def getquestion():
  url = "https://opentdb.com/api.php?amount=1"
  response = requests.get(url)
  return response.json()

def mencalc():
  thetype = random.choice(['add', 'subtract', 'multiply', 'divide', 'square', 'square root'])
  if thetype == 'add':
    number1 = random.randint(100,9999)
    number2 = random.randint(100,9999)
    answer = number1 + number2
    question = f"What is {str(number1)} + {str(number2)}?"
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    addcookie("MathsAns", str(answer))
    return question
  if thetype == 'subtract':
    number1 = random.randint(100,9999)
    number2 = random.randint(100,9999)
    answer = number1 - number2
    question = f"What is {str(number1)} - {str(number2)}?"
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    addcookie("MathsAns", str(answer))
    return question
  if thetype == 'multiply':
    number1 = random.randint(0,20)
    number2 = random.randint(0,20)
    answer = number1 * number2
    question = f"What is {str(number1)} × {str(number2)}?"
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    addcookie("MathsAns", str(answer))
    return question
  if thetype == 'divide':
    answer = random.randint(0,20)
    number2 = random.randint(0,20)
    number1 = number2 * answer
    question = f"What is {str(number1)} ÷ {str(number2)}?"
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    addcookie("MathsAns", str(answer))
    return question
  if thetype == 'square':
    number = random.randint(0,20)
    answer = number * number
    question = f"What is the square of {str(number)}?"
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    addcookie("MathsAns", str(answer))
    return question
  if thetype == 'square root':
    answer = random.randint(0,20)
    number = answer * answer
    question = f"What is the square root of {str(number)}?"
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    addcookie("MathsAns", str(answer))
    return question

def upgradeblock(username, index):
  try:
    if getuser(username)['Money'] < 5000:
      return "You need ∆5000 to upgrade one of the blocks in your block!"
    index = int(index)
    user = getuser(username)
    thetype = user['Block'][int(index)]
    if thetype == 1:
      return "You have upgraded that block in your block the most you can!"
    newtype = thetype + 1
    user2 = user
    block = user2['Block']
    block.pop(index)
    block[index:index] = [newtype]
    del user2['Block']
    user2['Block'] = block
    money = user2['Money']
    newmoney = money - 5000
    del user2['Money']
    user2['Money'] = newmoney
    profilescol.delete_one({"Username": username})
    profilescol.insert_many([user2])
    return True
  except:
    return "That is not real land on your grid!"