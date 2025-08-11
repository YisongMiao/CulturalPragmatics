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

    save_dir = 'assets/time_images'
    os.makedirs(save_dir, exist_ok=True)
    
    contents_dict = {
        '12AM': "Subject: A detailed digital clock. Display 12:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '1AM': "Subject: A detailed digital clock. Display 1:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '2AM': "Subject: A detailed digital clock. Display 2:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '3AM': "Subject: A detailed digital clock. Display 3:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '4AM': "Subject: A detailed digital clock. Display 4:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '5AM': "Subject: A detailed digital clock. Display 5:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '6AM': "Subject: A detailed digital clock. Display 6:00 (only, without any other text). The clock is on a table. Environment: Dimly lit room with dawn light starting to filter in. Window View: Early morning street scene with the first rays of sunlight beginning to illuminate the sky.",
        '7AM': "Subject: A detailed digital clock. Display 7:00 (only, without any other text). The clock is on a table. Environment: Dimly lit room with dawn light starting to filter in. Window View: Early morning street scene with the first rays of sunlight beginning to illuminate the sky.",
        '8AM': "Subject: A detailed digital clock. Display 8:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '9AM': "Subject: A detailed digital clock. Display 9:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '10AM': "Subject: A detailed digital clock. Display 10:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '11AM': "Subject: A detailed digital clock. Display 11:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '12PM': "Subject: A detailed digital clock. Display 12:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '1PM': "Subject: A detailed digital clock. Display 1:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '2PM': "Subject: A detailed digital clock. Display 2:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '3PM': "Subject: A detailed digital clock. Display 3:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '4PM': "Subject: A detailed digital clock. Display 4:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '5PM': "Subject: A detailed digital clock. Display 5:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '6PM': "Subject: A detailed digital clock. Display 6:00 (only, without any other text). The clock is on a table. Environment: Bright sunlit room with abundant natural daylight. Window View: Vibrant morning street scene with full sunlight illuminating buildings and trees.",
        '7PM': "Subject: A detailed digital clock. Display 7:00 (only, without any other text). The clock is on a table. Environment: Room with dimming natural light as sunset approaches. Window View: Evening street scene with long shadows and golden hour lighting.",
        '8PM': "Subject: A detailed digital clock. Display 8:00 (only, without any other text). The clock is on a table. Environment: Room with minimal natural light and some artificial lighting. Window View: Dusk street scene with street lamps beginning to illuminate.",
        '9PM': "Subject: A detailed digital clock. Display 9:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only street lamps and occasional car lights visible.",
        '10PM': "Subject: A detailed digital clock. Display 10:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
        '11PM': "Subject: A detailed digital clock. Display 11:00 (only, without any other text). The clock is on a table. Environment: Dark room with very minimal lighting. Window View: Night street scene with only faint moonlight and distant street lamps.",
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

