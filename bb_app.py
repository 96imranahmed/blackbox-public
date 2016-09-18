from flask import Flask
from flask import request
import json
import flask
import sys


sys.path.append('/pymessenger/')
from pymessenger.bot import Bot
from db import queryDB
from apiclient import discovery
from oauth2client import client

from dating import understand_sentence as u_s
from state_machine import state_machine
from StateInfo import StateInfo

URL = 'https://blackboxai.me/'
COMMANDS = ["clear", "howdy", "waddup"]
VALIDATION_TOKEN = 'super_amazing_secret_token'
ACCESS_TOKEN = ‘even_longer_super_amazing_secret_token’
bot = Bot(ACCESS_TOKEN)
app = Flask(__name__)
app.secret_key = 'super_duper_secret_token'
app.config.update(dict(
    PREFERRED_URL_SCHEME='https'
))


state_info = StateInfo(bot)

@app.route('/', methods = ['POST', 'GET'])
def welcome():
    if request.method == 'GET':
        try:
            if request.args['hub.verify_token'] == VALIDATION_TOKEN:
                return request.args['hub.challenge'], 200
            else:
                return 'Error - invalid token supplied', 403
        except:
            return 'Hey there! How about you try message me from Facebook Messenger?', 200

    elif request.method == 'POST':
        data = request.json
        messages = data['entry'][0]['messaging']
        print(messages)
        for msg in messages:
            if (msg.get('message') and msg['message'].get('text') and not 'is_echo' in msg['message'] and not 'delivery' in msg):
                if not 'quick_reply' in msg['message'] and not 'attachments' in msg['message']:
                    message = msg['message']['text']
                    user_id = msg['sender']['id']
                    state_info.set_user(user_id)
                    print(message)
                    bot.send_mark_seen(user_id)
                    bot.send_typing(user_id, True)
                    if (message[0] == '/'):
                        message = message[1:].lower()
                        if (message in COMMANDS):
                            if message == "clear":
                                queryDB("del_user", user_id)
                                bot.send_text_message(user_id, "Your ID " + user_id + " has been removed from the database.")
                            elif message == "howdy":
                                bot.send_text_message(user_id, "Howdy fella")
                            elif message == "waddup":
                                bot.send_text_message(user_id, "it's ya boi")
                        else:
                            bot.send_text_message(user_id, "Command not recognised :( ")
                    else:
                        # login on our server and on google
                        #jacqueslog(user_id, bot)

                        # call NLP and state machine
                        try:
                            flow(message)
                        except Exception as e:
                            print(e)
                            print('DEBUG')

                        pass
                    bot.send_typing(user_id, False)
                else:
                    #Handle custom reply
                    if 'quick_reply' in msg['message']:
                        payload = msg['message']['quick_reply']['payload']
                        print(payload)
                        #Quick replies
                    elif 'attachments' in msg['message']:
                        if  msg['message']['attachments']['type'] == 'location':
                            payload = msg['message']['attachments']['payload']['coordinates']
                            latitude = payload['lat']
                            longitude = payload['long']
                            #Location
            else:
                pass
    return 'Success!', 200


def jacqueslog(user_id, bot):
    if (queryDB('new_user_check', user_id) == False):
        bot.send_text_message(user_id, "Hey there " + user_id + " It's looking like this is your first message!")
        queryDB('add_user', user_id)
    else:
        bot.send_text_message(user_id, "Welcome back " + user_id + "!")

    if (queryDB('google_cal_check', user_id) == False):
        # edit the url below to be blackbox.../login flow
        # define the function in another flask file
        # this can redirect to google cloud login api
        # oauth callback on google logs you in, allows the blackbox app to use the calendar
        oauth_request_button = [
            {
                "type": "web_url",
                "url": URL + "login?user_id=" + str(user_id),
                "title": "Connect?",
                "webview_height_ratio": "compact"
            }
        ]
        bot.send_button_message(user_id, "How about you connect your Google Calendar? :)",
                                oauth_request_button)


def flow(message):
    state_info.processed_data, flag_empty = u_s.get_NLP(message)
    print(state_info.processed_data)
    intent = state_info.processed_data['intent']
    print(intent)
    state_info.bot.send_text_message(state_info.user.user_id, str(intent))
    state_info.flag_empty = flag_empty
    state_machine.state_machine(state_info)


@app.route('/done', methods=['GET'])
def calendar_connect_done():
    return 'All done! You have succesfully connected your calendar!', 200


@app.route('/login')
def login():
    user_id = request.args.get('user_id')
    flask.session['user_id'] = user_id
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        credentials = None
        try:
            credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
        except:
            return flask.redirect(flask.url_for('oauth2callback'))
        if credentials.access_token_expired:
            return flask.redirect(flask.url_for('oauth2callback'))
        else:
            cur_cred = json.loads(flask.session['credentials'])
            print(cur_cred)
            refresh_token = cur_cred['refresh_token']
            cur_token = cur_cred['access_token']
            if refresh_token == None:
                print(str(cur_token))
            else:
                queryDB('google_token_enter', [flask.session['user_id'], str(cur_token) + '||' + str(refresh_token)])
                bot.send_text_message(flask.session['user_id'],
                                      "Google calendar successfully setup - we're good to go woot! :D ")
    return flask.redirect(flask.url_for('calendar_connect_done'))


@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri=URL + 'oauth2callback')
    flow.params['approval_prompt'] = 'force'
    flow.params['access_type'] = 'offline'
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        cur_cred = json.loads(flask.session['credentials'])
        refresh_token = cur_cred['refresh_token']
        cur_token = cur_cred['access_token']
    if refresh_token == None:
        flask.session.pop('credentials', None)
        bot.send_text_message(flask.session['user_id'], "Suis désolé - do you mind logging in again?")
        return flask.redirect(flask.url_for('login?user_id=' + flask.session['user_id']))
    else:
        bot.send_text_message(flask.session['user_id'],
                              "Google calendar successfully setup - we're good to go woot! :D ")
        queryDB('google_token_enter', [flask.session['user_id'], str(cur_token) + '||' + str(refresh_token)])
        return flask.redirect(flask.url_for('calendar_connect_done'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
