from config import company_info

def get_product_numbered_list(product_list, include_remaining=False ):
    result = ""
    for index in range(len(product_list)):
        product = product_list[index]
        result += f"{index + 1}. [{product['product_id']}]  {product['name']} (X{product['quantity']})"
        if (include_remaining):
            stock = product['stock']
            result += f" - {'Out of stock' if stock == 0 else f'Only {stock} left in stock!'}\n"
        else:
            result += '\n'
    return result

def fully_processed_order_email(products_details):
    return f"""
Dear customer,

Thank you for your order! We’re excited to let you know that your order has been successfully processed and is on its way.

In-Stock products:
  {get_product_numbered_list(products_details)}

You can expect your delivery to arrive within 3–5 business days.

If you have any questions or need assistance, feel free to reply to this email or visit our Customer Support Center.

Thank you for choosing {company_info["name"]}. We look forward to serving you again soon!

Warm regards,
{company_info["name"]}
{company_info["contact"]}
"""

def partially_processed_order_email(instock_products, out_of_stock_product):
    return f"""
Dear Customer,

Thank you for placing an order with us! We regret to inform you that we were unable to fully process your order due to the following item(s) being out of stock:

Order Details:
  {get_product_numbered_list(instock_products)}

Out-of-Stock Items:
  {get_product_numbered_list(out_of_stock_product, True)}

We apologize for the inconvenience this may have caused. You have the following options:
  1.Wait for Restock: We will notify you as soon as the item(s) become available.
  2.Partial Fulfillment: We will process the available items and cancel the out-of-stock items.

Next Steps:
  Please reply to this email with your preferred option within 7 days. If we don’t hear back, we will proceed with Option 2 and issue a refund for the out-of-stock items.

Thank you for your understanding and patience. If you have any further questions or concerns, please feel free to contact us at {company_info["contact"]}.

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