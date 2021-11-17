from flask import session
import os
import datetime
import random
import requests
from string import printable
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo
import smtplib
import ssl
import dns
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

clientm = pymongo.MongoClient(os.getenv("clientm"))
usersdb = clientm.Users
profilescol = usersdb.Profiles
notifscol = usersdb.Notifications
gamblingcol = usersdb.Gambling
xpstatscol = usersdb.XPStats
verificationcol = usersdb.Verification

with open("static/words.txt", "r") as file:
  allText = file.read()
  words = list(map(str, allText.split()))

def send_mail(usermail, username, id):  
  context = ssl.create_default_context()
  MAILPASS = os.getenv("MAIL_PASSWORD")
  html = f"""
  <h1>Hello {username}!</h1>
  <p><strong>You have signed up for an account / or changed your email in Jasonism!</strong></p>
  <p>Click <a href='https://jasonism-fork.vulcanwm.repl.co/verify/{username}/{str(id)}'>here</a> to verify your account</p>
  <p>If you didn't make this account, reply back to this email saying this isn't your account and <strong>DO NOT</strong> click on the link or the user who made the account will get verified with your email!</p>
  """
  message = MIMEMultipart("alternative")
  message["Subject"] = "Jasonism Verification Email"
  part2 = MIMEText(html, "html")
  message.attach(part2)
  try:
    sendermail = "stanjasonism@gmail.com"
    password = MAILPASS
    gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
    gmail_server.starttls(context=context)
    gmail_server.login(sendermail, password)
    message["From"] = sendermail
    message["To"] = usermail
    gmail_server.sendmail(sendermail, usermail, message.as_string())
    return True
  except Exception as e:
    return "Verification email not sent, due to some issues."
    gmail_server.quit()

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

def checkverification(theid):
  myquery = {"_id": ObjectId(theid)}
  mydoc = verificationcol.find(myquery)
  for x in mydoc:
    return x
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
      if x.get("BlockName", None) == None:
        x['BlockName'] = "your pet"
      return x
    return False
  return False

