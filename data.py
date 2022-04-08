from xToolkit import xfile
from pprint import pprint
import pandas as pd
import sys
record_l = xfile.read("/Users/andy/Desktop/新综合信息查询_委托流水.xls").excel_to_dict()

# pprint(record_l)
securities_l = []
date_l = []
action_l = []
fund_l = []
for record in record_l:
    securities_l.append(record.get('证券名称'))
    date_l.append(record.get('发生日期'))
    action_l.append(record.get('委托方向'))


securities_l = list(set(securities_l))

table_l = []

for securities in securities_l:

    # 获取证券所有数据
    securities_record_l = []
    for record in record_l:
        if record.get('证券名称') == securities:
            securities_record_l.append(record)

    # 获取所有日期
    securities_date_l = []
    for securities_record in securities_record_l:
        securities_date_l.append(securities_record.get('发生日期'))
    securities_date_l = list(set(securities_date_l))

    # 处理每个日期
    for securities_date in securities_date_l:
        one_day_securities_record_l = []
        for securities_record in securities_record_l:
            if securities_record.get('发生日期') == securities_date:
                one_day_securities_record_l.append(securities_record)

        # 处理同一天的数据

        # 统计单日所有基金名称
        fund_l = []
        for one_day_securities_record in one_day_securities_record_l:
            fund_l.append(one_day_securities_record.get('基金名称'))
        fund_l = list(set(fund_l))

        # 统计单日买入卖出
        sell_l = []
        buy_l = []
        for one_day_securities_record in one_day_securities_record_l:
            if one_day_securities_record.get('委托方向') == '卖出':
                sell_l.append(one_day_securities_record)
            elif one_day_securities_record.get('委托方向') == '买入':
                buy_l.append(one_day_securities_record)

        # 统计单日卖出各基金数量对比
        fund_trade_detail_l = []

        for fund in fund_l:
            sell_record_average_price = 0
            sell_record_price = 0
            sell_record_num = 0
            for sell in sell_l:
                if sell.get('基金名称') == fund:
                    record_price = sell.get('成交均价')
                    sell_record_price += record_price
                    sell_record_num += 1
            if sell_record_num > 0:
                sell_record_average_price = sell_record_price / sell_record_num

            buy_record_average_price = 0
            buy_record_price = 0
            buy_record_num = 0
            for buy in buy_l:
                if buy.get('基金名称') == fund:
                    record_price = buy.get('成交均价')
                    if record_price == 0:
                        break
                    buy_record_price += record_price
                    buy_record_num += 1
            if buy_record_num > 0:
                buy_record_average_price = buy_record_price / buy_record_num

            fund_trade_detail = {
                'fund': fund,
                'sell_record_average_price': sell_record_average_price,
                'buy_record_average_price': buy_record_average_price
            }

            fund_trade_detail_l.append(fund_trade_detail)

        record_1 = fund_trade_detail_l[0]
        if len(fund_trade_detail_l) == 2:
            record_2 = fund_trade_detail_l[1]
        else:
            print("单日只有一只股票交易 {securities} {date} {fund} ".
                  format(fund=record_1.get('fund'), date=securities_date, securities=securities))
            break

        fund1 = record_1.get('fund')
        fund2 = record_2.get('fund')
        record_1_buy_price = record_1.get('buy_record_average_price')
        record_2_buy_price = record_2.get('buy_record_average_price')
        record_1_sell_price = record_1.get('sell_record_average_price')
        record_2_sell_price = record_2.get('sell_record_average_price')

        # 计算买入差价
        diff_buy_price = 0
        if record_1_buy_price != 0 and record_2_buy_price != 0:
            diff_buy_price = (record_1_buy_price - record_2_buy_price) / record_1_buy_price

        # 计算卖出差价
        diff_sell_price = 0
        if record_1_sell_price != 0 and record_2_sell_price != 0:
            diff_sell_price = (record_1_sell_price - record_2_sell_price) / record_1_sell_price

        if diff_buy_price != 0:
            diff_buy_l = [securities_date, securities, fund1, fund2, "买入", record_1_buy_price, 
                          record_2_buy_price, '{:.4%}'.format(diff_buy_price)]
            table_l.append(diff_buy_l)

        if diff_sell_price != 0:
            diff_sell_l = [securities_date, securities, fund1, fund2, "卖出", record_1_sell_price, record_2_sell_price,
                           '{:.4%}'.format(diff_sell_price)]
            table_l.append(diff_sell_l)

name = ['日期', '证券名称', '基金名称1', '基金名称2', '委托方向', '基金1成交均价', '基金2成交均价', '差异=(基1均价-基2均价)/基1均价']

data = pd.DataFrame(columns=name, data=table_l)

data.to_csv('/Users/andy/Desktop/result.csv',encoding="utf_8_sig", float_format="%.4f")

pprint(table_l)
