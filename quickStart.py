# import gspread
import os
import json
import requests
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from tinydb import TinyDB, Query

db = TinyDB('./db.json')

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(SLACK_BOT_TOKEN)

CONFLUENCE_TOKEN = os.environ["CONFLUENCE_TOKEN"]

userEmail = os.environ["CONFLUENCE_USER_EMAIL"]

headers = {
   "Accept": "application/json"
}

basUrl = "https://iexecproject.atlassian.net"
urlContent = "https://iexecproject.atlassian.net/wiki/rest/api/content/"

CHANNEL = '????'

def getMembers():
    payload = {'token': SLACK_BOT_TOKEN, 'channel': CHANNEL}
    r = requests.get('https://slack.com/api/conversations.members', params=payload)
    return r.text

def getUsername(id):
    payload = {'token': SLACK_BOT_TOKEN, 'user': id}
    r = requests.get('https://slack.com/api/users.info', params=payload)
    return r.text

# Messaging part
@slack_events_adapter.on("message")
def handle_message(event_data):
    # message = event_data["event"]
    # user = getUsername(message.get('user'))
    # user = json.loads(user)
    # print(user["user"]["real_name"])
    # If the incoming message contains "hi", then respond with a "Hello" message
    # if "yes" in message.get('event.type'):
    #     channel = message["channel"]
    #     message = "Hello <@%s>! :tada:" % message["user"]
#    slack_client.chat_postMessage(text=message)
    # print(sh.sheet1.update('A2', user["user"]["real_name"]))
    # print(sh.sheet1.update('B2', message.get('text')))
    # members = json.loads(getMembers())
    # for i in range(len(members["members"])):
    #     print(sh.sheet1.update("A"+ str(i+2), json.loads(getUsername(members["members"][i]))["user"]["real_name"]))
    response = requests.request(
        "GET",
        urlContent + '153944164?expand=body.storage',
        headers=headers,
        auth=(userEmail,CONFLUENCE_TOKEN)
    )
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(",", ": ")))

slack_events_adapter.start(port=3030)