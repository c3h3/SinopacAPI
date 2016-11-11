# coding=UTF-8
# __author__ == ypochien(at)gmail.com

from SinopacAPI import SinopacAPI

api = SinopacAPI()
# 先填好 config.json的設定值，讓api登入時讀取

# 登入
api.login()

# 產生下單資訊 - 現股買進永豐金3張 8.76元
order_object = api.MakeStockOrder(SinopacAPI.ORDER_TYPE_SPOT, "2890", 3, 8.76)

# 執行下單
order_stock_record = api.PlacingOrder(order_object)
print '下單回報:' + ','.join(order_stock_record[:-1]) + ',' + order_stock_record[-1].strip().decode('cp950').encode('utf8')

cancel_stock_record = api.CancelOrder(order_stock_record)

if cancel_stock_record is not None:
    print '刪單回報:' + ','.join(cancel_stock_record[:-1]) + ',' + cancel_stock_record[-1].strip().decode('cp950').encode(
        'utf8')
# 登出
api.logout()
