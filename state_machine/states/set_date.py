import datetime
from apiclient import discovery
import httplib2
import sys

sys.path.append('../../db')
from db import queryDB

def pro_set_date(state_info):
    return 'set_date'

def con_set_date(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(), "I'm adding the event to your Google calendar! Have fun ;)")
    return 'start_no_name'
    # event = state_info.recommended_event
    # print(event)
    # # event[0] - name
    # # event[1] - URL
    # # event[2] - venue
    # # event[3] - time and date
    # ev = {
    #     'summary': event[0],
    #     'location': event[2],
    #     'description': event[1],
    #     'start':
    #         {
    #         'dateTime': (event[3]),
    #         'timeZone': 'America/New_York',
    #         },
    #     'end':
    #         {
    #         #'dateTime': '2015-05-28T17:00:00-07:00',
    #         #'timeZone': 'America/New_York',
    #         },
    #     'reminders':
    #         {
    #         'useDefault': False,
    #         'overrides':
    #             [
    #               {'method': 'email', 'minutes': 24 * 60},
    #               {'method': 'popup', 'minutes': 10},
    #             ],
    #         },
    # }
    credentials = queryDB('google_cal_check', state_info.user.get_user())
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    ev = service.events().insert(calendarId='primary', body=ev).execute()
    print ('Event created: %s' % (ev.get('htmlLink')))


def event(event):
    ret = (None,None)
    days = ('monday', 'tuesday', 'wednesday', 'thursday','friday', 'saturday', 'sunday')
    for i in event:
        if i.lower() in days:
            ret[1] = days
