from state_machine.states import *

proc_states = {'start_with_name': pro_start_with_name, 'start_no_name': pro_start_no_name,
               'calendar': pro_calendar, 'confused': pro_confused, 'give_recommendation': pro_give_recommendation,
               'pickups': pro_pickup, 'set_date': pro_set_date}

states = {'start_with_name': con_start_with_name, 'start_no_name': con_start_no_name,
          'calendar': con_calendar, 'confused': con_confused, 'give_recommendation': con_give_recommendation,
          'pickups': con_pickup, 'set_date': con_set_date}


def update_state(next_state, state_info):
    state_info.old_state = state_info.cur_state
    state_info.cur_state = next_state


# IMPORTANT - THIS MUST MUST MUST HAVE THE STATEINFO OBJECT READY TO USE
# ELSE EVERYTHING WILL BREAK FOR SURE.
def state_machine(state_info):
    print(state_info.processed_data)
    print(state_info.cur_state, 'cur_state')
    if state_info.started == False:
        state_info.started = True

    next_state = proc_states[state_info.cur_state](state_info)
    update_state(next_state, state_info)
    print(next_state, state_info.cur_state, 'GO TO THIS STATE 1', state_info.old_state)
    while True:
        next_func = states[state_info.cur_state](state_info)
        if next_func is not None:
            update_state(next_func, state_info)

            next_func = states[next_func](state_info)
            print(state_info.cur_state, 'GO TO THIS STATE')
        else:  # this is the case when we must break out of here -we are waiting for input
            break
    # all done with the state machine
    return
