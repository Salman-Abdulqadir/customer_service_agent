import pandas as pd
import os
from openai import OpenAI
from config import *
from datetime import datetime
import json

client = OpenAI(
    base_url=openai_config["base_url"],
    api_key=openai_config["openai_key"]
)

def ask_openai(messages, log_message = ""):

    try:
        logger(f'Asking openAI message: {log_message}')
        prompt =  client.chat.completions.create(
            model=openai_config["openai_model"],
            messages=messages
        )
        return prompt.choices[0].message.content
    except Exception as e:
        logger(f"Something went wrong while Asking openAI error: {e}", "ERROR")

def read_data(filename):
    return pd.read_csv(filename)

def save_data(df, filename):
    return df.to_csv(filename, index=False)

def get_products_df():
    return read_data(input_file_paths["products"])

def get_emails_df():
    return read_data(input_file_paths["emails"])

def parse_json(input, fallback = {}):
    try:
        data = json.loads(input)
        return data
    except Exception as e:
        logger(f"Something went wrong while parsing json, input: {input}, Error: {e}")
        return fallback
    
def logger(message, type='INFO'):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{type}] {current_time} - {message}")
