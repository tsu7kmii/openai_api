userid = 112


def save_chat(res):
    global userid
    # 新しいメッセージを追加し、チャット履歴をファイルに保存
        
    if "+*+*end topic*+*+" in res:
        ress = res.replace("+*+*end topic*+*+","")
        # 終了したときの挙動
        with open("./plan_career/api_outputs/chat_last_"+str(userid)+".txt", "w+") as f:
            f.writelines(ress)
            
inin = "aaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaasssssssssss\nfffffffffffff\ngggggggggagds\nafasfaefadf\n\n+*+*end topic*+*+"

save_chat(inin)