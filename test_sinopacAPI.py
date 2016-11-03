# coding=UTF-8
# __author__ == ypochien@gmail.com
# __date__ ==
from random import choice
from unittest import TestCase
from unittest import skip
from nose_parameterized import parameterized

from SinopacAPI import SinopacAPI


class TestSinopacAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestSinopacAPI, cls).setUpClass()
        cls.api = SinopacAPI()
        cls.api.login()

    @classmethod
    def tearDownClass(cls):
        cls.api.logout()
        super(TestSinopacAPI, cls).tearDownClass()

    def setUp(self):
        self.api = TestSinopacAPI.api

    @skip('no personal info')
    def test_verify_config_json_file(self):
        actual = self.api.show_user()
        expected = {'UserId': '', 'Password': '', 'eKey': 'C:/ekey/551/',
                    'eKeyPassword': ''}
        self.assertDictEqual(expected, actual)

    @parameterized.expand([('01S', SinopacAPI.ORDER_TYPE_SPOT, "2890", -1)
                              , ('02S', SinopacAPI.ORDER_TYPE_SPOT, "2890", -1)
                              , ('02S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", -2)
                              , ('01S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", -2)
                              , ('01S', SinopacAPI.ORDER_TYPE_LOAN, "2890", -3)
                              , ('02S', SinopacAPI.ORDER_TYPE_LOAN, "2890", -3)
                              , ('01S', SinopacAPI.ORDER_TYPE_SPOT, "2890", 4, 8.10)
                              , ('01S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", 5, 8.11)
                              , ('01S', SinopacAPI.ORDER_TYPE_LOAN, "2890", 6, 8.12)
                              , ('02S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", -7, 8.13)])
    def test_make_order_TYPE_STOCK_QTY_and_at_market(self, expected, order_type, stock_id, qty, price=None):
        # '''測試下單-現股、融資、融券 + 買進、賣出 + 限價、市價'''
        order_object = self.api.MakeStockOrder(order_type, stock_id, qty, price)
        actual = self.api.placeOrder(order_object)
        self.assertIn(expected, actual)

    @skip("no impl")
    def test_cancel_all_orders(self):
        actual = self.api.calcel_all()
        expected = '01S'
        self.assertIn(expected, actual)

    @skip("login skipping")
    def test_normal_login(self):
        # Arrange
        expected = '初始化成功'

        # Act
        actual = self.api.login()

        # Assert
        self.assertEqual(expected, actual, 0)

    def test_account_list(self):
        actual = self.api
        print 'Account counts:', len(actual.accounts)
        for item in actual.accounts.items():
            print item
        self.assertEqual(1,1)

    @skip("login skipping")
    def test_no_auth_login(self):
        # Arrange
        expected = 'Error'

        # Act
        actual = self.api.login()

        # Assert
        self.assertIn(expected, actual)
