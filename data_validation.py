# Standard Python
import copy
import datetime

# Third Party
import pandas as pd


EARLIEST_START_DATE_FOR_DATA = pd.to_datetime("2003-03-23 00:00:00+00:00")

class DataValidator:
    @staticmethod
    def validate_dates_and_convert_to_timestamps(start_date, end_date):

        validated_dates_as_timestamps = []

        for date_string in [start_date, end_date]:
            try:
                validated_date = pd.to_datetime(date_string, utc=True)
                validated_dates_as_timestamps.append(validated_date)
            except Exception as e:
                raise ValueError(f"""
                Error parsing dates: {e}
                Please ensure that both 'start_date' and 'end_date' are in the correct format: YYYY-MM-DD."
                """)

        validated_start_timestamp, validated_end_timestamp = validated_dates_as_timestamps

        validated_end_timestamp = correct_end_timestamp_for_market_close(start_timestamp=validated_start_timestamp,
                                                                         end_timestamp=validated_end_timestamp)

        if validated_start_timestamp >= validated_end_timestamp:
            raise ValueError("Start date must be before end date.")

        if validated_start_timestamp < EARLIEST_START_DATE_FOR_DATA:
            raise ValueError(f"""
            No data for SPXUSD exists before {EARLIEST_START_DATE_FOR_DATA.date()}. 
            Please specify a start date on or after {EARLIEST_START_DATE_FOR_DATA.date()}.
            """)

        today_date = pd.to_datetime(datetime.date.today(), utc=True)

        if validated_end_timestamp > today_date:
            raise ValueError(f"""
            End date cannot be in the future. Please specify an end date on or before {today_date.date()}.
            """)

        return validated_start_timestamp, validated_end_timestamp

def correct_end_timestamp_for_market_close(start_timestamp, end_timestamp):

    end_timestamp_before_correction = copy.deepcopy(end_timestamp)

    # Compute how many days have passed since the most recent Friday
    days_since_friday = (end_timestamp.dayofweek - 4) % 7

    # Get the most recent Friday (same day if end_ts is Friday)
    timestamp_shifted_to_previous_friday = end_timestamp - pd.Timedelta(days=days_since_friday)
    previous_market_close_index = timestamp_shifted_to_previous_friday.replace(hour=22, minute=0, second=0)

    # Closed window: [Friday 22:00, Sunday 22:00]
    next_market_open_index = previous_market_close_index + pd.Timedelta(days=2)

    if previous_market_close_index <= end_timestamp < next_market_open_index:
        end_timestamp = previous_market_close_index - datetime.timedelta(seconds=60)

    if (end_timestamp < start_timestamp) and (end_timestamp_before_correction > start_timestamp):
        raise ValueError(f"""
        Your given end date of {end_timestamp_before_correction} falls within a market-closed window 
        (Friday 22:00 UTC through Sunday 22:00 UTC), so was moved to the nearest previous Friday.
        However, after this correction, the end date '{end_timestamp}' is before the start date of '{start_timestamp}'.
        Please specify start and end dates that are not during a market-closed window (Friday 22:00 UTC 
        through Sunday 22:00 UTC).
        """)

    return end_timestamp
