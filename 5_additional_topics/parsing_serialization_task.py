import glob
import json
import os
import numpy as np
from lxml import etree


def getting_json_paths():
    """Function that collects filepaths to json files"""

    return glob.glob('parsing_serialization_task/source_data/*/*.json')


def temp_wind_data(json_files):
    """Function that collects necessary parameters from json files, and calculates values
    for the cities."""

    data_dictionary = {}

    for json_file in json_files:
        city_name = str(os.path.basename(os.path.dirname(json_file))).replace(' ', '_')

        with open(json_file, 'r') as f:
            data = json.load(f)

            wind_speed_tab = [hour['wind_speed'] for hour in data['hourly']]
            temp_tab = [hour['temp'] for hour in data['hourly']]

            mean_wind_speed = np.round(np.mean(wind_speed_tab), 2)
            mean_temp = np.round(np.mean(temp_tab), 2)

            min_wind_speed = np.round(min(wind_speed_tab), 2)
            min_temp = np.round(min(temp_tab), 2)

            max_wind_speed = np.round(max(wind_speed_tab), 2)
            max_temp = np.round(max(temp_tab), 2)

            data_dictionary[city_name] = \
                {'mean_temp': mean_temp, 'mean_wind_speed': mean_wind_speed,
                 'min_temp': min_temp, 'min_wind_speed': min_wind_speed,
                 'max_temp': max_temp, 'max_wind_speed': max_wind_speed
                 }

    return data_dictionary


def weather_summary(data_dictionary):
    """Function that calculates values for the summary section."""

    cities_tab = list(data_dictionary.keys())
    all_temp_mean = [city['mean_temp'] for city in data_dictionary.values()]
    all_wind_speed_mean = [city['mean_wind_speed'] for city in data_dictionary.values()]

    global_temp_mean = np.round(np.mean(all_temp_mean), 2)
    global_wind_speed_mean = np.round(np.mean(all_wind_speed_mean), 2)

    coldest_place = cities_tab[all_temp_mean.index(min(all_temp_mean))]
    warmest_place = cities_tab[all_temp_mean.index(max(all_temp_mean))]
    windiest_place = cities_tab[all_wind_speed_mean.index(max(all_wind_speed_mean))]

    summary_result = {
        'mean_temp': global_temp_mean, 'mean_wind_speed': global_wind_speed_mean,
        'coldest_place': coldest_place, 'warmest_place': warmest_place,
        'windiest_place': windiest_place
    }

    return summary_result


def xml_writing(summary_result, data_dictionary):
    """Function that writes data to xml file."""

    summary_result_tuples = list(summary_result.items())
    weather = etree.Element('weather')
    summary = etree.SubElement(weather, 'summary')
    for result_tuple in summary_result_tuples:
        summary.set(str(result_tuple[0]), str(result_tuple[1]))
    cities = etree.SubElement(weather, 'cities')
    for city in data_dictionary.keys():
        attributes_tuples = list(data_dictionary[city].items())
        city = etree.SubElement(cities, str(city))
        for attribute in attributes_tuples:
            city.set(str(attribute[0]), str(attribute[1]))

    with open('weather_file.xml', 'wb') as f:
        f.write(etree.tostring(weather))


if __name__ == '__main__':
    data_dictionary = temp_wind_data(getting_json_paths())
    weather_summary = weather_summary(data_dictionary)
    xml_writing(weather_summary, data_dictionary)
