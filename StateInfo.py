from dating.data_structures import User, Target, Date

class StateInfo:
    def __init__(self, bot):
        self.cur_state = 'start_no_name'
        self.old_state = 'start_no_name'
        self.user = User()
        self.target = Target()
        self.date = Date()
        self.bot = bot
        # dict up of up to three elems - intents: , values: , extras:
        # these contain all the information we can use to sort stuff in the
        # state machine
        self.processed_data = None
        self.recommended_event = None
        self.started = False
        self.flag_empty = False

    def set_user(self, user_id):
        if self.user.get_user() == '0':
            self.user.set_user(user_id)
