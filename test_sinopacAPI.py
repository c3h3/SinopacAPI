# coding=UTF-8
# __author__ == ypochien@gmail.com
# __date__ ==
from random import choice
from unittest import TestCase
from unittest import skip
from nose_parameterized import parameterized

from SinopacAPI import SinopacAPI


class TestSinopacAPI(TestCase):
    '''
        # Arrange
        expected = '初始化成功'
        # Act
        actual = self.api.login()
        # Assert
        assert
    '''

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

    @parameterized.expand([('01S', SinopacAPI.ORDER_TYPE_SPOT, "2890", 1)
                              , ('02S', SinopacAPI.ORDER_TYPE_SPOT, "2890", -1)
                              , ('01S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", 2)
                              , ('02S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", -2)
                              , ('01S', SinopacAPI.ORDER_TYPE_LOAN, "2890", 3)
                              , ('02S', SinopacAPI.ORDER_TYPE_LOAN, "2890", -3)
                              , ('01S', SinopacAPI.ORDER_TYPE_SPOT, "2890", 4, 8.10)
                              , ('01S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", 5, 8.11)
                              , ('01S', SinopacAPI.ORDER_TYPE_LOAN, "2890", 6, 8.12)
                              , ('02S', SinopacAPI.ORDER_TYPE_MARGIN, "2890", -7, 8.13)])
    def test_make_order_TYPE_STOCK_QTY_and_at_market(self, expected, order_type, stock_id, qty, price=None):
        '''Test PlacingOrder(Type,Stock,Qty,Price)'''
        order_object = self.api.MakeStockOrder(order_type, stock_id, qty, price)
        actual = self.api.placeOrder(order_object)
        self.assertIn(expected, actual)

    def test_account_list(self):
        '''設定並且登入正常，會有一組帳號以上，否則請檢查t4的設定'''
        actual = self.api
        account_size = len(actual.accounts)
        self.assertGreater(account_size, 0, 'Account not found. Plz check t4.ini and t4.log')
