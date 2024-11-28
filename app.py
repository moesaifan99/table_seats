from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Initialize the dictionaries
friends_moe = []
friends_renad = []
no_rsvp_guests = set()  # Set to track guests who have declined

moe = {
    "Akram Yasien": 5,
    "Ali and Doaa": 2,
    "Asma Habahbeh":0,
    "Elias": 1,
    "Eyad and Sara": 2,
    "Hussein Odeh and Family": 3,
    "Ibrahim Hamza": 1,
    "Ibrahim Odeh and Family": 2,
    "Ibrahim Suaifan and Family": 4,
    "Jihad Jabir and Family": 4,
    "Malek": 1,
    "Mark": 1,
    "Mohamed Ahmed": 1,
    "Naser Abu El Hawa": 2,
    "Walid Jaludi": 2,
    "Ahmed Suqi": 0,
    "Heithem Odeh": 2,
    "Saher Odeh": 2,
    "Wesam Daraghmeh": 2,
    "Abu Hashim": 4,
    "Ahmed Awadallah": 0,
    "Khalil Awadallah": 0,
    "Omar Warraky": 3,
    "Patryk Kaziow": 1,
    "Saleh Aby Nasir": 3,
    "Samir Issa and Family": 3,
    "Khaled Saifan Entire Family": 8,
    "Walid Suaifan and Children": 1,
    "Yahya Saifan": 5,
    "Yousef Elmorsi": 1,
}

renad = {
    "Adeeb and Saeda": 0,
    "Ali and Ebtehal": 0,
    "Amal and Alaa Hirzallah": 1,
    "Dania Alaraj":1,
    "Dia and Lana": 0,
    "Emad Saleh and Family": 6,
    "Hussein Saleh and Family": 6,
    "Ismail Faraj and Family": 3,
    "Jamal Saleh and Family": 4,
    "James and Dalal": 0,
    "Maher Deeb and Family": 4,
    "Mahmood Faraj": 0,
    "Mohammad Saleh and entire family": 7,
    "Mr. and Mrs. Adnan Saleh":0,
    "Mr. and Mrs. Nabil saleh": 2,
    "Mr. and Mrs. Riyad Saleh":2,
    "Mr. and Mrs. Samir Saleh":1,
    "Nabil Saleh and Family": 4,
    "Naser Saleh and Family": 0,
    "Odeh Saleh and Family": 4,
    "Omar and Gadeer": 2,
    "Roquieh Faraj": 1,
    "Said Alhayek and Family": 6,
    "Tamer and Yasmeen": 2,
    "Abdelrahim Family": 3,
    "Texas Hirzolla": 0,
    "Eman Assaf": 1,
    "Noor Ahmed": 1,
    "Ghunwah Melhem": 1,
    "Minna Mohammad": 1
}

# Store original counts for resetting later
original_moe = moe.copy()
original_renad = renad.copy()

# To track updated guests
updated_guests_moe = set()
updated_guests_renad = set()

@app.route('/', methods=['GET', 'POST'])
def index():
    global moe, renad, updated_guests_moe, updated_guests_renad, no_rsvp_guests
    global friends_moe, friends_renad

    if request.method == 'POST':
        # Update guest count
        name = request.form.get('name')
        count = request.form.get('count')
        action = request.form.get('action')

        # Handle adding friend
        if action == 'add_friend':
            if name not in friends_moe and name in moe:
                friends_moe.append(name)
            elif name not in friends_renad and name in renad:
                friends_renad.append(name)

        # Update guest count
        elif name and count.isdigit():
            if name in moe:
                moe[name] = int(count)
                updated_guests_moe.add(name)
            elif name in renad:
                renad[name] = int(count)
                updated_guests_renad.add(name)

        # Handle "No RSVP" action
        if action == 'No RSVP':
            if name in moe:
                total_guests_moe = sum(moe.values())
                moe[name] = 0  # Set the count to 0 since they declined
                no_rsvp_guests.add(name)  # Track guests who declined
            elif name in renad:
                total_guests_renad = sum(renad.values())
                renad[name] = 0  # Set the count to 0 since they declined
                no_rsvp_guests.add(name)  # Track guests who declined

        # Redirect to refresh the page
        return redirect(url_for('index'))

    # Get the filter query for Moe's guests
    filter_query_moe = request.args.get('filter_moe', '')
    filtered_moe = {name: count for name, count in moe.items() if filter_query_moe.lower() in name.lower()}

    # Get the filter query for Renad's guests
    filter_query_renad = request.args.get('filter_renad', '')
    filtered_renad = {name: count for name, count in renad.items() if filter_query_renad.lower() in name.lower()}

    # Calculate updated total guests
    updated_total_guests_moe = sum(value for name, value in moe.items() if name not in updated_guests_moe)
    updated_total_guests_renad = sum(value for name, value in renad.items() if name not in updated_guests_renad)

    return render_template('index.html', 
                           moe=filtered_moe, 
                           renad=filtered_renad, 
                           total_guests_moe=sum(filtered_moe.values()),
                           total_guests_renad=sum(filtered_renad.values()),
                           updated_guests_moe=updated_guests_moe,
                           updated_guests_renad=updated_guests_renad,
                           updated_total_guests_moe=updated_total_guests_moe,
                           updated_total_guests_renad=updated_total_guests_renad,
                           friends_moe=friends_moe, 
                           friends_renad=friends_renad,
                           no_rsvp_guests=no_rsvp_guests)  # Pass no_rsvp_guests to the template


@app.route('/clear_updates', methods=['POST'])
def clear_updates():
    global moe, renad, updated_guests_moe, updated_guests_renad, no_rsvp_guests
    # Reset to original counts
    moe = original_moe.copy()
    renad = original_renad.copy()
    
    # Clear updated guests and no RSVP guests
    updated_guests_moe.clear()
    updated_guests_renad.clear()
    no_rsvp_guests.clear()  # Reset the no RSVP guests

    return redirect(url_for('index'))

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

# Predefine tab passwords in the backend
TAB_PASSWORDS = {
    "Ammar Shots": "Ammar",
    "May Events": "May",
    "DJ Ibrahim": "DJ"
}

@app.route('/get_passwords', methods=['GET'])
def get_passwords():
    return jsonify(TAB_PASSWORDS)

@app.route('/load_moes_guests', methods=['GET'])
def load_moes_guests():
    try:
        # Path to the session_data.json file in the templates folder
        file_path = os.path.join('templates', 'session_data.json')

        # Open and load the session_data.json
        with open(file_path, 'r') as file:
            session_data = json.load(file)

        return jsonify(session_data)  # Return the JSON data to the client

    except FileNotFoundError:
        return jsonify({"error": "session_data.json not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding session_data.json"}), 400

if __name__ == '__main__':
    app.run(debug=True)
