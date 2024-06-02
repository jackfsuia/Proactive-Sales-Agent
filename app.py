from flask import Flask, render_template,request,session
from flask_socketio import SocketIO, emit,join_room
import time
from models.modelsAPI import deepseek, ERNIE_Speed_8K, Yi_34B_Chat,gpt_3_5_turbo
from queue import Queue, Empty
import threading
from threading import Thread
from datetime import datetime, timedelta
from tools.orders import print_order
model = deepseek()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

 

@app.route('/')
def index():

    return render_template('index.html')

# 模型的思考信息
def agent_message(send_msg, room_id):
    THINK_INTERVAL = 60
    with open('products/product_description', 'r',encoding='utf-8') as file:
        product_description = file.read()
        if product_description:
            mission_prompt=\
            f"现在你来扮演推销员，商品信息如下：\n{product_description}\n 你要向客户推销上面的商品。我来向你传达客户的话，你回答完，我再转达给客户。用户确定下单后，你在给客户的回复前加上这个格式的回复：\
                <客户姓名><北京市朝阳区18号><联系方式><购买数量><下单总额>。\n比如，假如客户李明已确定购买3瓶洗发水，地址是北京市朝阳区18号，电话213213，那么你就要回复：\
            订单信息：<李明><朝阳区18号><213213><3瓶><300元> 已下单，谢谢您的信任，我们会尽快发货！。或者，假如客户张三已确定购买5瓶洗发水，地址是广西玉林市民治区19栋20号，电话18937792，那么你就要回复：\
            订单信息：<张三><广西玉林市民治区19栋20号><18937792><5瓶><1500元> 已下单，谢谢您的信任，我们会尽快发货！。又或者，假如客户Tim已确定购买6瓶洗发水，地址是beijing,china，电话00-233-322，那么你就要回复：\
            订单信息：<Tim><beijing,china><00-233-322><6><102 dollars> 已下单，谢谢您的信任，我们会尽快发货！现在我帮你随机接通一个潜在客户的电话，接下来你要向他推销我们的产品，做好准备哈。他要是最后确定买的话，记得问他姓名，快递的收货地址和电话。\
            这个客户可能是中国人或外国人，他用什么语言你就用他相应的语言沟通。客户不说话的时候我会每{THINK_INTERVAL/60}分钟找你一次，请根据等待时间长短，揣摩客户心理以选择对他说话或者不说话，如果不说话，请回答waiting。客户说话的时候我会立即向你传达他说的话。"

    history = [
    # {"role": "system", "content": "你是一个人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"},
    {"role": "user", "content":mission_prompt},
    {"role": "assistant", "content":"好的，我准备好了,现在接通电话吧。到时候我会遵守你的格式的。"},
    {"role": "user", "content": "客户说: 你好。"}
    ]
    agent_activation_time = datetime.now()
    agent_proactive_num = 0


    while True:

        if history[-1]["role"] == 'user':
            waiting = False
            astream = model(history)
            agtmsg = ""
            cstmmsg = ""
            first_chunk = ""
            # streaming
            for chunk in astream:
                if not first_chunk:
                    first_chunk = chunk
                try:
                    # see if new user input exists in his/her message queue. If exist, break and process that, i.e. , add it to history for llm to process.
                    cstmmsg = send_msg.get_nowait()  
                    break
                except Empty:  
                    # "waiting" means the llm dont want to speak, as pre-defined in mission prompt.
                    if "waiting" in first_chunk[:8].lower():
                        agtmsg += first_chunk
                        waiting = True
                        break
                    else:
                        agtmsg += chunk
                        socketio.emit("response", chunk, to=room_id)
            if not waiting:
                # send the end sign to front end          
                socketio.emit("response", "END_OF_STREAM",to=room_id)     
            agent_activation_time = datetime.now()
            if agtmsg:
                history += [{"role": "assistant", "content": agtmsg}]
                # print orders to the cli
                print_order(agtmsg)

            if cstmmsg:
                history += [{"role": "user", "content": "客户说: " + cstmmsg + "。"}]
        else:

            try:
                cstmmsg = send_msg.get_nowait()
                history += [{"role": "user", "content": "客户说: " + cstmmsg + "。"}]
                agent_proactive_num = 0
                continue
                
            except Empty:
                # remind llm every THINK_INTERVAL seconds.
                time_difference = datetime.now() - agent_activation_time

                seconds_difference = time_difference.total_seconds()
                if seconds_difference > THINK_INTERVAL:
                    agent_proactive_num += 1
                    # tell llm "it has been agent_proactive_num*THINK_INTERVAL/60 minutes since user's last input, do you want to proactively say something to the user?" "waiting" means no.
                    history += [{"role": "user", "content": f"已过去了{agent_proactive_num*THINK_INTERVAL/60}分钟。客户还没回应。"}]
                    

@socketio.on('connect')
def test_connect(auth):
    room_id = request.sid  
    join_room(room_id)
    session['send_msg']=Queue()
    socketio.start_background_task(agent_message, session['send_msg'], room_id)
    # agent_thread = Thread(target=agent_message)
    # agent_thread.daemon = True
    # agent_thread.start()

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on('message')
def customer_message(data):
    session['send_msg'].put(data)

if __name__ == '__main__':

    socketio.run(app, debug=False)

