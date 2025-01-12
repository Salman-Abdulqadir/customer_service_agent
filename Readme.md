# AI-Powered Email Processor for Fashion Store

## Objective

This project is a proof-of-concept application designed to intelligently process email order requests and customer inquiries for a fashion store. The application uses AI technologies to accurately classify emails into categories (e.g., "Product Inquiry" or "Order Request") and generate contextually appropriate responses based on product catalog information and current stock status.

---

## Features

1. **Email Classification**

   - Categorizes emails as "Product Inquiry" or "Order Request" based on the email content.

2. **Order Processing**

   - Verifies product availability in stock for order requests.
   - Creates order entries with statuses ("created" or "out of stock").
   - Updates stock levels dynamically.

3. **Inquiry Handling**

   - Generates detailed responses to customer inquiries using relevant product information from a large catalog.

4. **Response Generation**
   - Crafts professional, customer-friendly emails tailored to order and inquiry results.

---

## Inputs

The system processes data from a **CSV file** with the following sheets:

### 1. Products Sheet

Fields:

- Product ID
- Name
- Category
- Stock Amount
- Detailed Description
- Season

### 2. Emails Sheet

Fields:

- Email ID
- Subject
- Body

---

## Outputs

The system generates a single spreadsheet with the following sheets:

1. **Email Classification**

   - Columns: `email ID`, `category`

2. **Order Status**

   - Columns: `email ID`, `product ID`, `quantity`, `status` ("created" or "out of stock")

3. **Order Responses**

   - Columns: `email ID`, `response`

4. **Inquiry Responses**
   - Columns: `email ID`, `response`

## Libraries and Tools

- **OpenAI GPT-4**: For classification and response generation.
- **Python**: Core programming language.

## How to start

1. clone this repo
2. setup a virtual env for python - preferrably .venv
3. run make install
4. run make run
