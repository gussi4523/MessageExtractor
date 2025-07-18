from src.NotionAPI.NotionAPi import Notion

notion = Notion()

if notion.findTeammate(Phone="9055797862"):
    print("succes")
else:
    print("fail")