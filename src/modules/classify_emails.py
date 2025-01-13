from concurrent.futures import ThreadPoolExecutor, as_completed
from lib.helpers import ask_openai, get_emails_df, save_data
from lib.const import CLASSIFY_EMAIL_PROMPT
from config import output_file_paths

def classify_email(email):
    try:
        valid_categories = ', '.join(["product inquiry", "order request"])
        
        subject = email["subject"]
        message = email["message"]
        email_id = email["email_id"]

        system_prompt = { 
            "role": 'system', 
            "content": CLASSIFY_EMAIL_PROMPT.format(valid_categories=valid_categories)
        }
        user_prompt = {
            "role": "user",
            "content": f"""
                Subject: {subject}
                Message: {message}
            """
        }
        return ask_openai([system_prompt, user_prompt], f"classifying email with id {email_id}")
    except Exception as e:
        print("Error happened while classifying email", e)
        return "error"


def classify_emails():
    emails_df = get_emails_df()
    results = []
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(classify_email, email): email for _, email in emails_df.iterrows()}
        for future in as_completed(futures):
            email = futures[future]
            try:
                result = future.result()
                results.append((email["email_id"], result))
            except Exception as e:
                print(f"Error for email {email['email_id']}: {e}")
                results.append((email["email_id"], "error"))
    
    # Assign categories to the DataFrame
    results_dict = dict(results)
    emails_df["category"] = emails_df["email_id"].map(results_dict)

    # Saving output to a file
    save_data(emails_df[["email_id", "category"]], output_file_paths["email_classification"])