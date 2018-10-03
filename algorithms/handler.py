class Handler(object):

    def __init__(self, _to_next=None):
        self._to_next = _to_next

    def to_next(self, _to_next):
        self._to_next = _to_next

    def handle(self, code, params, image):
        pass
