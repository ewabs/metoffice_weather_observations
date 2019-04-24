from collections import OrderedDict
from statistics import mean
from statistics import mode
import statistics
import requests
import json


class InvalidInput(Exception):
    pass


class MetofficeResponse:

    @staticmethod
    def _get_weather_data():

        API_KEY = ''
        METAOFFICE_URL = f"http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3772?res=hourly&key={API_KEY}"
        weather_response = requests.get(url=METAOFFICE_URL)

        try:
            weather_data = weather_response.json()
            with open('metoffice_response.json', 'w', encoding='utf8') as input_file:
                json.dump(weather_data, input_file, indent=4, ensure_ascii=False)

        except requests.exceptions.RequestException as exception:
            return f'Exception ocurred: {exception}'


class MetofficeAggregator:

    @staticmethod
    def _parse_json(day, raw_data):

        visibility = []
        temperature = []
        wind_speed = []
        wind_direction = []
        date = raw_data['SiteRep']['DV']['Location']['Period'][day]['value']
        date = date[:-1]
        observations_list = raw_data['SiteRep']['DV']['Location']['Period'][day]['Rep']

        for i in range(len(observations_list)):
            try:
                visibility.append(observations_list[i]['V'])
                temperature.append(observations_list[i]['T'])
                wind_speed.append(observations_list[i]['S'])
                wind_direction.append(observations_list[i]['D'])
            except KeyError:
                continue

        params = (visibility, temperature, wind_speed, wind_direction, date)

        return params

    @staticmethod
    def _aggregate_data(daily_obs_params):

        avg_visibility = mean([float(x) for x in daily_obs_params[0]])
        avg_temp = mean([float(x) for x in daily_obs_params[1]])
        avg_wind_speed = mean([float(x) for x in daily_obs_params[2]])
        try:
            most_freq_wind_direction = mode(daily_obs_params[3])
        except statistics.StatisticsError:
            most_freq_wind_direction = 'no dominating wind direction'

        date = daily_obs_params[4]
        aggregated_observations = [round(avg_visibility, 2) , round(avg_temp, 2), round(avg_wind_speed, 2), most_freq_wind_direction, date]

        return aggregated_observations

    @staticmethod
    def _format_daily_obs_data(aggregated_obs):

        daily_obs_dict = {
            "day": f"{aggregated_obs[4]}",
            "visibility": f"{aggregated_obs[0]}",
            "temperature": f"{aggregated_obs[1]}",
            "wind_speed": f"{aggregated_obs[2]}",
            "wind_direction": f"{aggregated_obs[3]}",
        }

        return daily_obs_dict

    @staticmethod
    def _format_report_dict(day0_obs_dict, day1_obs_dict):

        site_info = {
            "name": "London Heathrow",
            "country": "England",
            "observations": [day0_obs_dict, day1_obs_dict]
            }

        return site_info

    @staticmethod
    def _create_report(site_info):

        with open('metoffice_report.json', 'w', encoding='utf8') as input_file:
            json.dump(site_info, input_file, indent=4, ensure_ascii=False)

    @staticmethod
    def main(raw_data):
        try:
            if type(raw_data) != OrderedDict:
                raise InvalidInput(Exception)

            else:
                #day0
                observations_day0 = MetofficeAggregator._parse_json(0, raw_data)
                ag_day0 = MetofficeAggregator._aggregate_data(observations_day0)
                formatted_day0_data = MetofficeAggregator._format_daily_obs_data(ag_day0)

                #day1
                observations_day1 = MetofficeAggregator._parse_json(1, raw_data)
                ag_day1 = MetofficeAggregator._aggregate_data(observations_day1)
                formatted_day1_data = MetofficeAggregator._format_daily_obs_data(ag_day1)

                report_data = MetofficeAggregator._format_report_dict(formatted_day0_data, formatted_day1_data)
                MetofficeAggregator._create_report(report_data)

        except InvalidInput:
            return "invalid input"


if __name__ == '__main__':

    # get_weather_data() - not mentioned in task description,
    # added for updating weather data
    # can be turned off anytime,
    # then main() takes existing metoffice_response.json as an argument

    #MetofficeResponse._get_weather_data()

    with open('metoffice_response.json', 'r') as fp:
        raw_data = json.load(fp, object_pairs_hook=OrderedDict)
        MetofficeAggregator.main(raw_data)

