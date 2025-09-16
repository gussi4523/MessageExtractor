# main.py
from flask import Flask, request
from src.NotionAPI.NotionAPi import Notion
from src.TextOperations.TextOperator import split_text_n_parts
from HookSetup import AutoSetup
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
taskAI_server_url = os.getenv("AI_SERVER_URL")

AutoSetup()
notion_API = Notion()
app = Flask(__name__)

@app.route('/')
def homePage(): 
    if request.method == 'POST':
        print("⚠️ Received POST at /:", request.data)
        return '', 200
    return 'Home page'

@app.route('/openphone-webhook', methods=['POST'])
def webhook():
    data = request.json
    print("🔔 Webhook Received:", data)

    event_type = data.get("type")
    print(event_type)
    event_data = data.get("data", {}).get("object", {})

    # Example: log calls or messages
    if event_type.strip() == "message.received":
        print(f"📩 Message from {event_data.get('from')}: {event_data.get('text')}")
        print(" ")
        # Extract message details
        sender_number = event_data.get("from")
        message_text = event_data.get("text")
        timestamp = event_data.get("createdAt")
        teammate=notion_API.findTeammate(sender_number)

        if teammate:
            notion_API.createPage(timestamp,message_text,teammate)
            response = requests.post(url=taskAI_server_url,json={"event_type":event_type,
                                                         "text":message_text,
                                                         "date": str(datetime.today()),
                                                         "IDType":"Lead",
                                                         "Id":lead})
        else:
            lead = notion_API.findLead(phone=sender_number)
            notion_API.createPage(timestamp,message_text,lead)
            response = requests.post(url=taskAI_server_url,json={"event_type":event_type,
                                                         "text":message_text,
                                                         "date": str(datetime.today()),
                                                         "IDType":"Lead",
                                                         "Id":lead})

    elif event_type == "call.completed":
        if isinstance(event_data, dict):
            call = event_data
            status = call.get("status")
            direction = call.get("direction")
            answered_at = call.get("answeredAt")
            completed_at = call.get("completedAt")
            participants = call.get("participants", [])
            caller_number = participants[0] if participants else "Unknown"

            print(f"📞 Call status: {status}")
            print(f"👤 Caller: {caller_number}")
            print(f"🕒 Ended at: {completed_at}")

            lead = notion_API.findLead(phone=caller_number)

            if status == "no-answer" and direction == "incoming":
                notion_API.createPage(completed_at,"Call missed",LeadID=lead,Color="red")

        else:
            print("⚠️ Unexpected event_data format:", event_data)
        
    elif event_type.strip() == "call.recording.completed":
        call_info = event_data

        participants = call_info.get("participants", [])
        caller_number = participants[0] if participants else "Unknown"
        timestamp = call_info.get("completedAt", "Unknown")
        recordings = call_info.get("recordings", [])

        recording_url = recordings[0].get("url") if recordings else "No recording"

        print(f"📼 Call recording from {caller_number} at {timestamp}")
        print(f"🔗 Recording URL: {recording_url}")

        lead = notion_API.findLead(phone=caller_number)

        notion_API.createPage(timestamp, recording_url, lead)

    elif event_type == "call.transcript.completed":
        print("📞 call.transcript.completed received")

        dialogue = event_data.get("dialogue", [])
        call_id = event_data.get("callId")
        created_at = event_data.get("createdAt")
        lead = notion_API.findLead(call_id)
        if not dialogue:
            print("📝 No transcription available (empty dialogue)")
        else:
            full_text = " ".join([part.get("content", "") for part in dialogue])
            if len(full_text) > 1999:
                splited_text = split_text_n_parts(full_text,int(len(full_text)/1000))
                for text in splited_text:
                    print("📝 Transcription text:", text)
                    notion_API.createPage(created_at, text, lead)
            else:
                notion_API.createPage(created_at, full_text, lead)
        response = requests.post(url=taskAI_server_url,json={"event_type":event_type,
                                                         "text":text,
                                                         "date": str(datetime.today()),
                                                         "IDType":"Lead",
                                                         "Id":lead})
        print(response)

        

    elif event_type.strip() == "message.delivered":
        print(f"📩 Message from {event_data.get('from')}: {event_data.get('text')}")
        print(" ")
        print("Mark?")

        # Extract message details
        sender_number = event_data.get("from")
        message_text = event_data.get("text")
        timestamp = event_data.get("createdAt")

        lead = notion_API.findLead(phone=sender_number)

        notion_API.createPage(timestamp,message_text,lead,TeamMate="1fedfa6161aa802f9b36cdb9a3283a34")
        print(response)

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)