def checkusernamealready(username):
  myquery = { "Username": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return True
  return False

def checkemailalready(email):
  myquery = { "Email": email }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return True
  return False

def checkgambling(username):
  myquery = { "Username": username }
  mydoc = gamblingcol.find(myquery)
  for x in mydoc:
    return x
  document = {
    "Username": username,
    "Flipcoin": [0,0,0,0],
    "Rolldice": [0,0,0,0],
    "Cupgame": [0,0,0,0],
    "RPS": [0,0,0,0,0],
    "ChallengeRPS": [0,0,0,0,0]
  }
  return document

def addgambling(username, gametype, stats):
  if checkgambling(username) == False:
    document = [{
      "Username": username,
      # [wontime, losttime, wonmoney-lostmoney, howmuchgamble]
      "Flipcoin": [0,0,0,0],
      # [wontime, losttime, wonmoney-lostmoney, howmuchgamble]
      "Rolldice": [0,0,0,0],
      # [wontime, losttime, wonmoney-lostmoney, howmuchgamble]
      "Cupgame": [0,0,0,0],
      # [wontime, losttime, drawtime, wonmoney-lostmoney, howmuchgamble]
      "RPS": [0,0,0,0,0],
      # [wontime, losttime, drawtime, wonmoney-lostmoney, howmuchgamble]
      "ChallengeRPS": [0,0,0,0,0]
    }]
    gamblingcol.insert_many(document)
  userstats = checkgambling(username)
  if gametype == "flipcoin":
    doc = userstats['Flipcoin']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    new3 = stats[3] + doc[3]
    newdoc = [new0, new1, new2, new3]
    del userstats['Flipcoin']
    userstats['Flipcoin'] = newdoc
  if gametype == "rolldice":
    doc = userstats['Rolldice']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    new3 = stats[3] + doc[3]
    newdoc = [new0, new1, new2, new3]
    del userstats['Rolldice']
    userstats['Rolldice'] = newdoc
  if gametype == "cupgame":
    doc = userstats['Cupgame']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    new3 = stats[3] + doc[3]
    newdoc = [new0, new1, new2, new3]
    del userstats['Cupgame']
    userstats['Cupgame'] = newdoc
  if gametype == "rps":
    doc = userstats['RPS']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    new3 = stats[3] + doc[3]
    new4 = stats[4] + doc[4]
    newdoc = [new0, new1, new2, new3, new4]
    del userstats['RPS']
    userstats['RPS'] = newdoc
  if gametype == "challengerps":
    doc = userstats['ChallengeRPS']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    new3 = stats[3] + doc[3]
    new4 = stats[4] + doc[4]
    newdoc = [new0, new1, new2, new3, new4]
    del userstats['ChallengeRPS']
    userstats['ChallengeRPS'] = newdoc
  gamblingcol.delete_one({"Username": username})
  gamblingcol.insert_many([userstats])

def checkxpstats(username):
  myquery = { "Username": username }
  mydoc = xpstatscol.find(myquery)
  for x in mydoc:
    return x
  document = {
    "Username": username,
    # [times won, times lost, xp earned]
    "MenCalc": [0,0,0],
    # [times won, times lost, xp earned]
    "Trivia": [0,0,0],
    # [times won, times lost, xp earned]
    "Unscramble": [0,0,0]
  }
  return document

def addxpstats(username, gametype, stats):
  if checkxpstats(username) == False:
    document = [{
    "Username": username,
    # [times won, times lost, money earned]
    "MenCalc": [0,0,0],
    # [times won, times lost, money earned]
    "Trivia": [0,0,0],
    # [times won, times lost, money earned]
    "Unscramble": [0,0,0]
    }]
    xpstatscol.insert_many(document)
  userstats = checkxpstats(username)
  if gametype == "mencalc":
    doc = userstats['MenCalc']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    newdoc = [new0, new1, new2]
    del userstats['MenCalc']
    userstats['MenCalc'] = newdoc
  if gametype == "trivia":
    doc = userstats['Trivia']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    newdoc = [new0, new1, new2]
    del userstats['Trivia']
    userstats['Trivia'] = newdoc
  if gametype == "unscramble":
    doc = userstats['Unscramble']
    new0 = stats[0] + doc[0]
    new1 = stats[1] + doc[1]
    new2 = stats[2] + doc[2]
    newdoc = [new0, new1, new2]
    del userstats['Unscramble']
    userstats['Unscramble'] = newdoc
  xpstatscol.delete_one({"Username": username})
  xpstatscol.insert_many([userstats])

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
    "Description": None,
    "Verified": False
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
      addgambling(username, "rps", [0, 0, 1, 0, bet])
      return "It was a draw! You did rock and the computer did rock!"
    if guess == 'paper':
      addgambling(username, "rps", [1, 0, 0, bet*2, bet])
      addmoney(username, bet*2)
      return "You won! You did paper and the computer did rock!"
    if guess == 'scissors':
      addgambling(username, "rps", [0, 1, 0, -1*bet, bet])
      addmoney(username, bet*-1)
      return "You lost! You did scissors and computer did rock!"
  if comp == 'paper':
    if guess == 'rock':
      addgambling(username, "rps", [0, 1, 0, -1*bet, bet])
      addmoney(username, bet*-1)
      return "You lost! You did rock and the computer did paper!"
    if guess == 'paper':
      addgambling(username, "rps", [0, 0, 1, 0, bet])
      return "It was a draw! You did paper and the computer did paper!"
    if guess == 'scissors':
      addgambling(username, "rps", [1, 0, 0, bet*2, bet])
      addmoney(username, bet*2)
      return "You won! You did scissors and the computer did paper!"
  if comp == 'scissors':
    if guess == 'rock':
      addgambling(username, "rps", [1, 0, 0, bet*2, bet])
      addmoney(username, bet*2)
      return "You won! You did rock and the computer did scissors!"
    if guess == 'paper':
      addgambling(username, "rps", [0, 1, 0, -1*bet, bet])
      addmoney(username, bet*-1)
      return "You lost! You did paper and the computer did rock!"
    if guess == 'scissors':
      addgambling(username, "rps", [0, 0, 1, 0, bet])
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
    addgambling(username, "cupgame", [1,0,bet*3, bet])
    addmoney(username, bet*3)
    return f"You won! The ball landed in cup {answer}!"
  else:
    addgambling(username, "cupgame", [0,1,bet*-1, bet])
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
    addgambling(username, "rolldice", [1,0,bet*6, bet])
    addmoney(username, bet*6)
    return f"You won! The dice rolled {answer}!"
  else:
    addgambling(username, "rolldice", [0,1,bet*-1, bet])
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
    addgambling(username, "flipcoin", [1,0,bet*2, bet])
    addmoney(username, bet*2)
    return f"You won! The coin flipped {answer}!"
  else:
    addgambling(username, "flipcoin", [0,1,bet*-1, bet])
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
    if thetype == 3:
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

def randomword():
  word = random.choice(words)
  return word

def shuffleword(word):
  word = list(word)
  random.shuffle(word)
  shuffle = ''.join(word)
  return shuffle

def getnotifs(username):
  myquery = { "Username": username }
  mydoc = notifscol.find(myquery)
  notifs = []
  for x in mydoc:
    notifs.append(x)
  return notifs

def getnotifsnotseen(username):
  myquery = { "Username": username }
  mydoc = notifscol.find(myquery)
  notifs = []
  for x in mydoc:
    if x['Seen'] == False:
      notifs.append(x)
  notifs.reverse()
  return notifs

def addnotif(username, notif, typename):
  if isinstance(typename, dict):
    if typename['Type'] == 'RPS':
      notifdoc = {"Username": username, "Seen": False, "Type": "RPS", "Symbol": typename['Symbol'], "Bet": typename['Bet'], "User": typename['User']}
  else:
    notifdoc = {"Username": username, "Notification": notif, "Seen": False, "Type": "Normal"}
  notifscol.insert_many([notifdoc])
  return True

def clearnotifs(username):
  notifs = getnotifs(username)
  for notif in notifs:
    delete = {"_id": notif['_id']}
    notifscol.delete_one(delete)
  return True

def allseen(username):
  notifs = getnotifs(username)
  myquery = { "Username": username }
  newvalues = { "$set": { "Seen": True } }
  notifscol.update_many(myquery, newvalues)
  return True

def challengerps(username, enemy, bet, symbol):
  try:
    bet = int(bet)
    if getuser(enemy) == False:
      return f"{enemy} is not a real user!"
    if enemy == username:
      return "You cannot challenge yourself!"
    if bet > getuser(enemy)['Money']:
      return f"{enemy} does not have {str(bet)}!"
    if bet > getuser(username)['Money']:
      return f"You don't have {str(bet)}!"
    thedict = {"Type": "RPS", "Symbol": symbol, "Bet": bet, "User": username}
    addnotif(enemy, None, thedict)
    addnotif(username, f"You challenged {enemy} to a RPS game for ∆{str(bet)}!", "Normal")
    return True
  except:
    return f"{bet} is not a number!"

def getchallenge(theid):
  mydoc = notifscol.find({"_id": ObjectId(theid)})
  if mydoc == None or mydoc == False or mydoc == []:
    return False
  thedoc = []
  for x in mydoc:
    thedoc.append(x)
  challengedoc = thedoc[0]
  return challengedoc

def denychallenge(username, theid):
  challengedoc = getchallenge(theid)
  if challengedoc == False:
    return "That is not a real challenge!"
  if challengedoc['Username'] != username:
    return "You cannot deny this challenge as it has not been directed to you!"
  challengesender = challengedoc['User']
  addnotif(username, f"You rejected {challengesender}'s challenge to a {challengedoc['Type']} game for ∆{str(challengedoc['Bet'])}!", "Normal")
  addnotif(challengesender, f"{username} rejected your challenged to a {challengedoc['Type']} game for ∆{str(challengedoc['Bet'])}!", "Normal")
  notifscol.delete_one({"_id": ObjectId(theid)})
  return True

def acceptchallengefuncfunc(user2symbol, user1symbol, user2, user1, bet, theid):
  if user2symbol == 'rock':
    if user1symbol == 'rock':
      addgambling(user1, "challengerps", [0,0,1,0,bet])
      addgambling(user2, "challengerps", [0,0,1,0,bet])
      addnotif(user1, f"The RPS game between you and {user2} was a draw! You didn't win or lose anything!", "Normal")
      addnotif(user2, f"The RPS game between you and {user1} was a draw! You didn't win or lose anything!", "Normal")
    if user1symbol == 'paper':
      addgambling(user1, "challengerps", [1,0,0,bet,bet])
      addgambling(user2, "challengerps", [0,1,0,bet*-1,bet])
      addmoney(user1, bet)
      addmoney(user2, bet*-1)
      addnotif(user1, f"You won the RPS game between you and {user2}! You won ∆{str(bet)}!", "Normal")
      addnotif(user2, f"You lost the RPS game between you and {user1}! You lost ∆{str(bet)}!", "Normal")
    if user1symbol == 'scissors':
      addgambling(user1, "challengerps", [0,1,0,bet*-1,bet])
      addgambling(user2, "challengerps", [1,0,0,bet,bet])
      addmoney(user1, bet*-1)
      addmoney(user2, bet)
      addnotif(user1, f"You lost the RPS game between you and {user2}! You lost ∆{str(bet)}!", "Normal")
      addnotif(user2, f"You won the RPS game between you and {user1}! You won ∆{str(bet)}!", "Normal")
  if user2symbol == 'paper':
    if user1symbol == 'rock':
      addgambling(user1, "challengerps", [0,1,0,bet*-1,bet])
      addgambling(user2, "challengerps", [1,0,0,bet,bet])
      addmoney(user1, bet*-1)
      addmoney(user2, bet)
      addnotif(user1, f"You lost the RPS game between you and {user2}! You lost ∆{str(bet)}!", "Normal")
      addnotif(user2, f"You won the RPS game between you and {user1}! You won ∆{str(bet)}!", "Normal")
    if user1symbol == 'paper':
      addgambling(user1, "challengerps", [0,0,1,0,bet])
      addgambling(user2, "challengerps", [0,0,1,0,bet])
      addnotif(user1, f"The RPS game between you and {user2} was a draw! You didn't win or lose anything!", "Normal")
      addnotif(user2, f"The RPS game between you and {user1} was a draw! You didn't win or lose anything!", "Normal")
    if user1symbol == 'scissors':
      addgambling(user1, "challengerps", [1,0,0,bet,bet])
      addgambling(user2, "challengerps", [0,1,0,bet*-1,bet])
      addmoney(user1, bet)
      addmoney(user2, bet*-1)
      addnotif(user1, f"You won the RPS game between you and {user2}! You won ∆{str(bet)}!", "Normal")
      addnotif(user2, f"You lost the RPS game between you and {user1}! You lost ∆{str(bet)}!", "Normal")
  if user2symbol == 'scissors':
    if user1symbol == 'rock':
      addgambling(user1, "challengerps", [1,0,0,bet,bet])
      addgambling(user2, "challengerps", [0,1,0,bet*-1,bet])
      addmoney(user1, bet)
      addmoney(user2, bet*-1)
      addnotif(user1, f"You won the RPS game between you and {user2}! You won ∆{str(bet)}!", "Normal")
      addnotif(user2, f"You lost the RPS game between you and {user1}! You lost ∆{str(bet)}!", "Normal")
    if user1symbol == 'paper':
      addgambling(user1, "challengerps", [0,1,0,bet*-1,bet])
      addgambling(user2, "challengerps", [1,0,0,bet,bet])
      addmoney(user1, bet*-1)
      addmoney(user2, bet)
      addnotif(user1, f"You lost the RPS game between you and {user2}! You lost ∆{str(bet)}!", "Normal")
      addnotif(user2, f"You won the RPS game between you and {user1}! You won ∆{str(bet)}!", "Normal")
    if user1symbol == 'scissors':
      addgambling(user1, "challengerps", [0,0,1,0,bet])
      addgambling(user2, "challengerps", [0,0,1,0,bet])
      addnotif(user1, f"The RPS game between you and {user2} was a draw! You didn't win or lose anything!", "Normal")
      addnotif(user2, f"The RPS game between you and {user1} was a draw! You didn't win or lose anything!", "Normal")
  notifscol.delete_one({"_id": ObjectId(theid)})

def changeblockname(username, newname):
  user = getuser(username)
  if len(newname) > 15:
    return "Your pet block's name cannot be more than 16 letters long!"
  if set(newname).difference(printable):
    return "Your pet block's name cannot include any special letters!"
  del user['BlockName']
  user['BlockName'] = newname
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user])
  addlog(f"{username} changed their block name to {newname}")
  return True

