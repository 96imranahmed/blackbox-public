import random as r
from .default import pro_default


PICKUPS = ["Damn girl, is your name Wifi? Because I’m feeling a connection",
                "Are you made of beryllium, gold, and titanium? You must be because you are BeAuTi-ful.",
                "If you were a triangle youd be acute one.",
                "Are you a singularity? Not only are you attractive, but the closer I get to you, the faster time seems to slip by.",
                "Do you have 11 protons? Cause your sodium fine.",
                "You're sweeter than 3.14",
                "Are you a carbon sample? Because I want to date you.",
                "I'd like to calculate the slope of those curves.",
                "According to the second law of thermodynamics, you're supposed to share your hotness with me.",
                "Are you sitting on the F5 key? Because your backside is refreshing."]

def get_pickups():
    return PICKUPS[r.randint(0, len(PICKUPS) - 1)]

def pro_pickup(state_info):

    intent = state_info.processed_data['intent']

    if intent == 'Decline':
        return 'pickups'
    elif intent == 'more':
        return 'pickups'

    if intent == 'Accept':
        return 'start_no_name'

    else:
        return pro_default(state_info)

def con_pickup(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(), get_pickups())
    state_info.bot.send_text_message(state_info.user.get_user(), 'Was this ok?')

    return None
