# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
class ActionProvideProductDetails(Action):
    def name(self)->Text:
        return "action_provide_product_details"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, any])-> List[Dict[Text, any]]:
        try:
            product_data = self.load_product_data()
            #get information about product
            title = product_data.get('title', "Unknown")
            price = product_data.get('price', "Unknown")
            description = product_data.get('description', 'No description available')
            detail = product_data.get('detail', {})
            
            respone = f'Here are the details of product:\nTitle: {title}\nPrice:  {price}\nDescription: {description}\nProduct Details:'
            for k,v in detail.item():
                respone += f'\n -{k}: {v}'
            dispatcher.utter_message(respone)
            
            return []
        except FileNotFoundError:
            dispatcher.utter_message("Sorry, I cant find any product information, please try again later")
        except json.JSONDecodeError:
            dispatcher.utter_message("There was an issue processing product information. Please contact support")
    def load_product_data(self)->Dict[Text,any]:
        with open('\\data_scaping\\phone.json', 'r') as f:
            product_data = json.load(f)
        
        return product_data