def changedesc(username, desc):
  user = getuser(username)
  if len(desc) > 159:
    return "Your description cannot be more than 160 letters long!"
  if set(desc).difference(printable):
    return "Your description cannot include any special letters!"
  del user['Description']
  user['Description'] = desc
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user])
  addlog(f"{username} changed their description")
  return True

def addlog(log):
  file_object = open('.log', 'a')
  x = str(datetime.datetime.now())
  file_object.write(f'{x}: {log}\n')
  file_object.close()

def changeemail(username, email):
  user = getuser(username)
  emailold = user.get("Email", None)
  if emailold == email:
    return True
  if checkemailalready(email) == True:
    return "This email is already being used by someone else!"
  if emailold != None:
    del user['Email']
  user['Email'] = email
  if user.get("Verified", False) != False:
    del user['Verified']
  user['Verified'] = False
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user])
  document = {
    "Username": username
  }
  theid = verificationcol.insert(document)
  func = send_mail(email, username, str(theid))
  if func == True:
    return True
  else:
    return func


def verify(username, theid):
  myquery = {"_id": ObjectId(theid)}
  mydoc = verificationcol.find(myquery)
  for x in mydoc:
    if x['Username'] == username:
      verificationcol.delete_one({"_id": x['_id']})
      user = getuser(username)
      del user['Verified']
      user['Verified'] = True
      profilescol.delete_one({"Username": username})
      profilescol.insert_many([user])
      return True
  return False