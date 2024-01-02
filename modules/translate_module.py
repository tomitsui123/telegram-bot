import configparser
import os

from google.cloud import translate_v2 as translate

config = configparser.ConfigParser()
config.read('../config.ini')
if os.getenv('ENV') == 'production':
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise Exception("Please set the GOOGLE_APPLICATION_CREDENTIALS")
translate_client = translate.Client()


def google_translate(text: str):
    target = 'zh-TW'
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]


if __name__ == '__main__':
    text = '今日天氣好好 right'
    # print(google_translate(text))
