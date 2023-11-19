FROM python:3.8
COPY . .
RUN pip install requests beautifulsoup4 python-dotenv imageio apscheduler python-telegram-bot
CMD ["python","./main.py"]
