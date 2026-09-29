class NoActiveRideError(Exception):
    pass


class RideAlreadyActiveError(Exception):
    pass


class AlreadyInStateError(Exception):
    def __init__(self, state):
        self.state = state
        super().__init__(f"Already in state: {state}")
