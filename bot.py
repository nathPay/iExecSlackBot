# import gspread
import os
import json
import requests
import config
import schedule
import time
import slackdown

from slackeventsapi import SlackEventAdapter
from slack import WebClient
from tinydb import TinyDB, Query
from jinja2 import Template
from threading import Thread
import datetime

db = TinyDB('./db.json')

Q = Query()
members = db.table('members')
sprints = db.table('sprints')

slack_events_adapter = SlackEventAdapter(config.SLACK_SIGNING_SECRET, "/slack/events")

slack_client = WebClient(config.SLACK_BOT_TOKEN)

homePageID = "955172"
meetingPageID = "1403125859"

headersAccept = {
   "Accept": "application/json",
}

headersBoth = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

pageContent = '<p></p><p><strong>Vendredi</strong>10/01</p><table data-layout="default" class="confluenceTable"><colgroup><col style="width: 90.0px;"></col><col style="width: 363.0px;"></col><col style="width: 167.0px;"></col><col style="width: 140.0px;"></col></colgroup><tbody><tr><th class="confluenceTh"><p style="text-align: center;"></p></th><td data-highlight-colour="#f4f5f7" class="confluenceTd"><p style="text-align: center;"><strong>Daily notes</strong></p></td><td data-highlight-colour="#f4f5f7" class="confluenceTd"><p style="text-align: center;"><strong>Blockers</strong></p></td><th class="confluenceTh"><p></p></th></tr></tbody></table>'

def getMembers():
    payload = {'token': config.SLACK_BOT_TOKEN, 'channel': config.CHANNEL}
    r = requests.get('https://slack.com/api/conversations.members', params=payload)
    return json.loads(r.text)

def getUserInfo(id):
    payload = {'token': config.SLACK_BOT_TOKEN, 'user': id}
    r = requests.get('https://slack.com/api/users.info', params=payload)
    return json.loads(r.text)

def getImChannelIDOf(id):
    payload = {'token': config.SLACK_BOT_TOKEN, 'users': id}
    r = requests.get('https://slack.com/api/conversations.open', params=payload)
    return json.loads(r.text)

def genNewSprint(sprintScrumMaster, sprintStart, sprintEnd, sprintName, sprintID):
    sprints.insert()
    with open('newSprint.html.j2', 'r') as file:
        sprintPageTpl = file.read()
        sprint = Template(sprintPageTpl)
        res = sprint.render(SPRINT_SCRUM_MASTER=sprintScrumMaster, SPRINT_START=sprintStart, SPRINT_END=sprintEnd)
    return res

def genNewDay():
    with open('newDay.html.j2', 'r') as file:
        dayTpl = file.read()
        day = Template(dayTpl)
        res = day.render(DAY_NAME="vendredi", DAY_DATE="10/01")
    return res


# Merge tout les reports la journée et le push sur confluence
def endDay():
    users = members.all()
    reports = []
    for user in users:
        if not user["is_bot"]:
            reports.append(genNewReport(user["yesterday"], user["today"], user["blockers"]))
    
    return ""

def insertNewDay():
    return ""

def insertNewReport():
    return ""

def genNewReport(yesterday, today, blockers):
    with open('newSprint.html.j2', 'r') as file:
        reportTpl = file.read()
        report = Template(reportTpl)
        res = report.render(YESTERDAY_NOTES=yesterday, DAY_NOTES=today, DAY_BLOCKERS=blockers)
    return res

def getCurrentSprintPageContentOf(id):
    response = requests.request(
        "GET",
        urlContent + id + "?expand=body.storage",
        headers=headersAccept,
        auth=(config.userEmail,config.CONFLUENCE_TOKEN)
    )
    return json.loads(response.text)["body"]["storage"]["value"]

def updatePage(id, data):
    
    return ""

def getVersionOf(id):
    response = requests.request(
        "GET",
        urlContent+id,
        headers=headersAccept,
        auth=(config.userEmail,config.CONFLUENCE_TOKEN)
    )
    return json.loads(response.text)["version"]["number"]

