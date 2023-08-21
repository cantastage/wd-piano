import pandas as pd


class DataService(object):
    """
    Class used to provide data to the model
    """

    _instance = None  # singleton instance

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(DataService, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_piano_strings(cls):
        df = pd.read_excel('./unwrapped_strings_data.xlsx', sheet_name='UNWRAPPED STRINGS')
        print(df)
        strings = df.iloc[:, 2:].tojson(orient='records')
        return strings
