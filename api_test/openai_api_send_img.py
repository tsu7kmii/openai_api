# -*- coding: utf-8 -*-

# https://cdn.discordapp.com/attachments/1041539813821653022/1176023457763430480/image.png

import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key =os.environ['OPENAI_API_KEY']



completion = openai.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "この画像にはりんごが映っていますか？写っていた場合「apple」とだけ返してください"},
                {
                    "type": "image_url",
                    "image_url": "https://cdn.discordapp.com/attachments/1041539813821653022/1176023457763430480/image.png",
                },
            ],
        },
    ],
)
print(completion.choices[0].message.content)
