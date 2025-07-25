import requests
import urwid
from pyngrok import ngrok
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPEN_PHONE_API_KEY")

def create_webhook(api_key, webhook_url, webhook_type="calls", events=None):
    """
    Create a webhook endpoint for specific event types
    webhook_type can be: 'calls', 'messages', 'call-summaries', 'call-transcripts'
    """
    url = f"https://api.openphone.com/v1/webhooks/{webhook_type}"
    
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    
    # Default events
    if events is None:
        default_events = {
            "calls": ["call.ringing", "call.completed", "call.recording.completed"],
            "messages": ["message.received", "message.delivered"],
            "call-summaries": ["call.summary.completed"],
            "call-transcripts": ["call.transcript.completed"]
        }
        events = default_events.get(webhook_type, [])

    payload = {
        'url': webhook_url,
        'events': events
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        webhook_data = response.json()
        print("✅ Webhook created successfully!")
        print(f"🔗 Webhook ID: {webhook_data.get('data', {}).get('id')}")
        return webhook_data
    else:
        print(f"❌ Error creating webhook: {response.status_code}")
        try:
            print(response.json())
        except Exception:
            print(response.text)
        return None

def delete_webhook(api_key, webhook_id):
    url = f"https://api.openphone.com/v1/webhooks/{webhook_id}"
    headers = {
        "Authorization": f"{api_key}"
    }

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"✅ Deleted webhook {webhook_id}")
    else:
        print(f"❌ Failed to delete webhook {webhook_id}: {response.status_code}")
        print(response.text)

def create_transcription_webhook(api_key, webhook_url):
    url = "https://api.openphone.com/v1/webhooks/call-transcripts"
    
    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": webhook_url,
        "events": ["call.transcript.completed"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        data = response.json()
        print("✅ Transcription webhook created!")
        print("Webhook ID:", data.get("data", {}).get("id"))
        return data
    else:
        print("❌ Failed to create transcription webhook:", response.status_code)
        print(response.text)
        return None

def list_webhooks(api_key):
    url = "https://api.openphone.com/v1/webhooks"
    headers = {
        "Authorization": f"{api_key}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        webhooks = response.json().get("data", [])
        for wh in webhooks:
            print(f"Webhook ID: {wh.get('id')}")
            print(f"  URL: {wh.get('url')}")
            print(f"  Events: {wh.get('events')}")
            print(f"  Created At: {wh.get('createdAt')}")
            print("-" * 40)
        return webhooks
    else:
        print("Failed to list webhooks:", response.status_code, response.text)
        return None

def AutoSetup():
    public_url = ngrok.connect(5000)
    main_url = str(public_url.public_url) + "/openphone-webhook"
    wed_hooks = list_webhooks(API_KEY)
    if not any(wh.get("url") == str(main_url) for wh in wed_hooks):
        print("Webhook not found. Create it now.")
        create_transcription_webhook(api_key=API_KEY,webhook_url=main_url)
        ##
        ### For calls webhook
        create_webhook(API_KEY, main_url, "calls")
        ##
        ### For messages webhook  
        create_webhook(API_KEY, main_url, "messages")



#
#while True:
#    command = input("Option:")
#
#    if command == "add":
#        WEBHOOK_URL = input("URL: ")
#        list_webhooks(api_key=API_KEY)
#        create_transcription_webhook(api_key=API_KEY,webhook_url=WEBHOOK_URL)
#        ##
#        ### For calls webhook
#        create_webhook(API_KEY, WEBHOOK_URL, "calls")
#        ##
#        ### For messages webhook  
#        create_webhook(API_KEY, WEBHOOK_URL, "messages")
#    elif command == "delete":
#        WEBHOOK_URL = input("webhook:")
#        delete_webhook(api_key=API_KEY,webhook_id=WEBHOOK_URL)
#        #
#        list_webhooks(api_key=API_KEY)
#    elif command == "list":
#        list_webhooks(api_key=API_KEY)
#    elif command == "exit":
#        break