import os

"""General app configuration"""

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
CHANNEL = 'C017C1G6FGW'

CONFLUENCE_TOKEN = os.environ["CONFLUENCE_TOKEN"]
userEmail = os.environ["CONFLUENCE_USER_EMAIL"]
baseUrl = "https://iexecproject.atlassian.net"
urlContent = "https://iexecproject.atlassian.net/wiki/rest/api/content/"

BOT_NAME = 'iExecDailyBot'
BOT_ID = "U015KB2GVPH"
# DAILY_MEETING_CHANNEL = '#test-dailymeetingbot'
TIME = '09:00'

USER_BLACKLIST = ['slackbot']

QUESTIONS = [
    "Are you ready start the daily meeting now?",
    "Cool, What did you complete yesterday?",
    "What are you planning to work on today?",
    "Great. Do you have any blockers? If so, just tell me. Otherwise please say: no.",
    "Cool, Daily complete :D"
]

DEFAULT_ANSWER = "Sorry I did not understand :("

