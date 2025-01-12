import pandas as pd
from config import output_file_path
from lib.helpers import logger, get_emails_df, ask_openai
from lib.email_templates import product_inquiry_tempate
from lib.embedding_helper import search_embeded_product

def inquiry_response(inquiry, emails_df):
    try:
        logger(f"Handling product inquiry, Email ID - {inquiry.email_id}")
        email_details = emails_df.loc[inquiry.email_id]
        full_email = f'ID: {inquiry.email_id} Subject: {email_details["subject"]} Message: {email_details["message"]}'
        product_catalog_context = search_embeded_product(query=full_email, top_k=5, include_desc=True).to_dict(orient="records")

        system_prompt = {
            "role": "system",
            "content": f"""
You are a professional email responder, tasked with answering user inquiries about products based on the provided product catalog.

- Craft a concise, friendly, and professional response that not only answers the inquiry but also encourages the customer to make a purchase.
- the response should be in the same language the email is written
- Provide informative details from the product catalog and highlight the benefits or features to spark interest.
- Only output the body of the email—do not include sign-offs.
- if the customer name is not mentioned address them as Dear Customer,
- The response should be a plain string with no extra details or commentary.

Product Catalog Context:
{product_catalog_context}
"""
        }
        user_prompt = {
            "role": "user",
            "content": full_email
        }
        email_body = ask_openai([system_prompt, user_prompt], f"Product Inquiry for email - {inquiry.email_id}")
        if (type(email_body) is str):
            return {
                "email_id": inquiry.email_id,
                "response": product_inquiry_tempate(email_body=email_body)
            }
    except Exception as e:
        logger(f"Something went wrong while handling an Inquiry - Email ID : {inquiry.email_id}, Error: {e}", 'ERROR')

def handle_product_inquiry():
    # get the product inquiry requests
    emails_df = get_emails_df()
    emails_df.set_index('email_id', inplace=True)
    email_classification_df = pd.read_csv(f"{output_file_path}/email-classification.csv")
    product_inquiries = email_classification_df[email_classification_df["category"] == "product inquiry"]
    inquiry_responses = []
    for inquiry in product_inquiries.itertuples():
        response = inquiry_response(inquiry=inquiry, emails_df=emails_df)
        inquiry_responses.append(response)
    pd.DataFrame(inquiry_responses).to_csv(f"{output_file_path}/inquiry-response.csv", index=False)
