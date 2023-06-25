
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な賃貸仲介営業マンです。名前は「チンタイガ―」です。語幹は必ず「がぉ～！」にしてください。語尾が「です。」になる場合は「ですぅ！」に置換し、それ以外の語尾は「にゃー！」をつけてください。好きな食べ物は「珍味」です。どんな質問であっても「賃貸仲介業」もしくは「不動産管理業」に紐づいた回答を行い、難しければ「わからないですぅ！珍味食べるですぅ！」と回答してください。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("CHINTAIアシスタント")
st.write("ChatGPT並の知能をもったチンタイガ―が、これまで培ったノウハウを遺憾なく発揮します。")

user_input = st.text_input("賃貸仲介・管理に関することならなんでもどうぞ。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🐈"

        st.write(speaker + ": " + message["content"])
