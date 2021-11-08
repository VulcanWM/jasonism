from flask import Flask, render_template, redirect, request
import datetime
from functions import getcookie, makeaccount, addcookie, getuser, gethashpass, delcookies, makeblockbigger, getquestion, addxpmoney, cupgame, flipcoin, rps, rolldice, mencalc, upgradeblock, randomword, shuffleword, words, getnotifs, clearnotifs, allseen, challengerps, denychallenge, getchallenge, acceptchallengefuncfunc, checkgambling, changeblockname, changedesc, addxpstats, checkxpstats
import os
import random
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route("/")
def index():
  if getcookie("User") == False:
    return render_template("index.html", user=False)
  else:
    return render_template("index.html", user=getuser(getcookie("User")))

@app.route("/signup")
def signuppage():
  if getcookie("User") == False:
    return render_template("signup.html")
  else:
    return redirect("/")
  
@app.route("/signup", methods=['POST', 'GET'])
def signupfunc():
  if request.method == 'POST':
    if getcookie("User") != False:
      return redirect("/")
    username = request.form['username']
    password = request.form['password']
    passwordagain = request.form['passwordagain']
    func = makeaccount(username, password, passwordagain)
    if func == True:
      addcookie("User", username)
      return redirect("/")
    else:
      return render_template("signup.html", error=func)

@app.route("/login")
def loginpage():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    return redirect("/")

@app.route("/login", methods=['POST', 'GET'])
def loginfunc():
  if request.method == 'POST':
    if getcookie("User") != False:
      return render_template("login.html", error="You have already logged in!")
    username = request.form['username']
    if getuser(username) == False:
      return render_template("login.html", error="That is not a username!")
    password = request.form['password']
    if check_password_hash(gethashpass(username), password) == False:
      return render_template("login.html", error="Wrong password!")
    addcookie("User", username)
    return redirect("/")
  else:
    return redirect("/")

@app.route("/logout")
def logout():
  if getcookie("User") == False:
    return redirect("/")
  else:
    delcookies()
    return redirect("/")

@app.route("/profile")
def profile():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    user = getuser(getcookie("User"))
    level = str(int(user['XP'])/1000 + 1).split(".")[0]
    user['Level'] = level
    return render_template("profile.html", user=user)

@app.route("/makeblockbigger")
def makeblockbiggerpage():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    func = makeblockbigger(getcookie("User"))
    if func == True:
      return redirect("/profile")
    else:
      user = getuser(getcookie("User"))
      level = str(int(user['XP'])/1000 + 1).split(".")[0]
      user['Level'] = level
      return render_template("profile.html", error=func, user=user)

@app.route("/trivia")
def trivia():
  if getcookie("User") == False:
    return redirect("/login")
  username = getcookie("User")
  delcookies()
  question = getquestion()['results'][0]
  answers1 = [question['correct_answer']] + question['incorrect_answers']
  addcookie("User", username)
  addcookie("Difficulty", question['difficulty'])
  addcookie("Answer", question['correct_answer'])
  accquestion = question['question']
  accquestion = accquestion.replace("&", "")
  accquestion = accquestion.replace(";", "")
  accquestion = accquestion.replace("#039", "'")
  accquestion = accquestion.replace("quot", "")
  answers = []
  for answer in answers1:
    answer = answer.replace("&", "")
    answer = answer.replace(";", "")
    answer = answer.replace("#039", "'")
    answer = answer.replace("quot", "")
    answers.append(answer)
    random.shuffle(answers)
  return render_template("trivia.html", answers=answers, question=accquestion, user=getuser(username))

@app.route("/trivia/<guess>")
def triviaanswer(guess):
  if getcookie("User") == False:
    return redirect("/login")
  if getcookie("Answer") == False:
    return redirect("/trivia")
  if getcookie("Answer") == guess:
    xps = {"hard": 50, "medium": 40, "easy": 30}
    moneys = {"hard": 500, "medium": 400, "easy": 300}
    difficulty = getcookie("Difficulty")
    xp = xps[difficulty]
    money = moneys[difficulty]
    addxpstats(getcookie("User"), "trivia", [1,0,xp])
    addxpmoney(getcookie("User"), xp, money)
  else:
    addxpstats(getcookie("User"), "trivia", [0,1,0])
  return redirect("/trivia")

@app.route("/trivia/<guess>/<guess2>")
def triviaanswerwithslash(guess, guess2):
  if getcookie("User") == False:
    return redirect("/login")
  if getcookie("Answer") == False:
    return redirect("/trivia")
  guess = guess + "/" + guess2
  if getcookie("Answer") == guess:
    xps = {"hard": 50, "medium": 40, "easy": 30}
    moneys = {"hard": 500, "medium": 400, "easy": 300}
    difficulty = getcookie("Difficulty")
    xp = xps[difficulty]
    money = moneys[difficulty]
    addxpmoney(getcookie("User"), xp, money)
  return redirect("/trivia")


@app.route("/cupgame")
def cupgamepage():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    return render_template("cupgame.html", user=getuser(getcookie("User")))

