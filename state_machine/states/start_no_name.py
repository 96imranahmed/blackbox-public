from .default import pro_default

def pro_start_no_name(state_info):
    return pro_default(state_info)

def con_start_no_name(state_info):
    if not state_info.target.has_name():
       state_info.bot.send_text_message(state_info.user.get_user(), 'Who\'s your date? ;)')
       return None
    else:
       return 'start_with_name'
