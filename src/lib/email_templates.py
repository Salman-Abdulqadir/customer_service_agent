from config import company_info

def get_product_numbered_list(product_list):
    result = ""
    for index in range(len(product_list)):
        product = product_list[index]
        result += f"{index + 1}. {product['product_id']} X {product['quantity']}\n"
    return result

def fully_processed_order_email(products_details):
    return f"""
Dear customer,

Thank you for your order! We’re excited to inform you that your order has been successfully processed and is on its way. Below are the details of your purchase:

In-Stock products:

{get_product_numbered_list(products_details)}

You can expect your delivery to arrive within the estimated time. If you have any questions or need assistance, feel free to reply to this email.

Thank you for choosing us. We look forward to serving you again soon!

Warm regards,
{company_info["name"]}
{company_info["contact"]}
"""

def partially_processed_order_email(instock_products, out_of_stock_product):
    return f"""
Dear [Customer's Name],

Thank you for placing an order with us! We regret to inform you that we were unable to fully process your order due to the following item(s) being out of stock:

Out-of-Stock Items:

{get_product_numbered_list(out_of_stock_product)}

Order Details:

{get_product_numbered_list(instock_products)}

We apologize for the inconvenience this may have caused. You have the following options:

Wait for Restock: We can notify you as soon as the item(s) become available.
Alternative Products: [Provide a list of alternative product suggestions here.]
Partial Fulfillment: We can process the available items and cancel the rest of your order.
Please let us know how you would like to proceed. If we don’t hear back from you within [timeframe], we will process the available items and issue a refund for the out-of-stock items.

Thank you for your understanding and patience. If you have any further questions or concerns, don’t hesitate to reach out.

Warm regards,
{company_info["name"]}
{company_info["contact"]}
"""

def product_inquiry_tempate(email_body):
    return f"""
{email_body} 

Warm regards,
{company_info["name"]}
{company_info["contact"]}
"""