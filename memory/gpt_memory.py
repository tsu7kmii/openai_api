# import openai
import pickle
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

def main(messages):
    # OpenAIのAPIを呼び出し、与えられたメッセージに対する応答を取得
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )
    response = completion.choices[0].message.content
    # 応答を保存
    save_chat(messages=messages, new_message={'role':'assistant', 'content':response})
    return response

def save_chat(messages, new_message):
    # 新しいメッセージを追加し、チャット履歴をファイルに保存
    messages.append(new_message)
    with open("./memory/chatgpt_outputs/chat_history.pickle", "wb") as f:#バイナリなのでpickleでもtxtでも同じ
        pickle.dump(messages, f)

# ユーザーに以前の会話履歴を使用するかどうかを尋ねる
answer = input("これまでの会話履歴を引き継ぎますか？ (y/n)")
if not answer.lower() == "y" and not answer.lower() == "n":
    print("Invalid input. Please enter either 'y' or 'n'.")
    exit()

# ユーザーからのプロンプトを取得
prompt = input("会話や質問を入力してください\nuser: ")

if answer.lower() == "y":
    # 会話履歴を読み込み、ユーザーのプロンプトを追加
    with open("./chatgpt_outputs/chat_history.pickle", 'rb') as f:
        messages = pickle.load(f)
    messages.append({"role": "user", "content": prompt})
elif answer.lower() == "n":
    # 新しい会話を開始
    messages = [{"role": "system", "content": "あなたは優秀なAIアシスタントです。"},
                {"role": "user", "content": prompt}
    ]

# メイン関数を呼び出し、AIの応答を取得
response = main(messages)
print("AI:", response)
