from .default import pro_default

def pro_calendar(state_info):
    return pro_default(state_info)

def con_calendar(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(), "When is your date?")
    return None
