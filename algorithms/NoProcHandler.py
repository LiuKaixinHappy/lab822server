from algorithms.handler import Handler


class NoProcHandler(Handler):
    def handle(self, code, params, image):
        return None
