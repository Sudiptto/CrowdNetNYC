import pandas as pd

# NOTE FOR READERS:
""""
This python file is meant to test the NYC OPENDATA, places that can have free wifi, like colleges, public libraries, nyc internet spots, etc
Python file as of now should not re-set over and over, one time ordeal, this an addition to the data that is crowd sourced by the users
"""


# DATA FOR FILE: https://data.cityofnewyork.us/Social-Services/internet-connection-nyc/k9p3-ztqv  (source of original csv data)

# KEY NOTES ABOUT THIS DATA
# 1) Crowd sourced data to from residents of NYC , also includes data from NYC linktree and MTA data (THERE IS WIFI ON THE MTA!)

#nycWifi = pd.read_csv('nycWifi.csv')

#print(nycWifi['SSID'].value_counts())
"""
Results from the Data above are (Note's all the SSID, service set identifiers, some common ones include GuestWifi, TransitWirelessWifi (MTA) and more):
Instances 
LinkNYC Free Wi-Fi          629
GuestWiFi                   580
TransitWirelessWiFi         276
Harlem Wi-Fi                128
Downtown Brooklyn WiFi      100
NYPL                         90
QBPL_WIRELESS                65
BPLUNWIRED                   59
DowntownBrooklynWiFi_Fon     39
#DwtwnAllianceFreeWiFi       36
CICFreeWiFi                  30
attwifi                      27
unionsquarewifi               1
BryantPark.org                1
"""

# NOTE ORGANIZE THE DATA BELOW, so it goes from LinkNYC Free Wi-fi, than Guest-WiFi, etc. Only get the lat/long data, ssid and type. MAKE NEW CSV FILE
# get the latitude, longitude, ssid and type
#selected_columns = ['LAT', 'LON', 'SSID', 'TYPE']
#filtered_df = nycWifi[selected_columns]
#filtered_df.to_csv('nycWifiFilter.csv', index=False) # save as new csv file

# USE THE NYCWIFIFILTER.CSV 
# Read the filtered data CSV file
"""nycWifiFilter = pd.read_csv('nycWifiFilter.csv')

# Sort the DataFrame by the 'SSID' column in descending order and reset the index
nycWIFI = nycWifiFilter.sort_values(by='SSID', ascending=False).reset_index(drop=True)

# Save the sorted data to a new CSV file
nycWIFI.to_csv('NycHotspots.csv', index=False)

print("Sorted data saved to NycHotspots.csv")"""


new_test = pd.read_csv('NycHotspots.csv')
print(new_test['SSID'].value_counts())





