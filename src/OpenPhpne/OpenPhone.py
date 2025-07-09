import requests
import os 

class OpenPhone():
    
    def __init__(self,API_KEY):
        self.API_KEY = API_KEY
        self.BASE_URL = "https://api.openphone.com/v1"

    def GetConversations(self,user_id=None, phone_numbers=None, limit=100):
        endpoint = f"{self.BASE_URL}/conversations"

        headers = {
        'Authorization': self.API_KEY,
        'Content-Type': 'application/json'
        }

        conversation_summaries = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {'limit': limit}

            if user_id:
                params['userId'] = user_id

            if phone_numbers:
                params['phoneNumbers'] = phone_numbers

            if next_page_token:
                params['pageToken'] = next_page_token

            try:
                response = requests.get(endpoint, headers=headers, params=params)
                response.raise_for_status()

                data = response.json()

                # Extract specific fields from each conversation
                if 'data' in data:
                    for conversation in data['data']:
                        summary = {
                            'conversationId': conversation.get('id'),
                            'lastActivityAt': conversation.get('lastActivityAt'),
                            'lastActivityId': conversation.get('lastActivityId')
                        }
                        conversation_summaries.append(summary)

                # Check if there are more pages
                if data.get('hasNextPage') and data.get('nextPageToken'):
                    next_page_token = data['nextPageToken']
                else:
                    break

            except requests.exceptions.RequestException as e:
                print(f"Error fetching conversations: {e}")
                break
            
        return conversation_summaries
        