def getCurrentSprint():
    return sprints.get(doc_id=len(sprints))

def startConversationWith(user):
    if user["convState"] == 0:
        slack_client.chat_postMessage(text=config.QUESTIONS[user["convState"]], token=config.SLACK_BOT_TOKEN, channel=user["imChannelID"])
    return

# @slack_events_adapter.on('sprint')
# def result():
#     print(request) # should display 'bar'
#     return 'Received !' # response to your request.

# def test(event_data):
#     print(event_data["event"])

# Messaging part
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if members.search(Q.id.matches(message["user"])) == []:
        return
    user = members.search(Q.id.matches(message["user"]))[0]
    if user != config.BOT_ID:
        if user["convState"] == 0:
            if message["text"] != "yes" and message["text"] != "Yes":
                slack_client.chat_postMessage(text="Sorry you can only answer by yes :) please try again!", token=config.SLACK_BOT_TOKEN, channel=user["imChannelID"])
                return
            user["convState"] = user["convState"] + 1
            members.update({"convState": user["convState"]}, Q.id == user["id"])
            slack_client.chat_postMessage(text=config.QUESTIONS[user["convState"]], token=config.SLACK_BOT_TOKEN, channel=user["imChannelID"])
            return
        if user["convState"] == 1:
            user["convState"] = user["convState"] + 1
            members.update({"yesterday": slackdown.render(message['text']), "convState": user["convState"]}, Q.id == user["id"])
            slack_client.chat_postMessage(text=config.QUESTIONS[user["convState"]], token=config.SLACK_BOT_TOKEN, channel=user["imChannelID"])
            return
        if user["convState"] == 2:
            user["convState"] = user["convState"] + 1
            members.update({"today": slackdown.render(message['text']), "convState": user["convState"]}, Q.id == user["id"])
            slack_client.chat_postMessage(text=config.QUESTIONS[user["convState"]], token=config.SLACK_BOT_TOKEN, channel=user["imChannelID"])
            return
        if user["convState"] == 3:
            user["convState"] = user["convState"] + 1
            members.update({"blockers": slackdown.render(message['text']), "convState": user["convState"]}, Q.id == user["id"])
            slack_client.chat_postMessage(text=config.QUESTIONS[user["convState"]], token=config.SLACK_BOT_TOKEN, channel=user["imChannelID"])
            return
    return

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
    
    # version = getCurrentSprintPageContentOf("1404829697")

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
    #     config.urlContent,
    #     data=data,
    #     headers=headersBoth,
    #     auth=(config.userEmail,config.CONFLUENCE_TOKEN)
    # )
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(",", ": ")))
    # print(version)

def run_daily_meeting():
    channelMember = getMembers()
    for el in channelMember["members"]:
        if(members.search(Q.id.matches(el)) == []):
            imChannelID = getImChannelIDOf(el)
            tmpUser = getUserInfo(el)["user"]
            tmpUser["imChannelID"] = imChannelID["channel"]["id"]
            tmpUser["convState"] = 0
            tmpUser["yesterday"] = ""
            tmpUser["today"] = ""
            tmpUser["blockers"] = ""
            tmpUser["profile"] = ""
            members.insert(tmpUser)
    weekno = datetime.datetime.today().weekday()
#     if weekno >= 5:
#         return 
#     for el in members.all():
#         startConversationWith(el)
#     return

run_daily_meeting()
user = members.search(Q.id.matches("UCZFH9ZHR"))[0]
startConversationWith(user)
print(user)
# def dailyThread():
#     schedule.every().day.at(config.TIME).do(run_daily_meeting)
#     #  \
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def dayEndThread():
#     schedule.every().day.at("19:00").do(endDay)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# thread = Thread(target=dailyThread).start()
# thread = Thread(target=dayEndThread).start()

slack_events_adapter.start(port=3030)