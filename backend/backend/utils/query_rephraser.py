from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

def query_rephraser_fn(query:str)->str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=api_key)
    
    prompt = f"""
You are a helpful assistant that rephrases shorthand or fragmented user queries into clear, complete English questions to check **whether a specific medical case is covered under an insurance policy**.
The original input may include age, gender, medical condition, location, and policy duration in a shorthand format.
Your job is to **preserve all key details** and rewrite the query as a **natural language yes/no question** that helps determine if the scenario is covered by the insurance policy.
Only return the final rephrased question.

### Examples:

Input: "46M, knee surgery, Pune, 3-month policy"
Output: "Is a 46-year-old male who had knee surgery in Pune covered under a 3-month-old insurance policy?"

Input: "30F, pregnancy, Delhi, new policy"
Output: "Is a 30-year-old pregnant female in Delhi covered under a newly issued insurance policy?"

Input: "65M, bypass surgery, Mumbai, 1-year policy"
Output: "Is a 65-year-old male who underwent bypass surgery in Mumbai covered under a 1-year-old insurance policy?"

Now rephrase this input:
{query}
"""
    rephrased_query = llm.invoke(prompt)
    return rephrased_query