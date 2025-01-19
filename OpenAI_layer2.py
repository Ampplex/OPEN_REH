import os
from openai import OpenAI
from methods import print_responses
import tiktoken  # Ensure you're using the correct tokenizer for your use case

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
        max_tokens=10,
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

    # Instruction for selecting the best agent based on user_param
    instruction = f"""
    There are three main aspects or factors for every AI agent: accuracy of response, token size of the output, and time taken to reply.
    We have selected different agents which perform the best for each aspect:
    - At index 0: Most accurate agent.
    - At index 1: Most cost-efficient agent (least token-consuming).
    - At index 2: Fastest agent (responds in minimum time).

    Main factors: {main_factors}

    Now, based on the following requirements, please select the best agent. Give higher priority to the requirements mentioned below:
    {user_param}

    If you select index 0, return "yahoo".
    If you select index 1, return "finhub".
    If you select index 2, return "wiki".
    
    You must return only a single word ("yahoo", "finhub", or "wiki").
    """

    # def final_analysis():
    #     # Perform the final analysis by checking the user_param
    #     chat_completion = client.chat.completions.create(
    #         model="nvidia/llama-3.1-nemotron-70b-instruct",
    #         messages=[{"role": "system", "content": instruction}],
    #         temperature=0.0,
    #         top_p=1,
    #         max_tokens=10,
    #     )
    #     output = chat_completion.choices[0].message.content.strip()
    #     return output

    # output = final_analysis()
    # print(f"Final selected agent: {output}")
    print(responses)
    return responses[int(best_index)][0]