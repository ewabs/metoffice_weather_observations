# Metoffice weather observations

Script creating report containing aggregated weather observations in London Heathrow for last 25 hours/2 days
basing on Metoffice data https://www.metoffice.gov.uk/

Schema:
1. Downloading weather data from Metoffice API > json file
2. Parsing json file to fetch data about : date, visibility, temperature, wind speed, wind direction
3. Aggregating fetched data
4. Creating weather report for last 25 hours (divided into 2 separate dictionaries, one for each day) > json file

No enviroment, for executing recuired:
- Python >= 3.6
- requests

Testing
-Unit tests for main() function from MetofficeAggregator class

