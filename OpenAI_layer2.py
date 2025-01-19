import os
from openai import OpenAI
from methods import print_responses
import tiktoken

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)
encoding = tiktoken.encoding_for_model("gpt-4")

# Simulated responses
responses = print_responses()

# Create a consolidated prompt
prompt = f"""
Out of the following three answers for the question: 
What is the company information for Apple Inc. (AAPL)? 
choose the best answer and return only its index (0/1/2). 
You must only return one single number as a response and nothing else.

0: {responses[0][0]}
1: {responses[2][0]}
2: {responses[1][0]}
"""

chat_completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[
        {"role": "system", "content": prompt},
    ],
    temperature=0.0,
    top_p=1,
    max_tokens=10,
)

# Parse the response
best_index = chat_completion.choices[0].message.content.strip()
print(best_index)