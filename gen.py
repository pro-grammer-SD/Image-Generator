from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from sys import argv
from os import mkdir, chdir, path

client = genai.Client(api_key="AIzaSyBMzCMv9Z8XoVc7ei1gInsr2xDfnG7rRV8")

contents = argv[1]

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

if response and response.candidates:
    content = response.candidates[0].content
    if content and hasattr(content, 'parts'):
        for part in content.parts:
            if getattr(part, 'text', None):
                print(part.text)
            elif getattr(part, 'inline_data', None):
                image = Image.open(BytesIO(part.inline_data.data))
                if not path.exists("images"):
                    mkdir("images")
                chdir("images")
                image.save(f'{contents}.png')
                image.show()
    else:
        print("No parts in content.")
else:
    print("No candidates returned.")
