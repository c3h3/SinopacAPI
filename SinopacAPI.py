# coding=UTF-8
# __author__ == ypochien@gmail.com
import json
from collections import namedtuple

import struct

from pyT4 import *


def to_utf8(fn):
    def with_utf8(*args, **kwargs):
        msg = fn(*args, **kwargs)
        return msg.decode('cp950').encode('utf8')

    return with_utf8


class SinopacAPI(object):
    ORDER_TYPE_SPOT = '0'  # 現股
    ORDER_TYPE_MARGIN = '3'  # 融資
    ORDER_TYPE_LOAN = '4'  # 融券

    ORDER_BS_BUY = 'B'  # 買進
    ORDER_BS_SELL = 'S'  # 賣出
    ORDER_BS_FIRST = 'F'  # 先賣

    ORDER_SECTION_NORMAL = '0'  # 一般交易
    ORDER_SECTION_FIXED = 'P'  # 定盤交易
    ORDER_SECTION_PENNY = '2'  # 零股

    ORDER_FLAG_LIMIT_UP = '2'  # 漲停
    ORDER_FLAG_LIMIT_NORMAL = ' '  # 限價
    ORDER_FLAG_LIMIT_DOWN = '3'  # 跌停

    def __init__(self):
        self._accounts = {}
        self.__load_config()
        self.MakeStockOrder = namedtuple('MakeStockOrder', 'Order_Type,Stock_ID,Qty,Price')

        field = 'trade_type Account stock_id ord_price ord_qty ord_seq ord_date effective_date ord_time ord_no ord_soruce org_ord_seq ord_bs ord_type1 ord_type2 market_id price_type ord_status Msg'
        self.StockOrderRecord = namedtuple('StockOrderRecord', field)
        self.StockOrderRecordfmt = '2s15s6s6s3s6s8s8s6s5s3s6s1s1s1s1s1s2s60s'
        self.StockOrderRecordList = []

    def __load_config(self, config_json='./config.json'):
        with open(config_json) as fd_json:
            self.UserInfo = json.load(fd_json)

    @staticmethod
    def show_version():
        return show_version()

    @to_utf8
    def login(self):
        msg = init_t4(self.UserInfo['UserId'], self.UserInfo['Password'], '')
        do_register(1)
        self.__load_account()
        return msg

    def show_user(self):
        self.__load_config()
        return self.UserInfo

    @staticmethod
    def change_echo():
        change_echo()

    @staticmethod
    def logout():
        log_out()

    def MakeStockOrder(self, order_type, stock_id, qty, price):
        return self.MakeStockOrder._make(Order_Type=order_type, Stock_ID=stock_id, Qty=qty, Price=price)

    def PlacingOrder(self, order_obj):
        price = order_obj.Price
        order_type = order_obj.Order_Type
        stock_id = order_obj.Stock_ID
        qty = order_obj.Qty

        if price == None:
            _price = ' '
            _price_type = '2'
        else:
            _price = price
            _price_type = ' '
        _price = str(_price)
        _ord_type = '0' + order_type
        _bs = 'B' if qty > 0 else 'S'
        _qty = str(abs(qty))
        raw_record = stock_order(_bs, self._accounts['S']['branch'], self._accounts['S']['account'], stock_id, _ord_type,
                                 _price, _qty, _price_type)
        if 'Error' in raw_record:
            print raw_record.decode('cp950').encode('utf8')
            return None
        stock_order_record = self._make_stock_order_record(raw_record)
        self.StockOrderRecordList.append(stock_order_record)
        return stock_order_record

    def CancelOrder(self, stock_order_record):
        # stock_order_record = self.StockOrderRecord
        bs = stock_order_record.ord_bs
        branch = stock_order_record.Account[1:7].strip()
        account = stock_order_record.Account[7:15].strip()
        stock_id = stock_order_record.stock_id.strip()
        ord_type = stock_order_record.ord_type1 + stock_order_record.ord_type2
        ord_seq = stock_order_record.ord_seq
        ord_no = stock_order_record.ord_no
        pre_order = ' ' if int(ord_no) == 0 else 'N'
        raw_record = stock_cancel(bs, branch, account, stock_id, ord_type, ord_seq, ord_no, pre_order)
        if 'Error' in raw_record:
            print raw_record.decode('cp950').encode('utf8')
            return None
        stock_cancel_record = self._make_stock_order_record(raw_record)
        self.StockOrderRecordList.append(stock_cancel_record)
        return stock_cancel_record

    def _make_stock_order_record(self, raw_record):
        """stock_order_reply_record to StockOrderRecord struct."""
        # record = '01S9A95   98093152890  000000001360514201611102016111123171300000152000000B00S200委託處理中,
        # 請於交易時間確認委託狀態!                       '
        return self.StockOrderRecord._make(struct.unpack_from(self.StockOrderRecordfmt, raw_record))

    def GetAccount(self):
        return self._accounts

    def __load_account(self):
        account_list = show_list2().split('\n')
        for i, account in enumerate(account_list):
            if len(account) == 0:
                continue
            acc_type = account[0]
            acc_items = account[1:].split('-')
            acc_branch, acc_account, acc_name = acc_items[0], acc_items[1], acc_items[2]
            self._accounts[acc_type] = {'branch': acc_branch, 'account': acc_account, 'name': acc_name}
            add_acc_ca(acc_branch, acc_account, self.UserInfo['UserId'], self.UserInfo['eKey'],
                       self.UserInfo['eKeyPassword'])
