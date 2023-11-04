Document Managment for CrowdNet NYC

1) Set up the google maps api, refer to documentation, set to sattelite view etc - DONE
2) Create the appropriate routes, at first add an add_data route (pretty much gets the data from the google maps api through fetch api) - DONE
3) Experiment with adding text before the user actually types in a statement  (make the user type in like 30 characters as a test, like wifi-password, username, trustworthy etc)
    3.1) Note if this works and the ideas implemented below work than use the openAI API in order to verify the data so it looks legit and add in a rating system 
4) If all works well up there, use the csv data files (if any) for NYC free public wifi, subway stations (as they have wifi), libraries, colleges (a lot of them have free guest wifi), schools (all of them should still have free wifi)
5) With the CSV file, parse through that data and based on where that data comes from add markers onto the map, all hoverable 
