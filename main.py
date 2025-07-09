# main.py
from flask import Flask, request
from src.NotionAPI.NotionAPi import Notion
from src.TextOperations.TextOperator import split_text_n_parts

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

        notion_API.createPage(timestamp,message_text,notion_API.findLead(Phone=sender_number))

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

            if status == "no-answer" and direction == "incoming":
                notion_API.createPage(completed_at,"Call missed",notion_API.findLead(Phone=caller_number))

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

        notion_API.createPage(timestamp, recording_url, notion_API.findLead(caller_number))

    elif event_type == "call.transcript.completed":
        print("📞 call.transcript.completed received")

        dialogue = event_data.get("dialogue", [])
        call_id = event_data.get("callId")
        created_at = event_data.get("createdAt")

        if not dialogue:
            print("📝 No transcription available (empty dialogue)")
        else:
            full_text = " ".join([part.get("content", "") for part in dialogue])
            if len(full_text) > 1999:
                splited_text = split_text_n_parts(full_text,int(len(full_text)/1000))
                for text in splited_text:
                    print("📝 Transcription text:", text)
                    notion_API.createPage(created_at, text, notion_API.findLead(call_id))
            else:
                notion_API.createPage(created_at, full_text, notion_API.findLead(call_id))

        

    elif event_type.strip() == "message.delivered":
        print(f"📩 Message from {event_data.get('from')}: {event_data.get('text')}")
        print(" ")
        print("Mark?")

        # Extract message details
        sender_number = event_data.get("from")
        message_text = event_data.get("text")
        timestamp = event_data.get("createdAt")

        notion_API.createPage(timestamp,message_text,notion_API.findLead(Phone=sender_number),Mark="1fedfa6161aa802f9b36cdb9a3283a34")

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
