
def deepseek():


    from openai import OpenAI
    import json
    with open("./models/api-config.json",'r',encoding="utf-8") as f:
        config = json.load(f)
        for m in config:
            if m['name']== 'deepseek':
                client = OpenAI(api_key=m['api_key'], base_url=m['base_url'])
                break 
        
    def talk_to_seller(history):
 
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=history,
        stream=True
        )

        for r in response:
            yield r.choices[0].delta.content
  

    return talk_to_seller

def ERNIE_Speed_8K():
    import requests
    import json
    with open("./models/api-config.json",'r',encoding="utf-8") as f:
        config = json.load(f)
        for m in config:
            if m['name']== 'ERNIE-Speed-8K':
                api_key = m['api_key']
                secret_key = m['secret_key']
                base_url = m['base_url']
                break 
    
        
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", token_url, headers=headers, data=payload)
    access_token =  response.json().get("access_token")
    url = base_url + access_token
    def talk_to_seller(history):

        data = json.dumps({
            "messages": history,
            "stream": True
        })
           
        response = requests.request("POST", url, headers=headers, data=data, stream=True)

        for line in response.iter_lines():
            response_str=line.decode('utf-8')
            result=""
            try:
                result = json.loads(response_str[6:])["result"]
            except:
                result = response_str
            yield result
    return talk_to_seller

def Yi_34B_Chat():
    import requests
    import json
    with open("./models/api-config.json",'r',encoding="utf-8") as f:
        config = json.load(f)
        for m in config:
            if m['name']== 'Yi-34B-Chat':
                api_key = m['api_key']
                secret_key = m['secret_key']
                base_url = m['base_url']
                break 
    
        
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", token_url, headers=headers, data=payload)
    access_token =  response.json().get("access_token")
    url = base_url + access_token
    def talk_to_seller(history):

        data = json.dumps({
            "messages": history,
            "stream": True
        })
           
        response = requests.request("POST", url, headers=headers, data=data, stream=True)

        for line in response.iter_lines():
            response_str=line.decode('utf-8')
            result=""
            try:
                result = json.loads(response_str[6:])["result"]
            except:
                result = response_str
            yield result
    return talk_to_seller

def gpt_3_5_turbo():
    from openai import OpenAI
    import json
    import os
    with open("./models/api-config.json",'r',encoding="utf-8") as f:
        config = json.load(f)
        for m in config:
            if m['name']== 'gpt-3.5-turbo':
                os.environ["OPENAI_API_KEY"] = m['api_key']
                client = OpenAI()
                break 
        
    def talk_to_seller(history):
 
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history,
        stream=True
        )

        for r in response:
            yield r.choices[0].delta.content
  

    return talk_to_seller
