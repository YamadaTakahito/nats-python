import os

from dotenv import load_dotenv
load_dotenv()

SUB = os.environ['SUBJECT']
NATS_URL = os.environ['NATS_URL']
