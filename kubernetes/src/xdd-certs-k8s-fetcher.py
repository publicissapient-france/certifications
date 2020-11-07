from __future__ import print_function
import csv
import requests
import os.path

from spreadsheet import downloadSpreadsheet, parseSpreadsheetRows

#def testConfig():
#    print("Current environment: " + settings.current_env)
#    print(settings.log_level)
#    print(settings.spreadsheet_id)
#    print(settings.service_account_file_path)



def main():
    spreadsheet = downloadSpreadsheet()
    parseSpreadsheetRows(spreadsheet)

    #output_file = f'bla.csv'

    #with open(output_file, 'w') as f:
    #    writer = csv.writer(f)
    #    writer.writerows(spreadsheet.get('values'))

    #f.close()

if __name__ == '__main__':
    main()
    #testConfig()
