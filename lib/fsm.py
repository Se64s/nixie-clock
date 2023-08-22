#
# fsm.py
# Brief: Module to handle simple finite state machines
#

class Fsm:
    def __init__(self, init_state=0, state_handlers=[], event_handler=None):
        self.__state = init_state
        self.__state_handlers = state_handlers
        self.__event_handler = event_handler
    
    def execute_state(self):
        if len(self.__state_handlers) >= self.__state:
            return self.__state_handlers[self.__state]()
        else:
            return None

    def get_state(self):
        return self.__state
    
    def rise_event(self, event):
        self.__state = self.__event_handler(self.__state, event)
        return self.__state

# EOF