@app.route("/cupgame/<guess>/<bet>")
def cupgamefunc(guess, bet):
  if getcookie("User") == False:
    return redirect("/login")
  func = cupgame(getcookie("User"), guess, bet)
  return render_template("cupgame.html", error=func, user=getuser(getcookie("User")))

@app.route("/cupgame/<guess>/")
def cupgameerror(guess):
  if getcookie("User") == False:
    return redirect("/login")
  return render_template("cupgame.html", error="You have to enter a bet amount!", user=getuser(getcookie("User")))

@app.route("/flipcoin")
def flipcoinpage():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    return render_template("flipcoin.html", user=getuser(getcookie("User")))

@app.route("/flipcoin/<guess>/<bet>")
def flipcoinfunc(guess, bet):
  if getcookie("User") == False:
    return redirect("/login")
  func = flipcoin(getcookie("User"), guess, bet)
  return render_template("flipcoin.html", error=func, user=getuser(getcookie("User")))

@app.route("/flipcoin/<guess>/")
def flipcoinerror(guess):
  if getcookie("User") == False:
    return redirect("/login")
  return render_template("flipcoin.html", error="You have to enter a bet amount!", user=getuser(getcookie("User")))

@app.route("/rps")
def rpspage():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    return render_template("rps.html", user=getuser(getcookie("User")))

@app.route("/rps/<guess>/<bet>")
def rpsfunc(guess, bet):
  if getcookie("User") == False:
    return redirect("/login")
  func = rps(getcookie("User"), guess, bet)
  return render_template("rps.html", error=func, user=getuser(getcookie("User")))

@app.route("/rps/<guess>/")
def rpserror(guess):
  if getcookie("User") == False:
    return redirect("/login")
  return render_template("rps.html", error="You have to enter a bet amount!", user=getuser(getcookie("User")))

@app.route("/rolldice")
def rolldicepage():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    return render_template("rolldice.html", user=getuser(getcookie("User")))

@app.route("/rolldice/<guess>/<bet>")
def rolldicefunc(guess, bet):
  if getcookie("User") == False:
    return redirect("/login")
  func = rolldice(getcookie("User"), guess, bet)
  return render_template("rolldice.html", error=func, user=getuser(getcookie("User")))

@app.route("/rolldice/<guess>/")
def rolldiceerror(guess):
  if getcookie("User") == False:
    return redirect("/login")
  return render_template("rolldice.html", error="You have to enter a bet amount!", user=getuser(getcookie("User")))

@app.route("/mencalc")
def mencalcpage():
  if getcookie("User") == False:
    return redirect("/login")
  ques = mencalc()
  return render_template("mencalc.html", question=ques, user=getuser(getcookie("User")))

@app.route("/mencalc", methods=['POST', 'GET'])
def mencalcfunc():
  if request.method == 'POST':
    if getcookie("User") == False:
      return redirect("/login")
    answer = getcookie("MathsAns")
    guess = request.form['guess']
    if answer == guess:
      addxpstats(getcookie("User"), "mencalc", [1, 0, 25])
      addxpmoney(getcookie("User"), 25, 250)
    else:
      addxpstats(getcookie("User"), "mencalc", [0,1,0])
    return redirect("/mencalc")
  else:
    return redirect("/mencalc")

@app.route("/upgradeblock/<index>")
def upgradeblockpage(index):
  if getcookie("User") == False:
    return redirect("/login")
  func = upgradeblock(getcookie("User"), index)
  if func == True:
    return redirect("/profile")
  else:
    user = getuser(getcookie("User"))
    level = str(int(user['XP'])/1000 + 1).split(".")[0]
    user['Level'] = level
    return render_template("profile.html", error=func, user=user)

@app.route("/allgames")
def allgames():
  if getcookie("User") == False:
    return render_template("allgames.html", user=False)
  else:
    return render_template("allgames.html", user=True)

@app.route("/unscrambleword")
def unscramblewordpage():
  if getcookie("User") == False:
    return redirect("/login")
  word = randomword()
  shuffle = shuffleword(word)
  addcookie("scrambletime", datetime.datetime.now(datetime.timezone.utc))
  return render_template("unscrambleword.html", shuffle=shuffle, user=getuser(getcookie("User")))

@app.route("/unscrambleword/<shuffle>", methods=['POST', 'GET'])
def unscramblewordfunc(shuffle):
  if request.method == 'POST':
    if getcookie("User") == False:
      return redirect("/login")
    if getcookie("scrambletime") == False:
      return redirect("/unscrambleword")
    word = request.form['word'].lower()
    shuffleletters = []
    for letter in shuffle:
      shuffleletters.append(letter)
    wordletters = []
    for letter in word:
      wordletters.append(letter)
    wordletters.sort()
    shuffleletters.sort()
    timenow = datetime.datetime.now(datetime.timezone.utc)
    timethen = getcookie("scrambletime")
    diff = timenow - timethen
    seconds = diff.total_seconds()
    username = getcookie("User")
    delcookies()
    addcookie("User", username)
    if seconds > 30:
      return redirect("/unscrambleword")
    if wordletters == shuffleletters:
      if word in words:
        xp = random.randint(75,100)
        addxpstats(getcookie("User"), "unscramble", [1,0,xp])
        addxpmoney(getcookie("User"), xp, xp*10)
      else:
        addxpstats(getcookie("User"), "unscramble", [0,1,0])
    return redirect("/unscrambleword")
  else:
    return redirect("/unscrambleword")

