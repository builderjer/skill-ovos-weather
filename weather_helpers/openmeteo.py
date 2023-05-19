import requests
# TODO - get rid of relative imports
# /home/miro/PycharmProjects/.venvs/ovos/bin/python /home/miro/PycharmProjects/skill-ovos-weather/weather_helpers/openmeteo.py
# Traceback (most recent call last):
#   File "/home/miro/PycharmProjects/skill-ovos-weather/weather_helpers/openmeteo.py", line 3, in <module>
#     from .config import *
# ImportError: attempted relative import with no known parent package
# so annoying
from .config import *
from .weather import WeatherReport
from ovos_utils import timed_lru_cache


@timed_lru_cache(seconds=60*15)  # cache for 15 mins
def get_report(cfg: WeatherConfig):
    if cfg.speed_unit == MILES_PER_HOUR:
        windspeed_unit = "mph"
    elif cfg.speed_unit == METERS_PER_SECOND:
        windspeed_unit = "ms"
    elif cfg.speed_unit == KILOMETERS_PER_HOUR:
        windspeed_unit = "kmh"
    else:
        raise ValueError("invalid speed unit")

    if cfg.temperature_unit == CELSIUS:
        temperature_unit = "celsius"
    elif cfg.speed_unit == FAHRENHEIT:
        temperature_unit = "fahrenheit"
    else:
        raise ValueError("invalid temperature unit")

    if cfg.precipitation_unit == MILLIMETERS:
        precipitation_unit = "mm"
    elif cfg.speed_unit == INCH:
        precipitation_unit = "inch"
    else:
        raise ValueError("invalid precipitation unit")

    daily_params = [
        "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",
        "apparent_temperature_min",
        "precipitation_sum",
        "precipitation_hours",
        "weathercode",
        "sunrise",
        "sunset",
        "windspeed_10m_max",
        "windgusts_10m_max",
        "winddirection_10m_dominant",
        "shortwave_radiation_sum",
        "et0_fao_evapotranspiration",
        "uv_index_max",
        "precipitation_probability_mean",
        "precipitation_probability_min",
        "precipitation_probability_max",
        "uv_index_clear_sky_max"]
    hourly_params = ["temperature_2m",
                     "relativehumidity_2m",
                     "dewpoint_2m",
                     "apparent_temperature",
                     "pressure_msl",
                     "surface_pressure",
                     "cloudcover",
                     "cloudcover_low",
                     "cloudcover_mid",
                     "cloudcover_high",
                     "windspeed_10m",
                     "windspeed_80m",
                     "windspeed_120m",
                     "windspeed_180m",
                     "winddirection_10m",
                     "winddirection_80m",
                     "winddirection_120m",
                     "winddirection_180m",
                     "windgusts_10m",
                     "shortwave_radiation",
                     "direct_radiation",
                     "diffuse_radiation",
                     "vapor_pressure_deficit",
                     "cape",
                     "evapotranspiration",
                     "et0_fao_evapotranspiration",
                     "precipitation",
                     "weathercode",
                     "snow_depth",
                     "showers",
                     "snowfall",
                     "visibility",
                     "precipitation_probability",
                     "freezinglevel_height",
                     "soil_temperature_0cm",
                     "soil_temperature_6cm",
                     "soil_temperature_18cm",
                     "soil_temperature_54cm",
                     "soil_moisture_0_1cm",
                     "soil_moisture_1_3cm",
                     "soil_moisture_3_9cm",
                     "soil_moisture_9_27cm",
                     "soil_moisture_27_81cm",
                     "is_day"]

    args = {
        "longitude": cfg.longitude,
        "latitude": cfg.latitude,
        "hourly": ','.join(hourly_params),
        "daily": ','.join(daily_params),
        "current_weather": True,
        "temperature_unit": temperature_unit,  # fahrenheit
        "windspeed_unit": windspeed_unit,  # ms, mph, kn
        "precipitation_unit": precipitation_unit,  # inch
        "timezone": cfg.timezone  # gmt ...
    }
    url = f"https://api.open-meteo.com/v1/forecast"
    data = requests.get(url, params=args).json()
    return WeatherReport(data)


