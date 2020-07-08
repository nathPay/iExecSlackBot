# create file:
headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

baseUrl = "https://iexecproject.atlassian.net"
urlContent = "https://iexecproject.atlassian.net/wiki/rest/api/content/"

data = json.dumps({
    "title": "test",
    "type": "page",
    "space": {
        "key": "IP"
    },
    "ancestors": [
        {
        "id": meetingPageID
        }
    ],
    "body": {
        "storage": {
            "value": sprint,
            "representation": "storage"
        }
    }
})
response = requests.request(
    "POST",
    urlContent,
    data=data,
    headers=headers,
    auth=(userEmail,CONFLUENCE_TOKEN)
)

# Update File:
headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

baseUrl = "https://iexecproject.atlassian.net"
urlContent = "https://iexecproject.atlassian.net/wiki/rest/api/content/{id}"

data = json.dumps({
    "version":{
        "number": ????
    }
    "title": "test",
    "type": "page",
    "status": "current",
    "ancestors": [
        {
        "id": meetingPageID
        }
    ],
    "body": {
        "storage": {
            "value": sprint,
            "representation": "storage"
        }
    }
})
response = requests.request(
    "PUT",
    urlContent,
    data=data,
    headers=headers,
    auth=(userEmail,CONFLUENCE_TOKEN)
)