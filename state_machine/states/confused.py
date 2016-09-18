from .default import pro_default

def pro_confused(state_info):
    #Not Implemented
    print('What am I doing here???')
    state_info.bot.send_text_message(state_info.user.get_user(),'I am confused. Let us try again')
    return 'start_no_name'

def con_confused(state_info):
    if not state_info.flag_empty:
        state_info.bot.send_text_message(state_info.user.get_user(), "Hey, didn't catch that - try to rephrase that")
    if state_info.cur_state == 'confused':
        return None
    else:
        return state_info.cur_state
