import pandas as pd
from config import input_file_paths, output_file_paths
from lib.helpers import get_emails_df, logger, ask_openai, parse_json, get_products_df, save_data, read_data
from lib.embedding_helper import search_embeded_product
from lib.email_templates import fully_processed_order_email, partially_processed_order_email

def get_order_status(email_id, order, target_product):
    order["email_id"] = email_id
    if target_product["stock"] < order["quantity"]:
        order["status"] = "out of stock"
        return order
    order["status"] = "created"
    return order

def process_email(email):
    email_id = email.email_id
    full_email = f"subject:{email.subject} message: {email.message}"
    # get similarity chech from product catalog
    product_context = search_embeded_product(full_email, 3, include_desc=True).to_dict(orient='records')
    # call an LLM to extract the quantity from the order
    system_prompt = {
        "role": 'system',
        "content": f"""
You are an assistant designed to extract structured data from emails.
Your task is to identify product orders from the email content and return `product_id` and `quantity` as a JSON array of objects.
- If `product_id` is not explicitly mentioned, infer it from the product name, category, or description in the email content by matching it with the available products.
- If the quantity is not explicitly mentioned, infer it from phrases like "all," "half," or "quarter," converting them to numeric values (e.g., "all" equals full stock). Use available stock to calculate the quantity when necessary.
- Make sure to put the quantity regardless of the stock available if explicitly mentioned in the email.
- If no valid product order is found, return an empty array (`[]`).

The available products are as follows:
{product_context}

The response must be A VALID JSON object (double quotes for keys and values (when applicable)) with no additional details.
        """
    }
    user_prompt = {
        "role": 'user',
        "content": full_email
    }
    reponse = ask_openai([system_prompt, user_prompt], f"Process order email {email_id}")
    product_orders = parse_json(input=reponse, fallback=[])  
    products_df = get_products_df()
    order_status_list = []
    for order in product_orders:
        target_product = products_df.loc[products_df["product_id"] == order["product_id"]].iloc[0]
        if target_product.empty:
            continue
        order_status = get_order_status(email_id=email_id, order=order, target_product=target_product)

        # updating the datafram of products_df
        if order_status["status"] == 'created':
            products_df.loc[products_df['product_id'] == target_product['product_id'], 'stock'] = target_product['stock'] - order_status["quantity"]
            logger("Saving Products CSV...")
            save_data(products_df, input_file_paths["products"])

        order_status_list.append(order_status)


    return order_status_list

def generate_email_responses(order_status_df):
    products_df = get_products_df()
    order_status_df = order_status_df.merge(products_df, on="product_id", how="left")
    grouped = order_status_df.groupby('email_id')
    responses = []
    for email, products in grouped:
        is_fully_proccessed = products['status'].apply(lambda x: (x == "created")).all()
        if is_fully_proccessed:
            logger(f"Generating fully proccessed email response for Email ID: {email}", 'DEBUG')
            email_response = fully_processed_order_email(products.to_dict(orient='records') or [])
        else:
            logger(f"Generating partially processed email response for Email ID: {email}", 'DEBUG')

            # Filter the DataFrame for the 'created' status
            instock_products = products[products['status'] == 'created'].to_dict(orient='records')

            # Filter the DataFrame for the 'out of stock' status
            out_of_stock_products = products[products['status'] == 'out of stock'].to_dict(orient='records')
            email_response = partially_processed_order_email(
                instock_products=instock_products or [], 
                out_of_stock_product=out_of_stock_products or []
            )

        responses.append({
            "email_id": email,
            "response": email_response
        })
    return responses

def process_order_requests():
    print("output_file", output_file_paths)
    email_classification_df = read_data(output_file_paths["email_classification"])
    emails_df = get_emails_df()
    # filtering order requests from email_classification csv
    order_request_ids = email_classification_df[email_classification_df['category'] == 'order request']["email_id"]

    # using the filtered email ids getting the corresponding email details
    order_emails_df = emails_df[emails_df['email_id'].isin(order_request_ids)]

    order_status_list = []
    # for email in order_emails_df.itertuples():
    #     logger(f"Processing order Email - {email.email_id} in progress...")
    #     order_status = process_email(email=email)
    #     order_status_list.extend(order_status)
    #     logger(f"Processing order Email - {email.email_id} completed, order status: {order_status}")
    order_status_list = [
        {"product_id": "LTH0976", "quantity": "4", "email_id": "E001", "status": "created"},
        {"product_id": "VBT2345", "quantity": "1", "email_id": "E002", "status": "created"},
        {"product_id": "SFT1098", "quantity": "3", "email_id": "E004", "status": "created"},
        {"product_id": "CLF2109", "quantity": "5", "email_id": "E007", "status": "out of stock"},
        {"product_id": "FZZ1098", "quantity": "2", "email_id": "E007", "status": "created"},
        {"product_id": "VSC6789", "quantity": "1", "email_id": "E008", "status": "created"},
        {"product_id": "RSG8901", "quantity": "1", "email_id": "E010", "status": "created"},
        {"product_id": "SLD7654", "quantity": "1", "email_id": "E013", "status": "created"},
        {"product_id": "SWL2345", "quantity": "1", "email_id": "E014", "status": "created"},
        {"product_id": "CBT8901", "quantity": "2", "email_id": "E019", "status": "created"},
        {"product_id": "CGN2345", "quantity": "5", "email_id": "E023", "status": "out of stock"}
    ]
    if len(order_status_list) > 0:
        order_status_df = pd.DataFrame(order_status_list)
        email_responses_df = pd.DataFrame(generate_email_responses(order_status_df) or [])

        # # saving order status and order responses
        save_data(order_status_df, output_file_paths["order_status"])
        save_data(email_responses_df, output_file_paths["order_response"])