@app.route("/notifs")
def notifs():
  if getcookie("User") == False:
    return render_template("/login")
  notifs = getnotifs(getcookie("User"))
  allseen(getcookie("User"))
  return render_template("notifs.html", notifs=notifs)

@app.route("/clearnotifs")
def clearnotifsapp():
  if getcookie("User") == False:
    return render_template("/login")
  clearnotifs(getcookie("User"))
  return redirect("/notifs")

@app.route("/challengerps")
def challengerpspage():
  if getcookie("User") == False:
    return redirect("/login")
  else:
    return render_template("challengerps.html")

@app.route("/challengerps/<symbol>/<enemy>/<bet>")
def challengerpsfunc(symbol, enemy, bet):
  if getcookie("User") == False:
    return redirect("/login")
  func = challengerps(getcookie("User"), enemy, bet, symbol)
  if func == True:
    return redirect("/notifs")
  else:
    return render_template("challengerps.html", error=func)

@app.route("/denychallenge/<theid>")
def denychallengepage(theid):
  if getcookie("User") == False:
    return redirect("/login")
  denychallenge(getcookie("User"), theid)
  return redirect("/notifs")

@app.route("/acceptchallenge/<theid>")
def acceptchallengepage(theid):
  if getcookie("User") == False:
    return redirect("/login")
  challenge = getchallenge(theid)
  if challenge == False:
    return redirect("/notifs")
  if challenge['Username'] != getcookie("User"):
    return redirect("/notifs")
  return render_template("acceptchallenge.html", challenge=challenge)

@app.route("/acceptchallenge/<theid>/<symbol>")
def acceptchallengefunc(theid, symbol):
  if getcookie("User") == False:
    return redirect("/login")
  challenge = getchallenge(theid)
  if challenge == False:
    return redirect("/notifs")
  if challenge['Username'] != getcookie("User"):
    return redirect("/notifs")
  if challenge['Type'] == 'RPS':
    user2symbol = symbol
    user1symbol = challenge['Symbol']
    user2 = challenge['Username']
    user1 = challenge['User']
    bet = challenge['Bet']
    acceptchallengefuncfunc(user2symbol, user1symbol, user2, user1, bet, theid)
    return redirect("/notifs")

@app.route("/@<username>")
def user(username):
  if getcookie("User") == False:
    pass
  else:
    if getcookie("User") == username:
      return redirect("/profile")
  user = getuser(username)
  if user == False:
    return redirect("/")
  else:
    level = str(int(user['XP'])/1000 + 1).split(".")[0]
    user['Level'] = level
    return render_template("userprofile.html", user=user)

@app.route("/gamblingstats")
def gamblingstats():
  if getcookie("User") == False:
    return redirect("/login")
  stats = checkgambling(getcookie("User"))
  return render_template("gamblingstats.html", stats=stats)

@app.route("/gamblingstats/@<username>")
def gamblingstatsuser(username):
  if getcookie("User") == False:
    pass
  else:
    if getcookie("User") == username:
      return redirect("/gamblingstats")
  stats = checkgambling(username)
  return render_template("usergamblingstats.html", stats=stats)

@app.route("/settings")
def settings():
  if getcookie("User") == False:
    return redirect("/login")
  user = getuser(getcookie("User"))
  return render_template("settings.html", user=user)

@app.route("/changeblockname", methods=['GET', 'POST'])
def changeblocknamefunc():
  if request.method == 'POST':
    if getcookie("User") == False:
      return redirect("/login")
    newname = request.form['blockname']
    user = getuser(getcookie("User"))
    if user['BlockName'] == newname:
      return redirect("/settings")
    func = changeblockname(getcookie("User"), newname)
    if func == True:
      return redirect("/settings")
    else:
      return render_template("settings.html", error=func, user=user)
  else:
    return redirect("/settings")

@app.route("/changedesc", methods=['GET', 'POST'])
def changedescfunc():
  if request.method == 'POST':
    if getcookie("User") == False:
      return redirect("/login")
    desc = request.form['desc']
    user = getuser(getcookie("User"))
    if user['Description'] == desc:
      return redirect("/settings")
    func = changedesc(getcookie("User"), desc)
    if func == True:
      return redirect("/settings")
    else:
      return render_template("settings.html", error=func, user=user)
  else:
    return redirect("/settings")

@app.route("/xpstats")
def xpstats():
  if getcookie("User") == False:
    return redirect("/login")
  stats = checkxpstats(getcookie("User"))
  return render_template("xpstats.html", stats=stats)

@app.route("/xpstats/@<username>")
def xpstatsuser(username):
  if getcookie("User") == False:
    pass
  else:
    if getcookie("User") == username:
      return redirect("/xpstats")
  stats = checkgambling(username)
  return render_template("userxpstats.html", stats=stats)