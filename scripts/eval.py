import openai
import os
import pandas as pd
import json
import argparse
import math
import base64

def get_answer(question, image_path):
    # Encode image to base64
    # with open(image_path, "rb") as image_file:
    #     image_data = image_file.read()
    #     original_size = len(image_data) / 1024  # Convert to KB
    #     # Check if image is larger than 1MB
    #     if len(image_data) > 1024 * 1024:
    #         from PIL import Image
    #         import io
    #         # Open image and reduce quality until size is under 1MB
    #         img = Image.open(io.BytesIO(image_data))
    #         quality = 95
    #         while True:
    #             buffer = io.BytesIO()
    #             img.save(buffer, format='JPEG', quality=quality)
    #             if len(buffer.getvalue()) <= 1024 * 1024:
    #                 image_data = buffer.getvalue()
    #                 break
    #             quality -= 5
    #             if quality < 5:
    #                 raise Exception("Could not reduce image size enough")
    #     encoded_image = base64.b64encode(image_data).decode('utf-8')
    # # Print image sizes and compression info
    # final_size = len(encoded_image) * 3/4 / 1024  # Base64 encoding adds ~33% overhead, so multiply by 3/4
    # compression_rate = (1 - final_size/original_size) * 100 if original_size != final_size else 0

    # print(f"Original size: {original_size:.1f}KB")
    # print(f"Final size: {final_size:.1f}KB") 
    # print(f"Compression rate: {compression_rate:.1f}%")

    with open(image_path, "rb") as image_file:
        # OK, now we don't need to compress the image. We will compress the image outside as a standalone function.
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    
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
        seed=42,
        temperature=1,
        logprobs=True,
        max_tokens=1,
        top_logprobs=20
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


