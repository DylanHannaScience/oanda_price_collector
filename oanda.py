# Third-party
import pandas as pd
import requests

# Local
from config.settings import ACCOUNT_ID, API_TOKEN, logger
from data_io import DataIOHelper

OANDA_BASE_URL = f"https://api-fxtrade.oanda.com/v3/accounts/{ACCOUNT_ID}"

API_HEADERS = {"Authorization": f"Bearer {API_TOKEN}",
               "X-Accept-Datetime-Format": "RFC3339",
               "Content-Type": "application/json"}

class OandaAPIHelper:

    @staticmethod
    def download_spxusd_price_data(start_timestamp, end_timestamp):

        current_timestamp_to_sample_from = start_timestamp

        sampled_candles = []

        while current_timestamp_to_sample_from <= end_timestamp:

            logger.info(f"Polling data from {current_timestamp_to_sample_from.strftime('%Y-%m-%d')}...")

            instrument_candles_response = requests.get(
                f"{OANDA_BASE_URL}/instruments/SPX500_USD/candles?granularity=D&from={current_timestamp_to_sample_from}&count=5000&price=BA",
                headers=API_HEADERS).json()

            sampled_candles += instrument_candles_response['candles']

            final_candle_timestamp_in_response = pd.to_datetime(instrument_candles_response['candles'][-1]['time'])

            if final_candle_timestamp_in_response >= end_timestamp:
                break
            else:
                current_timestamp_to_sample_from = final_candle_timestamp_in_response

        for candle_index in range(len(sampled_candles)):
            sampled_candles[candle_index]['bid'] = sampled_candles[candle_index]['bid']['o']
            sampled_candles[candle_index]['ask'] = sampled_candles[candle_index]['ask']['o']

        sampled_price_df = pd.DataFrame(sampled_candles)
        sampled_price_df['time'] = pd.to_datetime(sampled_price_df['time'])
        sampled_price_df['bid'] = sampled_price_df['bid'].astype(float)
        sampled_price_df['ask'] = sampled_price_df['ask'].astype(float)
        sampled_price_df.set_index("time", inplace=True)

        # Removing duplicate rows
        sampled_price_df = sampled_price_df[~sampled_price_df.index.duplicated()]

        # Removing rows that are after the end_timestamp
        sampled_price_df = sampled_price_df[sampled_price_df.index <= end_timestamp]

        # Removing rows where price data is not yet complete, and then dropping 'complete' column:
        sampled_price_df = sampled_price_df[sampled_price_df.complete]
        sampled_price_df = sampled_price_df.drop(labels=["complete"], axis=1)

        start_year = start_timestamp.year
        end_year = end_timestamp.year

        for sampled_year in range(start_year, end_year + 1):
            year_price_df = sampled_price_df.loc[str(sampled_year)]
            DataIOHelper.save_spxusd_price_data_for_single_year(year_data=year_price_df, year=sampled_year)

        return

