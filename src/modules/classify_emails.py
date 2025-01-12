from concurrent.futures import ThreadPoolExecutor, as_completed
from lib.helpers import ask_openai, get_emails_df
from config import output_folder_path

def classify_email(email):
    try:
        valid_categories = ', '.join(["product inquiry", "order request"])
        
        subject = email["subject"]
        message = email["message"]
        email_id = email["email_id"]

        system_prompt = { 
            "role": 'system', 
            "content": f"""
You are a highly accurate email classifier. You will be provided with the subject and message of an email. Your task is to categorize the email into one of the following three categories: {valid_categories}.

- Classify the email as "order request" only if the user is explicitly indicating an intention to place an order, such as specifying product details (e.g., product ID or name), quantity, or a request to finalize a purchase.
- Classify the email as "product inquiry" if the user is asking for more details or clarification before committing to an order. This can include vague references to products (id or name not included), requests for availability, or general questions without a direct intent to purchase.
- If product id and name are not explicitly mentioned classify as product inquiry e.g "the product with the geometric patterns and is viral on Instagram" -> product inquiry

Output only the category name with no additional explanations or details.
"""
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
    output_path = f"{output_folder_path}/email-classification.csv"
    emails_df[["email_id", "category"]].to_csv(output_path, index=False)