#intents = ['DateInfo', 'Accept', 'Decline', 'Pickup', 'None', 'Name', 'Recommend', 'SetDate', 'Like', 'Dislike', 'More']

#states = {'start_with_name' : start_with_name, 'start_no_name': start_no_name,
#		  'calendar' : calendar, 'confused': confused, 'give_recommendation': give_recommendation,
#		  'pickups' : pickups, 'set_date'; set_date, 'set_name': set_name, 'sleep': sleep}

def con_not_implemented(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(),'Not Implemented, +%s' % __func__.__name__)
    return None


def pro_not_implemented(state_info):
    state_info.bot.send_text_message(state_info.user.get_user(),'Not Implemented, +%s' % __func__.__name__)
    return 'start_no_name'


def pro_default(state_info):
    print(state_info.processed_data)

    intent = state_info.processed_data['intent']
    print('intent = ', intent)

    if intent == 'DateInfo':
        '''NI'''
        return pro_not_implemented(state_info)

    elif intent == 'Accept':
        '''Done'''
        state_info.bot.send_text_message(state_info.user.get_user(),'This should not be called')
        return 'start_no_name'

    elif intent == 'Pickup':
        '''Done'''
        return 'pickups'

    elif intent == 'None':
        '''Done'''
        print('None intent')
        return 'confused'

    elif intent == 'Recommend':
        print('Hello')
        return 'give_recommendation'

    elif intent == 'SetDate':
        return pro_not_implemented(state_info)

    elif intent == 'Like':
        state_info.bot.send_text_message(state_info.user.get_user(), "Glad you liked it!")
        #not done
        return state_info.cur_state

    elif intent == 'Dislike':
        state_info.bot.send_text_message(state_info.user.get_user(), "Sorry you didn't like that!")

        return state_info.cur_state

    elif intent == 'More':
        return state_info.cur_state

    elif intent == 'Decline':
        return 'start_no_name'

    elif intent == 'Name':
        print(state_info.processed_data['values'])
        state_info.target.name = str(state_info.processed_data['values']).capitalize()
        state_info.bot.send_text_message(state_info.user.get_user(), str(state_info.target.name) + ", huh? It's a beautiful name ;)")
        return 'start_with_name'

    else:
        print('!!!!Not Implemented,!!!!')
        return 'start_no_name'
        raise NotImplementedError
