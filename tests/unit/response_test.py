from magic_admin.response import MagicResponse


class TestMagicResponse:

    content = 'troll_goat'
    status_code = 200
    resp_data = {'data': 'another_troll_goat'}

    def test_response(self):
        resp = MagicResponse(
            content=self.content,
            status_code=self.status_code,
            resp_data=self.resp_data,
        )

        assert resp.content == self.content
        assert resp.status_code == self.status_code
        assert resp.data == self.resp_data['data']
