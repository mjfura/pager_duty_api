import pagerduty
from flask import Flask
from .env import API_KEY


client = pagerduty.RestApiV2Client(API_KEY)
app = Flask(__name__)
