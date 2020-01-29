# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/1/15 0:25
# @Author   : Fangyang
# @Software : PyCharm


import pandas as pd

from pytdx.exhq import TdxExHq_API
# from ips import IPsSource
from jnpy.DataSource.pytdx.ips import IPsSource
from jnpy.DataSource.pytdx.log import LogModule
from jnpy.DataSource.pytdx.constant import KBarType


class ExhqAPI(TdxExHq_API):

    def __init__(self):
        super(ExhqAPI, self).__init__()
        self.info_log = LogModule(name="ExhqAPI_info", level="info")
        self.err_log = LogModule(name="ExhqAPI_error", level="error")

    def get_all_KBars_df(self,
                         category=KBarType.KLINE_TYPE_DAILY.value,
                         market=30, code="FU2006") -> pd.DataFrame:  # 29 LL8  FUL8 主链
        '''
        category=KBarType.KLINE_TYPE_DAILY.value

        market 信息可以通过 data_df = ex_api.to_df(ex_api.get_markets()) 获得

        '''
        result_df = pd.DataFrame()
        start = 0
        count = 500

        while True:
            self.info_log.write_log(f"开始获取{start}条数据...")
            df = self.to_df(
                self.get_instrument_bars(
                    category=category,
                    market=market, code=code, start=start, count=500
                )
            )

            if df.shape[0] == 0 | (("value" in df.columns) and (df["value"][0] is None)):
                break
            result_df = pd.concat([df, result_df], axis=0, ignore_index=True)
            start += count

        if result_df.shape[0] == 0:
            self.info_log.write_log(f"{code} 数据条数为 0 !")
            return result_df

        select_columns_list = ["open", "high", "low", "close", "position", "trade", "datetime"]
        result_df = result_df[select_columns_list]

        result_df['datetime'] = pd.to_datetime(result_df['datetime'])
        return result_df

    def get_all_Ticks_df(self,
                         category=KBarType.KLINE_TYPE_DAILY.value,
                         market=30, date=20191227, code="FU2006") -> pd.DataFrame:  # 29 LL8  FUL8 主链
        '''
        category=KBarType.KLINE_TYPE_DAILY.value

        market 信息可以通过 data_df = ex_api.to_df(ex_api.get_markets()) 获得

        '''
        result_df = pd.DataFrame()
        start = 0
        count = 1800

        while True:
            self.info_log.write_log(f"开始获取{start}条数据...")
            df = self.to_df(
                self.get_history_transaction_data(
                    # category=category,
                    market=market, code=code, date=date, start=start, count=count
                )
            )

            if df.shape[0] == 0 | (("value" in df.columns) and (df["value"][0] is None)):
                break
            result_df = pd.concat([df, result_df], axis=0, ignore_index=True)
            start += count

        if result_df.shape[0] == 0:
            self.info_log.write_log(f"{code} 数据条数为 0 !")
            return result_df

        select_columns_list = ["price", "volume", "zengcang", "natrue_name", "direction", "date"]  # 好像是时间相关,暂时不用"nature"]
        result_df = result_df[select_columns_list]

        result_df['date'] = pd.to_datetime(result_df['date'])
        return result_df


if __name__ == '__main__':
    ip, port = IPsSource().get_fast_exhq_ip()
    # ex_api = TdxExHq_API()
    ex_api = ExhqAPI()
    with ex_api.connect(ip, port):
        data_df = ex_api.to_df(ex_api.get_markets())

        # ex_api.update_contracts_info_by_ctp_gateway()

        from constant import FutureMarketCode

        params_dict = {
            "category": KBarType.KLINE_TYPE_1HOUR.value,
            "market": FutureMarketCode.INE.value,
            "code": "SCL8",
        }
        # df = ex_api.get_all_KBars_df(**params_dict)

        params_dict['date'] = 20191227
        df = ex_api.get_all_Ticks_df(**params_dict)
        print(1)
