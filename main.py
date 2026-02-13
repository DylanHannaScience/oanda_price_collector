# Standard Python
import argparse

# Local
from data_validation import DataValidator
from oanda import OandaAPIHelper


def run_price_collector(
):
    ## Accept arguments "start_date" and "end_date" from command line
    parser = argparse.ArgumentParser(description='Collect price data from Oanda')
    parser.add_argument('-s',
                        '--start_date',
                        type=str,
                        required=True,
                        help='Start date to begin SPXUSD price collection from (format: YYYY-MM-DD)')
    parser.add_argument('-e',
                        '--end_date',
                        type=str,
                        required=True,
                        help='End date to stop SPXUSD price collection at (format: YYYY-MM-DD)')

    args = parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date

    start_timestamp, end_timestamp = DataValidator.validate_dates_and_convert_to_timestamps(start_date=start_date,
                                                                                            end_date=end_date)
    OandaAPIHelper.download_spxusd_price_data(start_timestamp=start_timestamp, end_timestamp=end_timestamp)

    return

if __name__ == "__main__":
    run_price_collector()