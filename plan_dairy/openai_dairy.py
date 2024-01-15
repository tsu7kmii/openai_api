# ボタンをしたらスタートする。
# 会話スタートのボタンおす→スタートする→会話画面に移行する


#会話結果　ボタン押した後returnで来るものを表示すればよい、、続きからスタートボタンを実装するならバイナリから表示出来るべき

import json
from openai import OpenAI
from dotenv import load_dotenv
import os

userid = ""
i = 0
load_dotenv()
client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

def startbutton(user_id_name):
    global userid
    userid = str(user_id_name)
    with open("./plan_dairy/gpt_pro.txt", 'r',encoding='utf-8') as f:
        c_prompt = f.read()      
    messages = [{"role": "system", "content": c_prompt},
                {"role": "user", "content": "2/2 スタート"}
        ]
        
    completion = client.chat.completions.create(
        model="gpt-4",
        messages= messages,
        temperature=0.7,
        max_tokens=500
    )
    response = completion.choices[0].message.content
    save_chat(messages=messages, new_message={'role':'assistant', 'content':response},res = response)
    return response

def post(con_input):
    global userid
    if con_input =="command":#コマンドモードの実行、バイナリ内容表示とか
        pass
    if con_input =="end":#一つの会話を終わらせて別バイナリに保存
        pass
    with open("./plan_dairy/api_outputs/chat_history_"+str(userid)+".json", 'r+',encoding='utf-8') as f:
        messages = json.load(f)
    messages.append({"role": "user", "content": con_input})
    msg =sendapi(messages)
    return msg

def sendapi(messages):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    response = completion.choices[0].message.content
    # 応答を保存
    save_chat(messages=messages, new_message={'role':'assistant', 'content':response},res = response)
    return response

def save_chat(messages, new_message,res):
    global userid
    # 新しいメッセージを追加し、チャット履歴をファイルに保存
    messages.append(new_message)
    with open("./plan_dairy/api_outputs/chat_history_"+str(userid)+".json", "w+",encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False)
        
    if "+*+*end topic*+*+" in res:
        ress = res.replace("+*+*end topic*+*+","")
        # 終了したときの挙動
        with open("./plan_dairy/api_outputs/chat_last_"+str(userid)+".txt", "w+",encoding='utf-8') as f:
            f.writelines(str(ress))
        
def main():
    message = 0
if __name__ == "__main__":
    main()
    
# 仮実行
print(startbutton("gi22010"))
while True:
    msg = input("user:")
    if msg =="end":
        print("終了します")
        break
    print(post(msg))
