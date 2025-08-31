from notion_client import Client
from dotenv import load_dotenv
import json
import os
import re

load_dotenv()

API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID  = os.getenv("DATABASE_ID")
DATABASE_ID_L  = os.getenv("DATABASE_ID_L")

class Notion():
    def __init__(self):
        self.notion = Client(auth=API_KEY)
        self.DB_Log = DATABASE_ID
        self.DB_Lead = DATABASE_ID_L

    def createPage(self,Time,Text,LeadID,TeamMate=None,Bold=False,Color="default"):
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
                        },
                        "annotations": {
                            "bold": Bold,
                            "color": Color
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

        if TeamMate:
            properties["Team"] = {
                "type": "relation",
                "relation": [
                    {
                        "id": TeamMate
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
        

    def findTeammate(self,Phone):

        response_Phone = self.notion.databases.query(
            database_id="048ea4ad7c7144e18872e23d0c70f042",
            filter={
                "property": "Phone",  # must match the name of your title property
                "phone_number": {
                    "equals": Phone
                }
            }
        )

        
        results = response_Phone.get("results", [])
        if results:
            return results[0]["id"]  # ✅ return just the page ID
        return None  # ❗ no match found

    @staticmethod
    def normalize_phone(number: str) -> str:
        """Remove everything except digits."""
        return re.sub(r'\D', '', number) if number else ''


    def findLead(self, phone: str):
        normalized_target = self.normalize_phone(phone)
        print(normalized_target)
        all_pages = []
        next_cursor = None

        # Fetch all pages
        while True:
            response = self.notion.databases.query(
                database_id=self.DB_Lead,
                page_size=100,
                start_cursor=next_cursor
            )
            all_pages.extend(response["results"])
            if response.get("has_more"):
                next_cursor = response["next_cursor"]
            else:
                break

        print(all_pages[0]["properties"]["Phone number"]["phone_number"])
        # Search for matching phone
        for page in all_pages:
            phone_prop = self.normalize_phone(page["properties"]["Phone number"]["phone_number"])
            print(phone_prop)
            if phone_prop == normalized_target:
                #number = phone_prop.get("phone_number")
                #if number and self.normalize_phone(number) == normalized_target:
                return page["id"]  # ✅ Return the page ID

        return None  # ❗ No match found
