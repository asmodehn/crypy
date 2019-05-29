import unittest

from pydantic import BaseModel
from ..popint import POP



from datetime import datetime
from typing import List




class TestModel(unittest.TestCase):

    class User(BaseModel):
        id: int
        name = 'John Doe'
        signup_ts: datetime = None
        friends: List[int] = []

    def test_class(self):

        POPUser = POP(TestModel.User)

        # pydantic works as documented
        external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
        user = POPUser(**external_data)

        # on errors, prompts:
        user = POPUser(signup_ts='broken', friends=[1, 2, 'not number'])


if __name__ == '__main__':
    unittest.main()