from notion_client import Client
from dotenv import load_dotenv
import json
import os

load_dotenv()

API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID  = os.getenv("DATABASE_ID")
DATABASE_ID_L  = os.getenv("DATABASE_ID_L")

class Notion():
    def __init__(self):
        self.notion = Client(auth=API_KEY)
        self.DB_Log = DATABASE_ID
        self.DB_Lead = DATABASE_ID_L

    def createPage(self,Time,Text,LeadID,Mark= None):
        properties = {
            "Time": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": Time
                        }
                    }
                ]
            },
            "Notes": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": Text  # змінна або рядок
                        }
                    }
                ]
            }
        }

        # Add Leads relation only if LeadID is not None or empty string
        if LeadID:
            properties["Leads"] = {
                "type": "relation",
                "relation": [
                    {
                        "id": LeadID
                    }
                ]
            }

        if Mark:
            properties["Team"] = {
                "type": "relation",
                "relation": [
                    {
                        "id": Mark
                    }
                ]
            }

        page = self.notion.pages.create(
            parent={"database_id": self.DB_Log},
            properties=properties,
            icon={
                "type": "external",
                "external": {
                    "url": "https://www.notion.so/icons/telephone_red.svg"
                }
            }
        )

        print("Page created:", page)
        
    def findLead(self,Phone):

        response_Phone = self.notion.databases.query(
            database_id=self.DB_Lead,
            filter={
                "property": "Phone number",  # must match the name of your title property
                "phone_number": {
                    "equals": Phone
                }
            }
        )

        
        results = response_Phone.get("results", [])
        if results:
            return results[0]["id"]  # ✅ return just the page ID
        return None  # ❗ no match found
