import discord
import os
import requests
import json
import random
from replit import db
from keep_wake import keep_wake


intents = discord.Intents.default()
client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable","failer", "unsuccessful", "ugly", "stupid", "dumb", "bad", "suck", "stink", "poor"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!",
  "You are amazing!",
  "you will be succesful",
  "you are beautiful",
  "Everyone make mistakes"
]

if "responding" not in db.keys():
  db["responding"] = True
  
def get_qoute():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  qoute = json_data[0]['q'] + " -" + json_data[0]['a']
  return(qoute)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  
  if message.content.startswith('$inspire me'):
    quote = get_qoute()
    await message.channel.send(quote)
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])
  
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
        db["responding"] = False
        await message.channel.send("Responding is off.")

keep_wake()
client.run('MTE4MjY3MzUxMjQyMzQ5NzgxOA.GAoT24.yeu2JJjW6l0iuqu4tk6OWquxKazWWTxNqtPKw0')
