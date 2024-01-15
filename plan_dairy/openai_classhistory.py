class chatmemory:
    memory = []
    def fastmessage(chat_prompt):
        fastm = [{
            "role":"system",
            "content":chat_prompt
        },
        {
            "role":"user",
            "content":"2/2 スタート"
        }]
        chatmemory.memory=fastm
    
    def save_message(role,new_message):
        addmessage = {
            "role":role,
            "content":new_message
        }
        chatmemory.memory.append(addmessage)

chatmemory.fastmessage(chat_prompt ="私は人間です")
chatmemory.save_message(role="user",new_message="ok")
print(chatmemory.memory)        
