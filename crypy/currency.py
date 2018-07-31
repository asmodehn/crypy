


class Currency:
    """ Specific object to manipulate currency properly, as a measure unit"""

    def __init__(self, identifier: str) -> Currency:
        self.identifer = identifier


    def __repr__(self):
        return self.identifer


    def __str__(self):
        return self.identifer