def eval_concept(concept, dir_path, eval_type):

    results_dict = {}

    save_dir = f"results"
    os.makedirs(save_dir, exist_ok=True)

    save_fp = f"{save_dir}/{concept}_{eval_type}.json"


    df = pd.read_csv(f"{dir_path}/index.csv")

    for index, row in df.iterrows():
        if index > 3:
            continue
        if concept == "time_camera" or concept == "time_googlegen":
            question = (
                f"You are shown an image of a clock. Answer the question based on the image.\n"
                f"Question: What is the time in the image?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['possible_answer_1']}\n"
                f"B: {row['possible_answer_2']}\n"
                f"Answer:"
            )
            
            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a clock. Answer the question based on the image.\n"
                    f"Question: What is the time in the image?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['possible_answer_2']}\n"
                    f"B: {row['possible_answer_1']}\n"
                    f"Answer:"
                )
            

        if concept == "quantifiers_battery":
            question = (
                f"You are shown an image of a battery. Answer the question based on the image.\n"
                f"Question: How much battery is left in the image?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['most_likely_answer']}\n"
                f"B: {row['possible_answer_2']}\n"
                f"Answer:"
                )
        
            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a clock. Answer the question based on the image.\n"
                    f"Question: What is the time in the image?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['possible_answer_2']}\n"
                    f"B: {row['most_likely_answer']}\n"
                    f"Answer:"
                )

        if concept == "quantifiers_eggs":
            question = (
                f"You are shown an image of a box of eggs. Answer the question based on the image.\n"
                f"Question: How would you rate the level of eggs?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['most_likely_answer']}\n"
                f"B: {row['possible_answer_2']}\n"
                f"Answer:"
                )

            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a box of eggs. Answer the question based on the image.\n"
                    f"Question: How would you rate the level of eggs?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['possible_answer_2']}\n"
                    f"B: {row['most_likely_answer']}\n"
                    f"Answer:"
                )

        if concept == "temperature_camera" or concept == "temperature_googlegen":
            question = (
                f"You are shown an image of a thermometer. Answer the question based on the image.\n"
                f"Question: What is the temperature reading shown in the thermometer?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['answer_m']} {row['unit_m']}\n"
                f"B: {row['answer_i']} {row['unit_i']}\n"
                f"Answer:"
            )

            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a thermometer. Answer the question based on the image.\n"
                    f"Question: What is the temperature reading shown in the thermometer?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['answer_i']} {row['unit_i']}\n"
                    f"B: {row['answer_m']} {row['unit_m']}\n"
                    f"Answer:"
                )
        

        if concept == "distance":
            question = (
                f"You are shown an image of two {row['object']}s. Answer the question based on the image.\n"
                f"Question: How far is between the two {row['object']}s?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['answer_m']} {row['unit_m']}\n"
                f"B: {row['answer_i']} {row['unit_i']}\n"
                f"Answer:"
                )

            if eval_type == 'flip':
                question = (
                    f"You are shown an image of two {row['object']}s. Answer the question based on the image.\n"
                    f"Question: How far is between the two {row['object']}s?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['answer_i']} {row['unit_i']}\n"
                    f"B: {row['answer_m']} {row['unit_m']}\n"
                    f"Answer:"
                )
        
        if concept == "speed":
            question = (
                f"You are shown an image of a vehicle. Answer the question based on the image.\n"
                f"Question: What is the speed of the vehicle when it is moving normally?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['answer_m']} {row['unit_m']}\n"
                f"B: {row['answer_i']} {row['unit_i']}\n"
                f"Answer:"
                )

            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a vehicle. Answer the question based on the image.\n"
                    f"Question: What is the speed of the vehicle when it is moving normally?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['answer_i']} {row['unit_i']}\n"
                    f"B: {row['answer_m']} {row['unit_m']}\n"
                    f"Answer:"
                )
        
        if concept == "size":
            question = (
                f"You are shown an image of a room. Answer the question based on the image.\n"
                f"Question: What is the size of the room?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['answer_m']} {row['unit_m']}\n"
                f"B: {row['answer_i']} {row['unit_i']}\n"
                f"Answer:"
                )

            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a room. Answer the question based on the image.\n"
                    f"Question: What is the size of the room?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['answer_i']} {row['unit_i']}\n"
                    f"B: {row['answer_m']} {row['unit_m']}\n"
                    f"Answer:"
                )
        
        if concept == "price":
            question = (
                f"You are shown an image of a product. Answer the question based on the image.\n"
                f"Question: What is the price of the product?\n"
                f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                f"A: {row['answer_u']} {row['unit_u']}\n"
                f"B: {row['answer_r']} {row['unit_r']}\n"
                f"Answer:"
                )

            if eval_type == 'flip':
                question = (
                    f"You are shown an image of a product. Answer the question based on the image.\n"
                    f"Question: What is the price of the product?\n"
                    f"Choose only one option that best matches the image. Please answer with only A or B.\n"
                    f"A: {row['answer_r']} {row['unit_r']}\n"
                    f"B: {row['answer_u']} {row['unit_u']}\n"
                    f"Answer:"
                )

        file_name = row['file_name']
        print(f"file_name: {file_name}")
        print(f"question: {question}")
        answer, token_probs = get_answer(question, f"{dir_path}/{row['file_name']}")
        print(answer)
        print(token_probs)
        print("--------------------------------")

        results_dict[file_name] = {
            "question": question,
            "answer": answer,
            "token_probs": token_probs
        }

        with open(save_fp, "w") as f:
            # The idea is to save the results every time we get a new answer. 
            json.dump(results_dict, f, indent=4)
            print(f"Saved to {save_fp}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    concept_paths = {
        "time_googlegen": "assets/1_time/googlegen",
        "time_camera": "assets/1_time/camera",
        "quantifiers_battery": "assets/2_quantifiers/battery",
        "quantifiers_eggs": "assets/2_quantifiers/eggs", 
        "distance": "assets/4_2_distance",
        "speed": "assets/4_3_speed",
        "size": "assets/4_4_size",
        "temperature_camera": "assets/4_1_temperature/camera",
        "temperature_googlegen": "assets/4_1_temperature/googlegen",
        "price": "assets/4_5_price"
    }

    parser.add_argument("--concept", type=str, default="temperature_googlegen")

    parser.add_argument("--eval_type", type=str, default="flip")
    

    args = parser.parse_args()
    eval_concept(args.concept, concept_paths[args.concept], args.eval_type)
