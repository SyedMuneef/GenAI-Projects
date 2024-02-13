import os
import streamlit as st
import json
import time
import streamlit as st
import requests
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from openai.types.chat.chat_completion import ChatCompletion
import time


st.title("Finacial AI Chat")

_ : bool = load_dotenv(find_dotenv()) # read local .env file
FMP_API_KEY = os.environ["FMP_API_KEY"] 

client : OpenAI = OpenAI()

# Define financial statement functions
def get_income_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_balance_sheet(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_cash_flow_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_key_metrics(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_financial_ratios(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_financial_growth(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/financial-growth/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


# Map available functions
available_functions = {
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_cash_flow_statement": get_cash_flow_statement,
    "get_key_metrics": get_key_metrics,
    "get_financial_ratios": get_financial_ratios,
    "get_financial_growth": get_financial_growth,
}


# Define the main function

def run_assistant(user_msg: str):

  # Creating an assistant with specific instructions and tools

  assistant = client.beta.assistants.create(
      instructions="Act as a financial analyst by accessing detailed financial data through the Financial Modeling Prep API. Your capabilities include analyzing key metrics, comprehensive financial statements, vital financial ratios, and tracking financial growth trends. ",
      model="gpt-3.5-turbo-1106",
      #stream=True,

      
  tools=[
      {
  "type": "function",   
  "function": {
    "name": "get_income_statement",
    "description": "Get the income statement for a given stock from the Financial Modeling Prep API.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {"type": "string", "description": "Ticker symbol of the stock."},
        "period": {"type": "string", "description": "Time period for the data (e.g., 'annual' or 'quarter')."},
        "limit": {"type": "integer", "description": "Number of periods to retrieve."}
      },
      "required": ["ticker", "period", "limit"]
    }
  }
},

           {
  "type": "function",
  "function": {
    "name": "get_balance_sheet",
    "description": "Get the balance sheet statement for a given stock from the Financial Modeling Prep API.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {"type": "string", "description": "Ticker symbol of the stock."},
        "period": {"type": "string", "description": "Time period for the data (e.g., 'annual' or 'quarter')."},
        "limit": {"type": "integer", "description": "Number of periods to retrieve."}
      },
      "required": ["ticker", "period", "limit"]
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "get_cash_flow_statement",
    "description": "Get the cash flow statement for a specified stock from the Financial Modeling Prep API.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {"type": "string", "description": "Ticker symbol of the stock."},
        "period": {"type": "string", "description": "Time period for the data (e.g., 'annual' or 'quarter')."},
        "limit": {"type": "integer", "description": "Number of periods to retrieve."}
      },
      "required": ["ticker", "period", "limit"]
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "get_key_metrics",
    "description": "Get key metrics for a given stock from the Financial Modeling Prep API.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {"type": "string", "description": "Ticker symbol of the stock."},
        "period": {"type": "string", "description": "Time period for the data (e.g., 'annual' or 'quarter')."},
        "limit": {"type": "integer", "description": "Number of periods to retrieve."}
      },
      "required": ["ticker", "period", "limit"]
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "get_financial_ratios",
    "description": "Get financial ratios for a specified stock from the Financial Modeling Prep API.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {"type": "string", "description": "Ticker symbol of the stock."},
        "period": {"type": "string", "description": "Time period for the data (e.g., 'annual' or 'quarter')."},
        "limit": {"type": "integer", "description": "Number of periods to retrieve."}
      },
      "required": ["ticker", "period", "limit"]
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "get_financial_growth",
    "description": "Get financial growth data for a given stock from the Financial Modeling Prep API.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {"type": "string", "description": "Ticker symbol of the stock."},
        "period": {"type": "string", "description": "Time period for the data (e.g., 'annual' or 'quarter')."},
        "limit": {"type": "integer", "description": "Number of periods to retrieve."}
      },
      "required": ["ticker", "period", "limit"]
    }
  }
},

          ])
  
  # Creating a new thread
  thread = client.beta.threads.create()

  # Adding a user message to the thread
  client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=user_msg
  )

    # Running the assistant on the created thread
  run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

# Loop until the run completes or requires action
  while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Add run steps retrieval here
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
        #print("Retrieving Data")
        #print()
        st.write(f"Retrieving data And Analyzing Data. Pleas Wait")   
            
        
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    output = function_to_call(**function_args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output,
                    })

            # Submit tool outputs and update the run
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        elif run.status == "completed":
            # List the messages to get the response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            #stream=True
            for message in messages.data:
                role_label = "User" if message.role == "user" else "Assistant"
                message_content = message.content[0].text.value
                #print(f"{role_label}: {message_content}\n")
                st.write(f"{role_label}: {message_content}\n")   

            break  # Exit the loop after processing the completed run

        elif run.status == "failed":
            st.write("Run failed.")
            break

        elif run.status in ["in_progress", "queued"]:
            #st.write(f"Analyzing Data ")
            #print(f"Analyzing Data ")
            time.sleep(5)  # Wait for 5 seconds before checking again

        else:
            st.write(f"Unexpected status: {run.status}")
            break
        

prompt: str = st.chat_input("Enter Prompt Here")

if prompt != None:
 run_assistant(prompt)
elif prompt == None:
    st.write("Welcome!! How i can assist you today ?")
     
     
