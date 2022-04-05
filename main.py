# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import http.client
from datetime import datetime
from datetime import timedelta
import json

#get data for every day from the date specified until now
def reportCountiesFromAPI(day):

    while day < datetime.now():
        try:
            conn = http.client.HTTPSConnection("idph.illinois.gov")
            payload = ''
            headers = {}
            datestr = day.strftime("%m/%d/%Y")

            conn.request("GET", f'/DPHPublicInformation/api/COVID/GetCountyHistoricalTestResults?reportDate={datestr}', payload,
                         headers)
            res = conn.getresponse()
            data = res.read()

            # returns JSON object as a dictionary
            jsondata = json.loads(data.decode("utf-8"))
            print(datestr)
            # Iterating through the json
            #print(jsondata['characteristics_by_county'])
            for i in jsondata['characteristics_by_county']:
                # print(i['CountyName'])
                if (i['CountyName'] == 'Cook') or (i['CountyName'] == 'Chicago') :
                    print(f'{i["CountyName"]}: {i["tested"]}\t{i["confirmed_cases"]}\t{i["deaths"]}')
                if (i['CountyName'] == 'Illinois') :
                    #different format for the whole state
                    # - basically I copy paste it and the order of fields is different
                    print(f'{i["CountyName"] }: { i["confirmed_cases"] }\t{ i["deaths"] }\t\t{ i["tested"] }')

        except Exception as inst:
            print(inst)

        day += timedelta(days=1)

#get data for every day from the date specified until now
def getZipData(day):
    currentDay = day
    # for day in days:
    while currentDay < datetime.now():
        jsondata = {}
        try:
            conn = http.client.HTTPSConnection("idph.illinois.gov")
            payload = ''
            headers = {}
            datestr = currentDay.strftime("%m/%d/%Y")

            conn.request("GET", f'/DPHPublicInformation/api/COVID/GetZip?reportDate={datestr}', payload,
                         headers)
            res = conn.getresponse()
            data = res.read()
            # returns JSON object as
            # a dictionary
            jsondata = json.loads(data.decode("utf-8"))

            print(datestr)
        except Exception as inst:
            print(inst)

        # Iterating through the json
        # print(jsondata['characteristics_by_county'])
        for i in jsondata['zip_values']:
            # print(i['CountyName'])
            if (i['zip'] == '60622'):
                print(f'{i["zip"]}: {i["total_tested"]}\t{i["confirmed_cases"]}')
        currentDay += timedelta(days=1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startDay = datetime(2022, 3, 25)
    reportCountiesFromAPI(startDay)
    getZipData(startDay)

