import datetime
import requests
from bs4 import BeautifulSoup

from utils.logger import get_logger

logger = get_logger()


def get_rate(rate='HKD-TWD'):
    logger.info(f"get exchange rate of {rate}")
    url = 'https://www.google.com/finance/quote/' + rate
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rate = soup.find_all("div", {"class": ["YMlKec fxKbKc"]})[0].text
    return rate


def get_exchange_rate_msg():
    logger.info("generating exchange rate message")
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jpy_rate = get_rate('JPY-HKD')
    twd_rate = get_rate('HKD-TWD')
    cad_rate = get_rate('CAD-HKD')
    msg = f" 今日匯率({current_datetime}): " \
          f"\n CAD:HKD:  {cad_rate}" \
          f"\n JPY:HKD:  {jpy_rate}" \
          f"\n HKD:TWD:  {twd_rate}"
    return msg


if __name__ == '__main__':
    print(get_exchange_rate_msg())
