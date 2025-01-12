import os
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(key):
    try:
        value = os.getenv(key=key)
        return value or ""
    except Exception as e:
        print(f"Error while loading env var {key}, Error: {e}", "ERROR")
        return ""


openai_config = {
    "base_url": get_env_var("OPEN_AI_BASE_URL"),
    "openai_key": get_env_var("OPEN_AI_KEY"),
    "openai_model":  get_env_var("OPEN_AI_MODEL")
}

current_work_directory = os.getcwd()

output_folder_path = os.path.join(current_work_directory, get_env_var("OUTPUT_FOLDER_PATH"))
input_folder_path = os.path.join(current_work_directory, get_env_var("INPUT_FOLDER_PATH"))

company_info = {
    "name": get_env_var("EMAIL_PROCESSING_CORP_NAME"),
    "contact": get_env_var("EMAIL_PROCESSING_CORP_CONTACT")
}

output_file_paths = {
    "email_classification": f"{output_folder_path}/email-classification.csv",
    "order_status": f"{output_folder_path}/order-status.csv",
    "order_response": f"{output_folder_path}/order-response.csv",
    "inquiry_response": f"{output_folder_path}/inquiry-response.csv",
}

input_file_paths = {
    "emails": f"{input_folder_path}/emails.csv",
    "products": f"{input_folder_path}/products.csv",
}