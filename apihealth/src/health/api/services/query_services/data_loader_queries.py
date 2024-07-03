import logging

from psycopg2 import Error as pgerror

from apihealth.src.health.api.services.query_services.session.session_manager import \
    DatabaseConnection


class DataLoaderQueries:
    def __init__(self, request_session=DatabaseConnection()):
        self.request_session = request_session

    def load_data_to_table(self, event_data):
        """
        Loads event data into the database.
        """
        try:
            with self.request_session as conn:
                with conn.cursor() as cursor:
                    insert_query = """
                        INSERT INTO us_event_data (
                            global_event_id, sql_date, event_code, event_base_code,
                            event_root_code, action_geo_full_name, action_geo_country_code,
                            action_geo_lat, action_geo_long, date_added, source_url, upload_date
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                        ) ON CONFLICT (global_event_id) DO NOTHING;
                    """
                    for index, row in event_data.iterrows():
                        cursor.execute(
                            insert_query,
                            (
                                row["GLOBALEVENTID"],
                                row["SQLDATE"].date(),
                                row["EventCode"],
                                row["EventBaseCode"],
                                row["EventRootCode"],
                                row["ActionGeo_FullName"],
                                row["ActionGeo_CountryCode"],
                                row["ActionGeo_Lat"],
                                row["ActionGeo_Long"],
                                row["DATEADDED"].date(),
                                row["SOURCEURL"],
                            ),
                        )
                    conn.commit()
                    logging.info("Data inserted successfully into the database")
        except pgerror as e:
            logging.error("Error occurred during database operation: %s", e)

    def fetch_latest_event_data(self) -> dict:
        """
        Fetches all records from the us_event_data table and returns them as a list of dictionaries.

        Returns:
            dict: A dictionary containing the result of the query. The keys are the column names,
                and the values are lists of column values.
                Returns None if an error occurs during the database operation.
        """
        try:
            with self.request_session as connection:
                cursor = connection.cursor()
                select_query = """
                    SELECT * FROM us_event_data
                """
                cursor.execute(select_query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                connection.commit()
                result = [dict(zip(columns, row)) for row in rows]
                return result
        except pgerror as e:
            logging.error("Error occurred during database operation: %s", e)
