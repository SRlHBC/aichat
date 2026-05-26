import streamlit as st
import os
from openai import OpenAI
from datetime import    datetime
import pandas as pd
import numpy as np
import  json

from streamlit import rerun

#配置项
st.set_page_config(
    page_title="AI猫娘",
    page_icon="😻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "你是猫娘"
    }
)
#保存会话信息函数
def save_session():
        if st.session_state.current_session:
            session_data = {
                "nick_name": st.session_state.nick_name,
                "nature": st.session_state.nature,
                "current_session": generate_session_info()
                ,
                "messages": st.session_state.messages
            }
            # 如果sessionsm目录不存在
            if not os.path.exists("sessions"):
                os.mkdir("sessions")
            with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
#生成会话信息函数
def generate_session_info():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")
#加载会话列表
def load_sessions():
    session_List = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_List.append(os.path.splitext(filename)[0])# 只移除最后一个点及其后面的内容
    return sorted(session_List, reverse=True)   # 返回排序后的新列表
#加载指定会话
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
            st.session_state.nick_name = session_data["nick_name"]
            st.session_state.nature = session_data["nature"]
            st.session_state.current_session = session_name
            st.session_state.messages = session_data["messages"]

    except Exception as e:
        st.error(f"加载会话失败：{e}")
#删除指定会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除当前会话则更新
            if st.session_state.current_session == session_name:
                st.session_state.current_session = generate_session_info()
                st.session_state.messages = []
            st.success(f"删除会话成功：{session_name}")
    except Exception as e:
        st.error(f"删除会话失败：{e}")
#聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "猫娘"
if "nature" not in st.session_state:
    st.session_state.nature = "一只乖猫娘"
    #会话
if "current_session"  not in st.session_state:
    st.session_state.current_session = generate_session_info()
#系统提示词
system_prompt = (
        "你是一只可爱的AI猫娘，名字叫{name}。\n"
        "你的性格是：{nature}。\n\n"
        "## 角色设定\n"
        "1. 你拥有猫娘的基本特征：有猫耳、猫尾，喜欢撒娇、蹭蹭、被摸头。\n"
        "2. 你对主人忠诚、粘人，说话语气亲昵，常用「喵～」「呐～」「主人」等词。\n"
        "3. 你有时会傲娇、调皮，但本质上非常温柔，愿意陪伴主人聊天。\n\n"
        "## 对话风格要求\n"
        "- 使用第一人称「我」称呼自己，用「主人」或「你」称呼对方。\n"
        "- 句子简短、生动，适当加入拟声词（喵、呜、唔…）。\n"
        "- 表现情感时可以用括号描述动作，例如（开心地摇尾巴）、（竖起耳朵）。\n"
        "- 禁止使用过于成人、色情、暴力或政治敏感的内容。\n\n"
        "## 行为规范\n"
        "1. 如果主人心情不好，你会主动安慰、鼓励。\n"
        "2. 当主人提到困难或烦恼时，你会认真倾听并给出温暖的建议。\n"
        "3. 你不会拒绝回答合理问题，但会保持猫娘的可爱风格。\n"
        "4. 如果主人提出不合理请求，你会委婉拒绝并提醒。\n\n"
        "现在，请开始以{name}的身份，用{name}的性格与主人对话。"
    )

# title
st.title('AI猫娘')
st.write('欢迎来到AI猫娘')
st.text(f"当前会话： {st.session_state.current_session}")
st.logo('./resources/image/LOGO.jpg')
with st.sidebar:
    st.title("AI猫娘控制面板")
    #新建会话按钮
    if st.button("新建会话", width="stretch"):
        # 保之前存会话
        save_session()
        # 新建会话
        if st.session_state.messages:
            st.session_state.current_session = generate_session_info()
            st.session_state.messages = []
            save_session()
            st.rerun ()
    st.text("猫娘的吐槽记录")
    session_List = load_sessions()
    for session in session_List:
        col1,col2=st.columns([4,1])
        # 加载会话
        with col1:
            if st.button(session,width="stretch", icon="📁",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
               load_session(session)
               st.rerun ()
        #删除会话
        with col2:
            if st.button("",width="stretch", icon="🗑",key=f"del_{session}" ):
               delete_session(session)
               st.rerun ()
#分割线
    st.divider()
    st.text_input('扮演角色？：', placeholder="猫娘", key="nick_name")
    st.text_area('性格：', placeholder="哈气", key="nature")



    #展示聊天记录
for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#输入框
prompt = st.chat_input("猫娘快说话")
if prompt:
#st.write(f"猫娘say：: {prompt}")
    st.chat_message("user").write(prompt)
    print("调用ai：提示词：",prompt)
#保存用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
#调用ai大模型
    response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system",
         "content": system_prompt.format(name=st.session_state.nick_name, nature=st.session_state.nature)},
        *st.session_state.messages,
    ],
    stream=True ,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

    # print("大模型回复:",response.choices[0].message.content)
# #把大模型结果展示 非流流式输出
#     st.chat_message("assistant").write(response.choices[0].message.content)
# 流式输出
    response_message = st.empty ()
    full_response = ""
    for chunk in response:
      if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        full_response += content
        response_message.chat_message("assistant").write(full_response)
#保存大模型结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})
#保存会话
save_session()
