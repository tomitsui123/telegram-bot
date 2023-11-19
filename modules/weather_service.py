# -*- coding: utf-8 -*-
import requests
import datetime
import imageio
import logging

url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc"
temperature_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"

TODAY_WEATHER = "forecastDesc"
OUTLOOK = "outlook"
UPDATE_TIME = "updateTime"

GENERAL_TEMP = 1
SHAUKEIWAN_TEMP = 17
KWUNTONG_TEMP = 22
SCIENCE_PARK_TEMP = 6

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def get_typhoon_info():
    typhoon_basic_info_url = "https://www.hko.gov.hk/probfcst/tc_spm.json"
    typhoon_basic_info_list = requests.get(typhoon_basic_info_url).json()
    desired_info_list = []
    for info in typhoon_basic_info_list["currentTC"]:
        typhoon_img_url = "https://www.hko.gov.hk/wxinfo/currwx/nwp_{}.png".format(info["id"])
        name = info["name_uc"]
        desired_info_list.append({"typhoon_img_url": typhoon_img_url, "name": name})
    return desired_info_list


def process_rain_graph():
    logger.info("Getting data from observatory")
    datetime_str_list = ["{}{:02d}{:02d}".format((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y%m%d"),
                                             (int(datetime.datetime.now().strftime("%H")) + 8) %24,
                                             x) for x in range(0, 60, 6)]
    radar_image_list = ["https://www.hko.gov.hk/wxinfo/radars/rad_064_png/2d064nradar_{}.jpg".format(x)
                        for x in datetime_str_list]
    images = []

    for image_url in radar_image_list:
        try:
            im = imageio.imread(image_url)
            print(image_url)
            images.append(im)
            images.append(im)
            images.append(im)
            images.append(im)

        except:
            print(image_url)

    imageio.mimsave('./radar.gif', images)


def get_weather_info_from_observatory():
    response = requests.get(url)
    res_json = response.json()
    reformat_datetime_str = datetime.datetime \
        .strptime(res_json[UPDATE_TIME].split('+')[0], "%Y-%m-%dT%H:%M:%S") \
        .strftime("%Y年%m月%d日 %H時%M分")
    today_weather = res_json[TODAY_WEATHER]
    return "氣溫:\n" \
           "觀塘： {kwun_tong_weather}度\n" \
           "筲箕灣： {skw_weather}度\n" \
           "科學園： {sci_park_temp}度\n" \
           "天氣預報:\n{today_weather}\n" \
           "`警告:\n{warning_message}`" \
           "\n\n更新時間:" \
           "\n{time}" \
        .format(time=reformat_datetime_str,
                today_weather=today_weather,
                kwun_tong_weather=get_temperature(KWUNTONG_TEMP),
                skw_weather=get_temperature(SHAUKEIWAN_TEMP),
                sci_park_temp=get_temperature(SCIENCE_PARK_TEMP),
                warning_message=get_warning_message())


def get_warning_message():
    res_json = requests.get(temperature_url).json()
    temp = "\n".join(res_json["warningMessage"])
    return temp


def get_temperature(district=GENERAL_TEMP):
    res_json = requests.get(temperature_url).json()
    district_temp = res_json["temperature"]["data"][district]["value"]
    return district_temp


if __name__ == '__main__':
    print(get_typhoon_info())
