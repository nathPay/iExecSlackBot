# import gspread
import os
import json
import requests
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from tinydb import TinyDB, Query
from jinja2 import Template

db = TinyDB('./db.json')

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(SLACK_BOT_TOKEN)

CONFLUENCE_TOKEN = os.environ["CONFLUENCE_TOKEN"]

userEmail = os.environ["CONFLUENCE_USER_EMAIL"]

homePageID = "955172"
meetingPageID = "1403125859"
headersAccept = {
   "Accept": "application/json",
}

headersBoth = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

baseUrl = "https://iexecproject.atlassian.net"
urlContent = "https://iexecproject.atlassian.net/wiki/rest/api/content/"

pageContent = '<p></p><p><strong>Vendredi</strong>10/01</p><table data-layout="default" class="confluenceTable"><colgroup><col style="width: 90.0px;"></col><col style="width: 363.0px;"></col><col style="width: 167.0px;"></col><col style="width: 140.0px;"></col></colgroup><tbody><tr><th class="confluenceTh"><p style="text-align: center;"></p></th><td data-highlight-colour="#f4f5f7" class="confluenceTd"><p style="text-align: center;"><strong>Daily notes</strong></p></td><td data-highlight-colour="#f4f5f7" class="confluenceTd"><p style="text-align: center;"><strong>Blockers</strong></p></td><th class="confluenceTh"><p></p></th></tr></tbody></table>'



CHANNEL = '????'

def getMembers():
    payload = {'token': SLACK_BOT_TOKEN, 'channel': CHANNEL}
    r = requests.get('https://slack.com/api/conversations.members', params=payload)
    return r.text

def getUsername(id):
    payload = {'token': SLACK_BOT_TOKEN, 'user': id}
    r = requests.get('https://slack.com/api/users.info', params=payload)
    return r.text

def genNewSprint(sprintScrumMaster, sprintStart, sprintEnd):
    with open('newSprint.html.j2', 'r') as file:
        sprintPageTpl = file.read()
        sprint = Template(sprintPageTpl);
        res = sprint.render(SPRINT_SCRUM_MASTER=sprintScrumMaster, SPRINT_START=sprintStart, SPRINT_END=sprintEnd)
    return res

def genNewDay():
    with open('newDay.html.j2', 'r') as file:
        dayTpl = file.read()
        day = Template(dayTpl);
        res = day.render(DAY_NAME="vendredi", DAY_DATE="10/01")
    return res

def insertNewDay():
    return ""

def insertNewReport():
    return ""

def genNewReport():
    return ""

def getCurrentSprintPageContentOf(id):
    response = requests.request(
        "GET",
        urlContent + id + "?expand=body.storage",
        headers=headersAccept,
        auth=(userEmail,CONFLUENCE_TOKEN)
    )
    return json.loads(response.text)["body"]["storage"]["value"]

def updatePage(id, data):
    
    return ""

def getVersionOf(id):
    response = requests.request(
        "GET",
        urlContent+id,
        headers=headersAccept,
        auth=(userEmail,CONFLUENCE_TOKEN)
    )
    return json.loads(response.text)["version"]["number"]

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
    
    version = getCurrentSprintPageContentOf("1404829697")

    # sprint = genNewSprint("Nathan", "Mercredi 08/07", "Jeudi 09/07")
    # data = json.dumps({
    #     "title": "test",
    #     "type": "page",
    #     "space": {
    #         "key": "IP"
    #     },
    #     "ancestors": [
    #         {
    #         "id": meetingPageID
    #         }
    #     ],
    #     "body": {
    #         "storage": {
    #             "value": sprint,
    #             "representation": "storage"
    #         }
    #     }
    # })
    # response = requests.request(
    #     "POST",
    #     urlContent,
    #     data=data,
    #     headers=headersBoth,
    #     auth=(userEmail,CONFLUENCE_TOKEN)
    # )
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(",", ": ")))
    print(version)

slack_events_adapter.start(port=3030)