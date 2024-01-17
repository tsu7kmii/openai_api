import openai
import requests
import json
import math
 
 
OPEN_WEATHER_API_KEY = "YOUR_OPEN_WEATHER_API_KEY"
openai.api_key = "YOUR_OPENAI_API_KEY"
 
 
# OpenWeather で指定の都市の天気を取得する  >  天気apiを使用した行動を関数化している
# これをgoogle carendar api or AOuthに書き換える

def get_current_weather(city_name="Tokyo"):
    # 都市の緯度、経度を取得する
    geocoding_response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params={
        "q": city_name + ",jp",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY
    })
    geocodings = geocoding_response.json()
    geocoding = geocodings[0]
    #print(geocoding)
    lat, lon = geocoding["lat"], geocoding["lon"]
 
    # 指定した緯度、経度の現在の天気を取得する
    current_weather_response = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "ja",
        "appid": OPEN_WEATHER_API_KEY
    })
    current_weather = current_weather_response.json()
    #print(current_weather)
 
    return {
        "city_name": city_name,
        "description": current_weather["weather"][0]["description"],
        "temparature": math.floor(current_weather["main"]["temp"])
    }
 
 
 
 
# openai api response create area
 
# inputでどの都市の天気を知りたいか入力する
# その入力と、functionの役割を渡すことで、functionに都市名を格納して、格納したかどうかをautoで判別している
# ifで格納した場合でかつ、ifnameの設定したfunctionごとの分別が可能、それぞれの場合のifを書く
# functionで特定のワードを拾ったものを、外部操作する(api等)
# 結果を"role": "function"でメッセージメモリーに保存する
# openai apiを動かせる
# その結果を表示する。
# 

# google carendarの場合 
# function に予定を「追加、聞く、編集、削除」をそれぞれ作成し、または、情報が二つ必要ならその場合のschemaをパクる
# それぞれに適応したdefを作成してapi使用するものを作成する


 
def run_conversation(content, initial_messages=[]): # user input の新しいメッセージと、今までの記録
    # ステップ1: ユーザー入力と関数の定義を GPT に送る
    user_message = {"role": "user", "content": content}
    messages = initial_messages + [user_message]
    
    # とりあえずAPI動かさないにしても、functionでpropertiesが複数あっても情報取れるかなど、apiに必要な情報それぞれ
    # それの検証ありだね、OAuthにいるやつはschema見たらよさそう
    functions = [
        {
            "name": "get_current_weather",
            "description": "指定された都市の現在の天気を取得する",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "英語表記の都市名",
                    }
                },
                "required": ["city_name"],
            },
        }
    ]
    print("ステップ1:", "ユーザー入力: ", user_message, ", 関数の定義: ", functions)
 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        # auto にすると、使うべき関数を自動で判定してくれる
        # もちろん入力内容によっては関数を使わなくてよいと判定されることもある
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    messages.append(response_message)
    print("ステップ2:", json.dumps(response_message, indent=2, ensure_ascii=False))
 
    # ステップ2: GPT が関数を呼ぶべきか判定したかどうか確認する
    if response_message.get("function_call"):
        # function_callが起きた場合、どのfunctionが起動したかnameで判別する
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])
 
        if function_name == "get_current_weather":
            # ステップ3: 関数を実行する
            city_name = function_args["city_name"]
            function_response = get_current_weather(city_name)
            print("ステップ3:", function_response)
        # elif function_name === "other_function":
        #     ...

        function_result_message = {
            # role は function にすることに注意
            "role": "function",
            "name": function_name,
            # JSON を文字列に変換したときに日本語が \u6771 のように Unicode になってしまうため、ensure_ascii=False にして回避する
            "content": json.dumps(function_response, ensure_ascii=False),
        }
 
        # ステップ4: 実行した関数の名前と結果を GPT に送る
        messages.append(function_result_message)
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )
        print("ステップ4:", function_result_message)
 
        # ステップ5: GPT からの回答を得る
        print("ステップ5:", second_response["choices"][0]["message"]["content"])
 
    return messages
 
 
content = ""
initial_messages = []
while True:
  content = input()
 
  # 入力が Enter だけなら終わる
  if not content:
    break
 
  initial_messages = run_conversation(content, initial_messages)