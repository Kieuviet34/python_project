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
    def name(self) -> Text:
        return "action_provide_product_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, any]) -> List[Dict[Text, any]]:
        try:
            # 1. Extract product name from user question (assuming Rasa NLU processing)
            product_name = tracker.get_slot("product_name")

            # 2. Search for product data in JSON file
            product_data = self.load_product_data()
            matched_product = None
            for data in product_data:
                if product_name == data.get("title"):
                    matched_product = data
                    break

            # 3. Check if product found
            if matched_product:
                title = matched_product.get("title", "Unknown")
                price = matched_product.get("price", "Unknown")
                description = matched_product.get("description", "No description available")

                # 4. Optionally filter or prioritize details
                relevant_details = {
                    # Select specific details based on user intent or preferences
                    "RAM": matched_product.get("product_details", {}).get("RAM"),
                    "Battery Power Rating": matched_product.get("product_details", {}).get("Batteries"),
                    "Screen size": matched_product.get("product_details",{}).get("Standing screen display size"),
                    "Memory capacity": matched_product.get("product_details",{}).get("Memory Storage Capacity"),
                    "OS" : matched_product.get("product_details",{}).get("OS")
                }

                response = f'Đây là thông tin của sản phẩm {title}:\n'
                response += f'Giá: {price}\n'
                response += f'Mô tả: {description}\n'
                if relevant_details:
                    response += 'Thông tin chi tiết:\n'
                    for k, v in relevant_details.items():
                        response += f'- {k}: {v}\n'

                dispatcher.utter_message(response)
            else:
                dispatcher.utter_message("Xin lỗi, tôi không tìm thấy thông tin về sản phẩm '{}'".format(product_name))

            return []

        except FileNotFoundError:
            dispatcher.utter_message("Xin lỗi tôi không thể tìm thông tin sản phẩm, vui lòng thử lại sau")
        except json.JSONDecodeError:
            dispatcher.utter_message("Đã xảy ra lỗi trong khâu xử lý thông tin sản phẩm, vui lòng liên hệ hỗ trợ")
    def load_product_data(self)->Dict[Text,any]:
        with open('\\data_scaping\\phone.json', 'r') as f:
            product_data = json.load(f)
        
        return product_data