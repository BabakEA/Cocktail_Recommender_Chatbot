from cgitb import reset
from datetime import date
from inspect import CO_ASYNC_GENERATOR
#from dis import dis
from re import S
import getpass
from typing import Any, Text, Dict, List,Union
import sqlite3
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info(str(date.today()))

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted,FollowupAction
from rasa_sdk.forms import FormValidationAction
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import os,re,json,requests
from difflib import *
import pprint
import warnings
import matplotlib
from matplotlib import pyplot as plt
from random import sample

warnings.filterwarnings("ignore")

print("*************************")
class ActionAskReset(Action):# action reset
    def name(self) -> Text:
        return "action_reset"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"""a new story is starting now ,
                                    please start with a greeting message"""
                                ) 
        logger.info("user called reset action")
        return [Restarted()]
