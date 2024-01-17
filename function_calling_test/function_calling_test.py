import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key =os.environ['OPENAI_API_KEY']

testfunction = [
    {
        "name": "get_anime_information",
        "description": "与えられたアニメタイトルの情報を返します",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string", "description": "アニメのタイトル"
                },
            },
            "required": ["title"]
        }
    }
]



completion = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",#system[先頭、プロンプト(設定)] or user or assistant[会話の記憶など]
            "content": "日本の人口は何億人ですか？",
        },
    ],
)
print(completion.choices[0].message.content)