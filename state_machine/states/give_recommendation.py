
from .default import pro_default
import os, sys
import requests
from xml.etree import ElementTree
import json

def pro_give_recommendation(state_info):

    intent = state_info.processed_data['intent']

    if intent == 'Accept' or intent == 'Like':
        if 'values' in state_info.processed_data:
            event = state_info.processed_data['values'][0]
        else:
            event = None
        if event is not None:
            state_info.user.likes.append(event)
        if intent == 'Accept':
            return 'set_date'
        else:
            return 'start_no_name'

    elif intent == 'Decline' or intent == 'Dislike':
        print("just after decline, " + state_info.processed_data)

        if 'values' in state_info.processed_data:
            event = state_info.processed_data['values'][0]
        else:
            event = None
        if event is not None:
            state_info.user.dislikes.append(event)
        if intent == 'Decline':
            state_info.bot.send_text_message(state_info.user.get_user(),
                                             ":( Ask me for more later!")
            return 'start_no_name'
        else:
            return 'give_recommendation'

    return pro_default(state_info)


def con_give_recommendation(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(), "I've got some recommendations for you - if you like them let me know!")
    event = get_top_event(get_event_data())
    oauth_request_button = [
            {
                "type": "web_url",
                "url": event[1],
                "title": event[0],
                "webview_height_ratio": "tall"
            }
        ]
    state_info.bot.send_button_message(state_info.user.get_user(), "How about this event?",
                                oauth_request_button)
    replies = [
        {
            "content_type": "text",
            "title": "Decline?",
            "payload": 'EVENT||' + event[0] + '||' + str(0)
        },
        {
            "content_type": "text",
            "title": "Accept?",
            "payload": 'EVENT||' + event[0] + '||' + str(1)
        }
    ]
    state_info.bot.quick_reply(state_info.user.get_user(), "Any good?", replies)

    state_info.recommended_event = event

    return None

def get_top_event(cur_events):
    return cur_events[0]

ZOMATO = '812c303f8675a8c4eac2a867e96bb0c4'

def get_event_data(loc_string = 'Boston, Massachusetts', loc_radius='25', date_info = 'Today'): #YYYYMMDD00-YYYYMMDD00 or Today/Future/Past
    #Not the most useful of feeds (and paid) but it might be worth having a look at later
    URL = 'http://api.eventful.com/rest/events/search?&app_key=SBMzG2R6777KG9CL&location='+loc_string+'&within='+ loc_radius + '&sort_order=popularity&date=' + date_info + '&include=subcategories,categories,popularity&category=attractions,festivals,sports,singles_social&ex_category=clubs_associations,family_fun_kids'
    txt = requests.get(URL).text
    cur_events = eventful_analyse_xml(txt)
    return cur_events

def eventful_analyse_xml(txt): #For parsing Eventful response
    events_out = []
    root = ElementTree.fromstring(txt)
    if int(root.find('total_items').text) > 0:
        events = root.find('events')
        for event in events:
            if int(event.find('popularity').text) > 50:
                #Further filter events
                category_list = []
                for category in (event.find('categories')):
                    category_list.append(category.find('id').text)
                events_out.append([event.find('title').text, event.find('url').text, event.find('venue_name').text, event.find('start_time').text, category_list])
    return events_out

def get_food_nearby(loc_string = 'Boston, Massachusetts'):
    URL = 'https://developers.zomato.com/api/v2.1/locations?query=' + loc_string
    headers = {"User-agent": "curl/7.43.0", 'Accept': 'application/json', 'user-key': ZOMATO}
    r = requests.get(URL, headers=headers)
    root = r.json()
    entity_id = root['location_suggestions'][0]['entity_id']
    entity_type = root['location_suggestions'][0]['entity_type']
    URL = 'https://developers.zomato.com/api/v2.1/location_details?entity_id='+str(entity_id)+'&entity_type=' + str(entity_type)
    r = requests.get(URL, headers=headers)
    root = r.json()
    root = root['best_rated_restaurant']
    ret_rest = []
    for val in root:
        cur_rest = val['restaurant']
        cur_price = cur_rest['average_cost_for_two']
        cuisine = cur_rest['cuisines']
        url = cur_rest['url']
        name = cur_rest['name']
        ret_rest.append([name, url, cuisine, cur_price])
    return ret_rest