if __name__ == "__main__":
    from pprint import pprint

    cfg = WeatherConfig()
    pprint(get_report(cfg))
    # {'current_weather': {'is_day': 1,
    #                      'temperature': 25.7,
    #                      'time': '2023-05-18T12:00',
    #                      'weathercode': 0,
    #                      'winddirection': 236.0,
    #                      'windspeed': 2.88},
    #  'daily': {'apparent_temperature_max': [29.2,
    #                                         20.3,
    #                                         19.9,
    #                                         25.1,
    #                                         25.0,
    #                                         27.4,
    #                                         30.3],
    #            'apparent_temperature_min': [13.8, 9.4, 6.4, 8.1, 10.4, 15.0, 15.6],
    #            'et0_fao_evapotranspiration': [5.8,
    #                                           2.67,
    #                                           4.78,
    #                                           5.2,
    #                                           3.65,
    #                                           5.22,
    #                                           5.39],
    #            'precipitation_hours': [0.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    #            'precipitation_sum': [0.0, 4.4, 0.0, 0.0, 0.1, 0.0, 0.0],
    #            'shortwave_radiation_sum': [27.64,
    #                                        12.03,
    #                                        30.57,
    #                                        29.96,
    #                                        18.75,
    #                                        26.7,
    #                                        27.13],
    #            'sunrise': ['2023-05-18T06:04',
    #                        '2023-05-19T06:03',
    #                        '2023-05-20T06:02',
    #                        '2023-05-21T06:01',
    #                        '2023-05-22T06:01',
    #                        '2023-05-23T06:00',
    #                        '2023-05-24T05:59'],
    #            'sunset': ['2023-05-18T20:30',
    #                       '2023-05-19T20:31',
    #                       '2023-05-20T20:32',
    #                       '2023-05-21T20:33',
    #                       '2023-05-22T20:34',
    #                       '2023-05-23T20:34',
    #                       '2023-05-24T20:35'],
    #            'temperature_2m_max': [28.4, 20.4, 19.8, 23.3, 23.2, 25.4, 27.7],
    #            'temperature_2m_min': [14.1, 12.4, 8.6, 9.5, 11.4, 15.4, 15.6],
    #            'time': ['2023-05-18',
    #                     '2023-05-19',
    #                     '2023-05-20',
    #                     '2023-05-21',
    #                     '2023-05-22',
    #                     '2023-05-23',
    #                     '2023-05-24'],
    #            'uv_index_clear_sky_max': [7.95, 8.0, 8.0, 8.0, 7.85, 7.65, 7.65],
    #            'uv_index_max': [7.85, 3.55, 8.0, 8.0, 7.7, 7.3, 7.7],
    #            'weathercode': [2, 63, 0, 3, 51, 3, 2],
    #            'winddirection_10m_dominant': [220, 357, 23, 130, 120, 142, 161],
    #            'windgusts_10m_max': [6.5, 10.5, 6.6, 2.6, 7.6, 7.7, 5.9],
    #            'windspeed_10m_max': [3.56, 6.26, 3.72, 3.23, 4.46, 3.36, 3.11]},
    #  'daily_units': {'apparent_temperature_max': '°C',
    #                  'apparent_temperature_min': '°C',
    #                  'et0_fao_evapotranspiration': 'mm',
    #                  'precipitation_hours': 'h',
    #                  'precipitation_sum': 'mm',
    #                  'shortwave_radiation_sum': 'MJ/m²',
    #                  'sunrise': 'iso8601',
    #                  'sunset': 'iso8601',
    #                  'temperature_2m_max': '°C',
    #                  'temperature_2m_min': '°C',
    #                  'time': 'iso8601',
    #                  'uv_index_clear_sky_max': '',
    #                  'uv_index_max': '',
    #                  'weathercode': 'wmo code',
    #                  'winddirection_10m_dominant': '°',
    #                  'windgusts_10m_max': 'm/s',
    #                  'windspeed_10m_max': 'm/s'},
    #  'elevation': 265.0,
    #  'generationtime_ms': 1.194000244140625,
    #  'latitude': 38.96149,
    #  'longitude': -95.25131,
    #  'timezone': 'America/Chicago',
    #  'timezone_abbreviation': 'CDT',
    #  'utc_offset_seconds': -18000}
    # {'current_weather': {'is_day': 1,
    #                      'temperature': 25.7,
    #                      'time': '2023-05-18T12:00',
    #                      'weathercode': 0,
    #                      'winddirection': 236.0,
    #                      'windspeed': 2.88},
    #  'daily': {'apparent_temperature_max': [29.2,
    #                                         20.3,
    #                                         19.9,
    #                                         25.1,
    #                                         25.0,
    #                                         27.4,
    #                                         30.3],
    #            'apparent_temperature_min': [13.8, 9.4, 6.4, 8.1, 10.4, 15.0, 15.6],
    #            'et0_fao_evapotranspiration': [5.8,
    #                                           2.67,
    #                                           4.78,
    #                                           5.2,
    #                                           3.65,
    #                                           5.22,
    #                                           5.39],
    #            'precipitation_hours': [0.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    #            'precipitation_sum': [0.0, 4.4, 0.0, 0.0, 0.1, 0.0, 0.0],
    #            'shortwave_radiation_sum': [27.64,
    #                                        12.03,
    #                                        30.57,
    #                                        29.96,
    #                                        18.75,
    #                                        26.7,
    #                                        27.13],
    #            'sunrise': ['2023-05-18T06:04',
    #                        '2023-05-19T06:03',
    #                        '2023-05-20T06:02',
    #                        '2023-05-21T06:01',
    #                        '2023-05-22T06:01',
    #                        '2023-05-23T06:00',
    #                        '2023-05-24T05:59'],
    #            'sunset': ['2023-05-18T20:30',
    #                       '2023-05-19T20:31',
    #                       '2023-05-20T20:32',
    #                       '2023-05-21T20:33',
    #                       '2023-05-22T20:34',
    #                       '2023-05-23T20:34',
    #                       '2023-05-24T20:35'],
    #            'temperature_2m_max': [28.4, 20.4, 19.8, 23.3, 23.2, 25.4, 27.7],
    #            'temperature_2m_min': [14.1, 12.4, 8.6, 9.5, 11.4, 15.4, 15.6],
    #            'time': ['2023-05-18',
    #                     '2023-05-19',
    #                     '2023-05-20',
    #                     '2023-05-21',
    #                     '2023-05-22',
    #                     '2023-05-23',
    #                     '2023-05-24'],
    #            'uv_index_clear_sky_max': [7.95, 8.0, 8.0, 8.0, 7.85, 7.65, 7.65],
    #            'uv_index_max': [7.85, 3.55, 8.0, 8.0, 7.7, 7.3, 7.7],
    #            'weathercode': [2, 63, 0, 3, 51, 3, 2],
    #            'winddirection_10m_dominant': [220, 357, 23, 130, 120, 142, 161],
    #            'windgusts_10m_max': [6.5, 10.5, 6.6, 2.6, 7.6, 7.7, 5.9],
    #            'windspeed_10m_max': [3.56, 6.26, 3.72, 3.23, 4.46, 3.36, 3.11]},
    #  'daily_units': {'apparent_temperature_max': '°C',
    #                  'apparent_temperature_min': '°C',
    #                  'et0_fao_evapotranspiration': 'mm',
    #                  'precipitation_hours': 'h',
    #                  'precipitation_sum': 'mm',
    #                  'shortwave_radiation_sum': 'MJ/m²',
    #                  'sunrise': 'iso8601',
    #                  'sunset': 'iso8601',
    #                  'temperature_2m_max': '°C',
    #                  'temperature_2m_min': '°C',
    #                  'time': 'iso8601',
    #                  'uv_index_clear_sky_max': '',
    #                  'uv_index_max': '',
    #                  'weathercode': 'wmo code',
    #                  'winddirection_10m_dominant': '°',
    #                  'windgusts_10m_max': 'm/s',
    #                  'windspeed_10m_max': 'm/s'},
    #  'elevation': 265.0,
    #  'generationtime_ms': 2.295970916748047,
    #  'latitude': 38.96149,
    #  'longitude': -95.25131,
    #  'timezone': 'America/Chicago',
    #  'timezone_abbreviation': 'CDT',
    #  'utc_offset_seconds': -18000}
