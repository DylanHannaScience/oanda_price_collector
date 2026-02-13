# Standard Python
import os

# Local
from config.settings import SPXUSD_DATA_DIR


class DataIOHelper:

    @staticmethod
    def save_spxusd_price_data_for_single_year(year_data, year):
        """
        Takes a pandas DataFrame for a given years' worth of spxusd_data, and saves it to disk as a CSV. Will
        over-write the existing CSV if there's already one there for that year.

        :param year_data: pandas DataFrame containing SPXUSD price data for a given year.
        :param year: Year you would like to label the CSV file you are saving with. For example, if 'year' is '2004',
        the CSV file will be saved as 'spxusd_2004.csv'.
        """

        if not os.path.exists(SPXUSD_DATA_DIR):
            os.makedirs(SPXUSD_DATA_DIR)

        year_data.to_csv(f"{SPXUSD_DATA_DIR}/spxusd_{year}.csv", index="time")
