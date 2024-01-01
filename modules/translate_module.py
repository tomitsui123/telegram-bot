import configparser
import os

from google.cloud import translate_v2 as translate
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from langdetect import detect
import re
import spacy

config = configparser.ConfigParser()
config.read('../config.ini')
if os.getenv('ENV') == 'production':
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise Exception("Please set the GOOGLE_APPLICATION_CREDENTIALS")
translate_client = translate.Client()
nlp = spacy.load('zh_core_web_lg')


def get_lang_detector(nlp, name):
    return LanguageDetector()


Language.factory('language-detector', func=get_lang_detector)
nlp.add_pipe('language-detector', last=True)


def google_translate(text: str):
    target = 'zh-TW'
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]


def is_foreign_language(_text: str) -> bool:
    doc = nlp(_text)
    is_chi = 'zh' in doc._.language.get('language')
    is_eng = doc._.language.get('language') == 'en'
    return not(is_chi or is_eng)


if __name__ == '__main__':
    text = '今日天氣好好 right'
    print(is_foreign_language(text))
    # print(google_translate(text))
