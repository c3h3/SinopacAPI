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

    @parameterized.expand([(['2890', '01'], SinopacAPI.ORDER_TYPE_SPOT, "2890", 1),
                           (['2890', '02'], SinopacAPI.ORDER_TYPE_SPOT, "2890", -1),
                           (['2890', '01'], SinopacAPI.ORDER_TYPE_MARGIN, "2890", 2),
                           (['2890', '02'], SinopacAPI.ORDER_TYPE_MARGIN, "2890", -2),
                           (['2890', '01'], SinopacAPI.ORDER_TYPE_LOAN, "2890", 3),
                           (['2890', '02'], SinopacAPI.ORDER_TYPE_LOAN, "2890", -3),
                           (['2890', '01'], SinopacAPI.ORDER_TYPE_SPOT, "2890", 4, 8.10),
                           (['2890', '01'], SinopacAPI.ORDER_TYPE_MARGIN, "2890", 5, 8.11),
                           (['2890', '01'], SinopacAPI.ORDER_TYPE_LOAN, "2890", 6, 8.12),
                           (['2890', '02'], SinopacAPI.ORDER_TYPE_MARGIN, "2890", -7, 8.13)])
    def test_make_order_TYPE_STOCK_QTY_and_at_market(self, expected, order_type, stock_id, qty, price=None):
        '''Test PlacingOrder Then CancelOrder (Type,Stock,Qty,Price)'''
        order_object = self.api.MakeStockOrder(order_type, stock_id, qty, price)
        actual = self.api.PlacingOrder(order_object)
        self.assertIn(expected[0], actual.stock_id, '股票代號錯誤')
        self.assertEqual(expected[1], actual.trade_type, '買賣別錯誤')
        print '\n=====Order'
        print ','.join(actual[:-1]) + ',' + str(actual.Msg.strip().decode('cp950').encode('utf8'))
        actual = self.api.CancelOrder(actual)
        print ','.join(actual[:-1]) + ',' + str(actual.Msg.strip().decode('cp950').encode('utf8'))
        print 'Cancel====='

    def test_order_return_format(self):
        record = '01S9A95   98093152890  000000001360514201611102016111123171300000152000000B00S200' \
                 '委託處理中, 請於交易時間確認委託狀態!                       '.decode('utf8').encode('cp950')
        actual = len(record)
        expected = 141  # Stock order回報格式長度
        self.assertEqual(expected, actual)
        actual = self.api._make_stock_order_record(record)
        expected = 'S9A95   9809315'
        self.assertEqual(expected, actual.Account)
        expected = 60  # msg 長度
        self.assertEqual(expected, len(actual.Msg))

    def test_account_list(self):
        '''設定並且登入正常，會有一組帳號以上，否則請檢查t4的設定'''
        actual = self.api
        account_size = len(actual.GetAccount())
        self.assertGreater(account_size, 0, 'Account not found. Plz check t4.ini and t4.log')
