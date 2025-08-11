import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import time

client = genai.Client(api_key='AIzaSyCMqQyzogp1_ehQeDLLSINoPJkuiCc0yCo')


def generate_one_image(prompt):
    response = client.models.generate_images(
        # model='imagen-4.0-ultra-generate-preview-06-06',
        model='imagen-4.0-generate-preview-06-06',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio='1:1'
        )
    )
    return response

def generate_time_expression():
    # Successful: "Subject: A detailed digital clock. Display 11:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps."

    save_dir = 'assets/temperature_images'
    os.makedirs(save_dir, exist_ok=True)
    
    contents_dict = {
        '-10-celcius': "A digital thermometer, which displaying '-10°C, 14°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (-10°C, 14°F) clearly on the screen.",
        '-5-celcius': "A digital thermometer, which displaying '-5°C, 23°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (-5°C, 23°F) clearly on the screen.", 
        '0-celcius': "A digital thermometer, which displaying '0°C, 32°F' (only, without any other text). The thermal meter is plugged into a bowl of frozen food on the table. The food appears to be just at freezing point with visible ice crystals. Please show the display numbers (0°C, 32°F) clearly on the screen.",
        '10-celcius': "A digital thermometer, which displaying '10°C, 50°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (10°C, 50°F) clearly on the screen.",
        '20-celcius': "A digital thermometer, which displaying '20°C, 68°F' (only, without any other text). The thermal meter is plugged into a bowl of cold food on the table. Please show the display numbers (20°C, 68°F) clearly on the screen.",
        '30-celcius': "A digital thermometer, which displaying '30°C, 86°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (30°C, 86°F) clearly on the screen.",
        '40-celcius': "A digital thermometer, which displaying '40°C, 104°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (40°C, 104°F) clearly on the screen.",
        '50-celcius': "A digital thermometer, which displaying '50°C, 122°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (50°C, 122°F) clearly on the screen.",
        '60-celcius': "A digital thermometer, which displaying '60°C, 140°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (60°C, 140°F) clearly on the screen.",
        '70-celcius': "A digital thermometer, which displaying '70°C, 158°F' (only, without any other text). The thermal meter is plugged into a sizzling hot casserole dish fresh from the oven. Please show the display numbers (70°C, 158°F) clearly on the screen.",
        '80-celcius': "A digital thermometer, which displaying '80°C, 176°F' (only, without any other text). The thermal meter is plugged into a very hot roasted chicken just out of the oven, steam rising intensely. Please show the display numbers (80°C, 176°F) clearly on the screen.",
        '90-celcius': "A digital thermometer, which displaying '90°C, 194°F' (only, without any other text). The thermal meter is plugged into an extremely hot baked dish with bubbling cheese on top. Please show the display numbers (90°C, 194°F) clearly on the screen.",
        '100-celcius': "A digital thermometer, which displaying '100°C, 212°F' (only, without any other text). The thermal meter is plugged into food on the table. Please show the display numbers (100°C, 212°F) clearly on the screen.",
    }

    for time_expression, prompt in contents_dict.items():
        print(f"Generating image for {time_expression}")
        start_time = time.time()
        response = generate_one_image(prompt)
        for generated_image in response.generated_images:
            image = generated_image.image
            image.save(f'{save_dir}/{time_expression}.png')
            image.show()
        end_time = time.time()
        generation_time = end_time - start_time

        print(f"Image generation took {generation_time:.2f} seconds for {time_expression}")

        # Wait until 15 seconds have passed since last generation
        elapsed = time.time() - start_time
        if elapsed < 15:
            time.sleep(15 - elapsed)



if __name__ == "__main__":
    generate_time_expression()


# response = client.models.generate_content(
#     model="gemini-2.0-flash-preview-image-generation",
#     contents=contents,
#     config=types.GenerateContentConfig(
#       response_modalities=['TEXT', 'IMAGE']
#     )
# )

# end_time = time.time()
# generation_time = end_time - start_time
# print(f"Image generation took {generation_time:.2f} seconds")

# for part in response.candidates[0].content.parts:
#   if part.text is not None:
#     print(part.text)
#   elif part.inline_data is not None:
#     image = Image.open(BytesIO((part.inline_data.data)))
#     image.save('gemini-time-image.png')
#     image.show()

