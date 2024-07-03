import io
import logging
import zipfile as zip
from typing import Any
from zipfile import BadZipFile, LargeZipFile

import pandas as pd
import requests


class APILoader:
    """
    Base class API Loader to facilitate with HTTP requests
    """

    def load_data_from_source(self, target_url: str, is_json=False) -> Any:
        """
        Loads data from a source, handles both JSON and ZIP files

        Args:
            target_url (str): The URL to fetch data from
            is_json (bool, optional): Flag to indicate if the response is JSON. Defaults to False.

        Returns:
            Any: The loaded data
        """
        try:
            response = requests.get(target_url)
            response.raise_for_status()
            if is_json:
                return response.json()
            else:
                return self.__extract_zip_file(response)
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.RequestException,
        ) as err:
            logging.exception(
                f"Error while fetching data from source: {target_url}, error: {err}"
            )

    def __extract_zip_file(self, response) -> pd.DataFrame:
        """
        Extracts the zip file data, this assumes the zip file is static in context of what we can expect

        Args:
            response (_type_):

        Returns:
            pd.DataFrame: _description_
        """
        try:
            with zip.ZipFile(io.BytesIO(response.content)) as thezip:
                with thezip.open(thezip.namelist()[0]) as thefile:
                    try:
                        column_names = [
                            "GLOBALEVENTID",
                            "SQLDATE",
                            "EventCode",
                            "EventBaseCode",
                            "EventRootCode",
                            "ActionGeo_FullName",
                            "ActionGeo_CountryCode",
                            "ActionGeo_Lat",
                            "ActionGeo_Long",
                            "DATEADDED",
                            "SOURCEURL",
                        ]
                        df = pd.read_csv(
                            thefile,
                            delimiter="\t",
                            header=None,
                            usecols=[0, 1, 26, 27, 28, 52, 53, 56, 57, 59, 60],
                        )
                        df.columns = column_names

                        df["SQLDATE"] = pd.to_datetime(df["SQLDATE"], format="%Y%m%d")
                        df["DATEADDED"] = pd.to_datetime(df["SQLDATE"], format="%Y%m%d")
                        df["ActionGeo_Lat"] = pd.to_numeric(
                            df["ActionGeo_Lat"], errors="coerce"
                        )
                        df["ActionGeo_Long"] = pd.to_numeric(
                            df["ActionGeo_Long"], errors="coerce"
                        )
                        # Drop rows with no long/lat
                        df.dropna(
                            subset=["ActionGeo_Lat", "ActionGeo_Long"], inplace=True
                        )
                        # Filter for US events only
                        us_events = df[
                            (df["ActionGeo_Lat"] >= 24.396308)
                            & (df["ActionGeo_Lat"] <= 49.384358)
                            & (df["ActionGeo_Long"] >= -125.0)
                            & (df["ActionGeo_Long"] <= -66.93457)
                        ]
                        logging.info(f"Filtered US events head: {us_events.head()}")
                        return us_events
                    except pd.errors.ParserError as e:
                        logging.exception(
                            f"ParserError while reading the CSV file: {e}"
                        )
                    except pd.errors.EmptyDataError as e:
                        logging.exception(
                            f"EmptyDataError: No data in the CSV file: {e}"
                        )

        except zip.BadZipFile as err:
            logging.exception(f"Error: Bad ZIP file: {err}")
        except zip.LargeZipFile as err:
            logging.exception(f"Error: ZIP file is too large: {err}")
        except KeyError as err:
            logging.exception(f"Error: File not found in the ZIP archive: {err}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"HTTP Request failed: {e}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
