from flask import Flask, render_template, render_template, redirect, url_for
from trello_utils import get_board_lists, get_board_cards
import time

app = Flask(__name__)

BOARDS = {
    'Sales': '6824b1725e722de9126ba280',
    'Success': '683752d8d6dee9e968539ca7',
    'Helpdesk': '6879103f95684607afc97c06',
}

BOARD_NAMES = list(BOARDS.keys())

@app.route("/")
def redirect_to_first():
    return redirect(url_for('dashboard', board_index=0))


@app.route("/<int:board_index>")
def dashboard(board_index):
    board_name = BOARD_NAMES[board_index % len(BOARD_NAMES)]
    board_id = BOARDS[board_name]

    lists = get_board_lists(board_id)
    cards = get_board_cards(board_id)

    # Define excluded list names per board
    EXCLUDED_LISTS = {
        'Sales': ['Ghost Archive', 'Cold', 'Parking Lot'],
        'Success': ['7. Parking Lot'],
    }

    # Build a list name → ID map, skipping excluded ones
    excluded_names = EXCLUDED_LISTS.get(board_name, [])
    structured = {}

    for lst in lists:
        if lst['name'] in excluded_names:
            continue  # Skip excluded lists
        structured[lst['name']] = []

    # Add cards only to included lists
    for card in cards:
        list_id = card['idList']
        list_obj = next((l for l in lists if l['id'] == list_id), None)

        if list_obj and list_obj['name'] not in excluded_names:
            structured[list_obj['name']].append(card)


    next_index = (board_index + 1) % len(BOARD_NAMES)

    return render_template("dashboard.html", board_name=board_name, board=structured, next_index=next_index)

if __name__ == "__main__":
    app.run(debug=True)
