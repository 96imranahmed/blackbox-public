import datetime

def pro_set_date(state_info):
    return 'set_date'

def con_set_date(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(), "I'm adding the event to your Google calendar! Have fun ;)")
    return 'state_no_name'


def event(event):
    ret = (None,None)
    days = ('monday', 'tuesday', 'wednesday', 'thursday','friday', 'saturday', 'sunday')
    for i in event:
        if i.lower() in days:
            ret[1] = days
