class NoActiveRideError(Exception):
    pass


class RideAlreadyActiveError(Exception):
    pass


class AlreadyInStateError(Exception):
    def __init__(self, state):
        self.state = state
        super().__init__(f"Already in state: {state}")


class AlreadyRegisteredError(Exception):
    pass


class BlankCredentialsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass
