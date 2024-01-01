FROM python:3.8
COPY . .
RUN pip install requests beautifulsoup4 python-dotenv imageio apscheduler python-telegram-bot google-cloud-translate==2.0.1 spacy_langdetect spacy
RUN python -m spacy download zh_core_web_lg
CMD ["python","./main.py"]
