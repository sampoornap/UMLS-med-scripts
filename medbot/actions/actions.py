import csv
import os
import random
from openai import OpenAI
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import logging


key = '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'
client = OpenAI(api_key = key)

logging.basicConfig(
    filename='/Users/sampoornaporia/medbot/actions/actions.log',  
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
class ActionProvideMedicationNames(Action):

    def name(self) -> Text:
        return "action_provide_medication_names"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        medical_condition = tracker.get_slot('medical_condition')
        logger.info(f"Medical condition received: {medical_condition}")
        # dispatcher.utter_message(text=f"Here are some medications for {medical_condition}")
                                 
        if not medical_condition:
            dispatcher.utter_message(text="Please provide the medical condition you are inquiring about.")
            return []

        medications = self.get_medications_by_condition(medical_condition)
        
        if medications:
            top_medications = random.sample(medications, min(5, len(medications)))  
            resp = self.generate_response(f"Here are some medications for {medical_condition}: {', '.join(top_medications)}.")
            dispatcher.utter_message(text = resp)
            # dispatcher.utter_message(text=f"Here are some medications for {medical_condition}: {', '.join(top_medications)}.")
        else:
             
            dispatcher.utter_message(text=f"Sorry, I couldn't find any medication info for {medical_condition}.")
        
        return []

    def get_medications_by_condition(self, condition):
        medications = []
        csv_file_path = '/Users/sampoornaporia/medbot/data.csv'
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['medical_condition'].strip().lower() == condition.strip().lower():
                    medications.append(row['medicine_name'])
        return medications
    
    def generate_response(self, prompt: Text) -> Text:
        
        
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt, 
            max_tokens = 100
            
        )
        return response.choices[0].text.strip()


class ActionProvideSideEffects(Action):

    def name(self) -> Text:
        return "action_provide_side_effects"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        medicine_name = tracker.get_slot('medicine_name')
        logger.info(f"Medicine name received: {medicine_name}")

        # dispatcher.utter_message(text=f"here are the side effects of {medicine_name}")
        if not medicine_name:
            dispatcher.utter_message(text="Please provide the name of the medication you are inquiring about.")
            return []

        side_effects = self.get_side_effects_by_medicine(medicine_name)
        if side_effects:

            resp = self.generate_response(f"The side effects of {medicine_name} include: {side_effects}.")
            # dispatcher.utter_message(text=f"The side effects of {medicine_name} include: {side_effects}.")
            dispatcher.utter_message(text = resp)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any side effects info for {medicine_name}.")
        
        return []

    def get_side_effects_by_medicine(self, medicine_name):
        side_effects = None
        csv_file_path = '/Users/sampoornaporia/medbot/data.csv'
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['medicine_name'].strip().lower() == medicine_name.strip().lower():
                    side_effects = row['side_effects']
                    break
        return side_effects 
    

    def generate_response(self, prompt: Text) -> Text:
        
        
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt, 
            max_tokens = 100
           
        )
        return response.choices[0].text.strip()


