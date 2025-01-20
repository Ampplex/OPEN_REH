import os
from openai import OpenAI
from methods import print_responses

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)
def final_analysis(main_factors, user_param: str):
    # Instruction for selecting the best agent based on user_param
    instruction = f"""
    Firstly give the response to the prompt with respect to parameters
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
    
    You must return a single word ("yahoo", "finhub", or "wiki").
    With a response to the prompt given by the user
    """

    print("MAIN_FACTORS: ", main_factors)
    print("user_param", user_param)

    # Perform the final analysis by checking the user_param
    chat_completion2 = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "system", "content": instruction}],
        temperature=0.0,
        top_p=1,
        max_tokens=300,
    )
    output = chat_completion2.choices[0].message.content.strip()
    output = [c for c in output if c != '*']
    return ''.join(output)
