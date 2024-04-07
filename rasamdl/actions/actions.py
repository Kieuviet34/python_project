# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import EventType
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import json,re

class ValidateProductForm(FormValidationAction):
    def __init__(self):
        self.PRODUCT_NAME = None
        self.PRODUCT_PRICE = None
        self.PRODUCT_DETAILS = {}
    def get_product_info(self):
        with open("\\data_scaping\\phone.json","r+") as f:
            data = json.load(f)
        title = data.get('title','')
        product_name = title.split(',')[0].split('|')[0].split('/')[0].split('\\')[0].strip() #reshape name
        self.PRODUCT_NAME = product_name
        self.PRODUCT_PRICE = data.get('price', None)
        
        self.PRODUCT_DETAILS = data.get("product_details",{})
        
    def name(self) ->Text:
        return "validate_product_form"
    
    def validate_product_name(
        self, 
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if self.PRODUCT_NAME and slot_value.lower() not in self.PRODUCT_NAME.lower():
            dispatcher.utter_message(text=f"tên sản phẩm không hợp lệ, sản phẩm của chúng tôi chỉ có {'/'.join(self.PRODUCT_NAME)}")
            return {"product_name": None} 
        if not slot_value:
            dispatcher.utter_message(
                text=f"Tôi không nhận ra tên sản phẩm, Data của chúng tôi chỉ có {'/'.join(self.PRODUCT_NAME)}"
            )
            return {"product_name": None}
        dispatcher.utter_message(text=f"OK! bạn muốn sản phẩm {slot_value}.")
        return {"product_name": slot_value}
    def validate_product_info(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message('Thông tin chi tiết không hợp lệ')
            return {'product_details':None}
        if slot_value not in self.PRODUCT_DETAILS:
            dispatcher.utter_message(text=f"Không tìm thấy thông tin chi tiết này.")
            return {"product_detail": None}
        dispatcher.utter_message(text=f"OK! Thông tin chi tiết bạn muốn là: {self.PRODUCT_DETAILS[slot_value]}.")
        return {"product_detail": slot_value}     