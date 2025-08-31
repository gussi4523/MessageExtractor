from src.NotionAPI.NotionAPi import Notion

notion = Notion()

if notion.findLead(phone="+1 (647) 303-6484"):
    print("succes")
else:
    print("fail")