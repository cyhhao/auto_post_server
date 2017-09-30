class PostHandler:
    def __init__(self):
        self.name = self.__class__.__name__

    def form(self):
        pass

    def payload(self, options):
        pass

    def response(self, payloads):
        pass

    def header(self):
        pass

    def render_form(self):
        data = self.form().render()
        data['key'] = self.name
        return data

    def render_payload(self):
        pass

    def render_response(self):
        pass
