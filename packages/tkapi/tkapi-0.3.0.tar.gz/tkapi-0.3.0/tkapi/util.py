import json
import datetime


def print_pretty(json_in):
    pretty_json = json.dumps(json_in, indent=4, sort_keys=True, ensure_ascii=False)
    print(pretty_json)


def datetime_to_odata(datetime_obj):
    return "datetime'" + datetime_obj.strftime('%Y-%m-%dT%H:%M:%S') + "'"


def odatedatetime_to_datetime(odate_datetime):
    return datetime.datetime.strptime(odate_datetime, '%Y-%m-%dT%H:%M:%S')
