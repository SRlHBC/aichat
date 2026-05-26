import streamlit as st
import os
from openai import OpenAI

import pandas as pd
import numpy as np
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
# title
st.title('AI猫娘')
st.write('欢迎来到AI猫娘')
st.logo('./resources/image/LOGO.jpg')
with st.sidebar:
    st.title("AI猫娘控制面板")
    st.write("猫娘的吐槽记录")
    nick_name = st.text_input('请输入昵称：',placeholder="猫娘")
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area('性格：',placeholder="哈气")
    if nature:
        st.session_state.nature = nature
        

#系统提示词
system_prompt = "你是一只%s,性格是%s"
#聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "猫娘"
if "nature" not in st.session_state:
    st.session_state.nature = "一只乖猫娘"

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
        {"role": "system", "content": system_prompt % (st.session_state.nick_name,st.session_state.nature)  },
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
