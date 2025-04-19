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

for part in response.candidates[0].content.parts:
    if hasattr(part, "text") and part.text:
        print(part.text)
    elif hasattr(part, "inline_data") and part.inline_data:
        image = Image.open(BytesIO(part.inline_data.data))
        if not path.exists("images"):
            mkdir("images")
        chdir("images")
        image.save("image.png")
        image.show()
        break
