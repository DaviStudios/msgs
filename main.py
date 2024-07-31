from flask import Flask, request, json

app = Flask(__name__)

user_messages = {}

connected_users = {}

@app.route('/')
def getdata():
    return f'Users connected: {str(len(connected_users))}', 200

@app.route('/send')
def handle_message():
    user_id = request.args.get('from')
    user_id2 = request.args.get('to')
    passw = request.args.get('pass')
    msg = request.args.get('msg')

    if user_id and msg and passw and user_id2:

        if user_id in connected_users:
            if passw != connected_users[user_id]:
                return 'Invalid password!', 400
        else:
            return 'Invalid from user!', 400
        
        if user_id2 in connected_users:
            user_messages[user_id2].append(msg)
        else:
            return 'Invalid to user!'

        print(f"{user_id} sent {msg} to {user_id2}")

        return f"Message sent to {user_id2}: {msg}", 200
    else:
        return "Please provide from, to, pass and msg parameters.", 400

@app.route('/connect')
def connect():
    user_id = request.args.get('user')
    passw = request.args.get('pass')

    if user_id and passw:
        if user_id in connected_users:
            return 'This user already exists!'
        connected_users[user_id] = passw
        user_messages[user_id] = []

        # Print the connection to the console
        print(f"User {user_id} connected")

        # Return the user ID
        response = {
            "user_id": user_id,
            "messages": user_messages.get(user_id, [])
        }
        return app.response_class(
            response=json.dumps(response),
            mimetype='application/json'
        )
    else:
        return "Please provide both user and pass parameters.", 400
    
@app.route('/delete')
def delete():
    user_id = request.args.get('user')
    passw = request.args.get('pass')

    if user_id and passw:
        if user_id in connected_users:
            if passw == connected_users[user_id]:
                del connected_users[user_id]
                del user_messages[user_id]

                return f'Succesfully deleted {user_id}!', 200
            else:
                return 'Invalid password!', 400
        else:
            return 'Invalid user!', 400
    return "Please provide both user and pass parameters.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4585)
