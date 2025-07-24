import requests
import os
from dotenv import load_dotenv

import os
from dotenv import load_dotenv

# Only load .env if it exists and we're not on Render
if os.path.exists(".env") and not os.environ.get("RENDER"):
    load_dotenv()

API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")


def get_board_cards(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        'key': API_KEY,
        'token': TOKEN,
        'fields': 'name,desc,url,idList,idMembers'
    }
    response = requests.get(url, params=params)
    cards = response.json()

    # Get all member details once
    members_url = f"https://api.trello.com/1/boards/{board_id}/members"
    members_resp = requests.get(members_url, params={'key': API_KEY, 'token': TOKEN})
    member_map = {
        m['id']: {
            'fullName': m.get('fullName', ''),
            'firstName': m.get('fullName', '').split()[0] if m.get('fullName') else ''
        }
        for m in members_resp.json()
    }


    # Attach member info to each card
    for card in cards:
        card_members = []
        for member_id in card.get('idMembers', []):
            if member_id in member_map:
                card_members.append(member_map[member_id])
        card['members'] = card_members

    return cards


def get_board_lists(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {
        'key': API_KEY,
        'token': TOKEN,
    }
    response = requests.get(url, params=params)
    return response.json()
