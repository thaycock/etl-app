import logging

from pandas import DataFrame

from apihealth.src.health.api.services.loaders.api_loader import APILoader


class ETLLoader(APILoader):
    def __init__(self, url) -> None:
        self.url = url

    def load_data_from_endpoint(self) -> DataFrame:
        # TODO handle this better
        extracted_data = self.load_data_from_source(self.url)
        if extracted_data:
            return True
