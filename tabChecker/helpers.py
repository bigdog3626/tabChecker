import pandas as pd
import json
import pprint


class AttendeeData():

    def __init__(self, file):
        data = pd.read_excel(file, sheet_name='Sheet1')
        json_str = data.to_json(orient='records')
        self.parsed = json.loads(json_str)


    def userInfoDict(self, z):
        return self.parsed[z]






