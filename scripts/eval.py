import openai
import os
import pandas as pd
import json
import argparse
import math


def get_answer(question, image_path):
    # Encode image to base64
    import base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.0,
        logprobs=True,
        max_tokens=10,
        top_logprobs=2
    )
    
    answer = response.choices[0].message.content
    token_probs = response.choices[0].logprobs.content[0].top_logprobs

    token_probs = {
        prob.token: round(math.exp(prob.logprob), 4)
        for prob in response.choices[0].logprobs.content[0].top_logprobs
    }
    
    print(f"Answer: {answer}")
    print(f"Top logprobs: {token_probs}")
    
    return answer, token_probs


def eval_concept(concept, dir_path):
    df = pd.read_csv(f"{dir_path}/index.csv")

    for index, row in df.iterrows():
        # if index < 15 or index > 20:
        #     continue
        if concept == "time":
            question = f"What is the time in the image?\nA: {row['possible_answer_1']}\nB: {row['possible_answer_2']}\nPlease answer with only A or B."
        if concept == "price":
            question = f"What is the price of the item in the image?\nA: {row['answer_u']} {row['unit_u']}\nB: {row['answer_r']} {row['unit_r']}\nPlease answer with only A or B."
        if concept == "speed":
            question = f"What is the speed in the image?\nA: {row['answer_m']} {row['unit_m']}\nB: {row['answer_i']} {row['unit_i']}\nPlease answer with only A or B."

        file_name = row['file_name']
        print(f"file_name: {file_name}")
        print(f"question: {question}")
        answer, token_probs = get_answer(question, f"{dir_path}/{row['file_name']}")
        print(answer)
        print(token_probs)
        print("--------------------------------")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--concept", type=str, default="time")
    # parser.add_argument("--dir_path", type=str, default="assets/1_time/googlegen")

    parser.add_argument("--concept", type=str, default="price")
    parser.add_argument("--dir_path", type=str, default="assets/4_5_price")


    args = parser.parse_args()
    eval_concept(args.concept, args.dir_path)