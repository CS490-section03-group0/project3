import json
import unittest
import unittest.mock as mock
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from server.utils import get_user_balance, get_user_by_id
from server.utils.database_test import DatabaseTest
from server.models import User, Transaction

KEY_SUCCESS = "success"
KEY_MESSAGE = "message"
KEY_AMOUNT = "amount"
KEY_TICKET_AMOUNT = 600

class BlackjackCheckFundsTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        trans1 = Transaction (
            user_id=self.user1_id,
            ticket_amount=KEY_TICKET_AMOUNT,
            activity="Transaction Test",
        )
        with self.app.app_context():
            db.session.add(trans1)
            db.session.commit()

        self.blackjack_checkfunds_success = {
            KEY_SUCCESS: True,
        }
        self.blackjack_checkfunds_bad = {
            KEY_SUCCESS: False,
            KEY_MESSAGE: "You are wagering more tickets than you currently have"
        }
        self.blackjack_checkfunds_error = {"error": "Malformed request"}

    def test_blackjack_check_success(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess['user_id'] = self.user1_id
            res = self.client.post('/api/blackjack/checkfunds', data = json.dumps({
                KEY_AMOUNT: 500
            }))
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(self.blackjack_checkfunds_success, result)
    
    def test_blackjack_check_bad(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess['user_id'] = self.user1_id
            res = self.client.post('/api/blackjack/checkfunds', data = json.dumps({
                KEY_AMOUNT: 1000
            }))
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(self.blackjack_checkfunds_bad, result)
    
    def test_blackjack_check_error(self):
        res = self.client.post('/api/blackjack/checkfunds', data = "bad data")
        result = json.loads(res.data.decode("utf-8"))
        self.assertDictEqual(self.blackjack_checkfunds_error, result)

if __name__ == "__main__":
    unittest.main()