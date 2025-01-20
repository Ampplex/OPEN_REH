import os
from openai import OpenAI
from methods import print_responses
from OpenAI_layer3 import final_analysis

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def filter_resp(prompt, user_param):
    # Simulated responses with token count and response time
    responses = print_responses(prompt)  # Ensure print_responses returns a list of tuples: (response_content, token_count, response_time)
    
    # Create a consolidated prompt for system
    instruction = f"""
    Out of the following three answers for the question: 
    {prompt} 
    choose the best answer and return only its index (0/1/2). 
    You must only return one single number as a response and nothing else.

    0: {responses[0][0]}
    1: {responses[1][0]}
    2: {responses[2][0]}
    """

    chat_completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "system", "content": instruction}],
        temperature=0.0,
        top_p=1,
        max_tokens=20,
    )

    # Parse the best index response
    best_index = chat_completion.choices[0].message.content.strip()
    print(f"Best index: {best_index}")

    # Find the agent with the minimum token count (cost-efficient)
    minimum_token = min([response[1] for response in responses])
    best_token = [i for i, response in enumerate(responses) if response[1] == minimum_token][0]

    # Find the agent with the minimum response time (fastest)
    min_time = min([response[2] for response in responses])
    best_time = [i for i, response in enumerate(responses) if response[2] == min_time][0]

    main_factors = [best_index, best_token, best_time]
    print(f"Main factors: {main_factors}")


    # output = final_analysis()
    # print(f"Final selected agent: {output}")
    Final_analysis = final_analysis(main_factors, user_param)
    print(f"Final selected agent: {Final_analysis}")