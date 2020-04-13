class MagicResponse:

    def __init__(self, content, resp_data, status_code):
        self.content = content
        self.status_code = status_code
        self.data = resp_data['data']
