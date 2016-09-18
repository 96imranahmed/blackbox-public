
from .default import pro_default

def pro_start_with_name(state_info):
    return pro_default(state_info)

def con_start_with_name(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(), "What can I help you with?")
    return None
