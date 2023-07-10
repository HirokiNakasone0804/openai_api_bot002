
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """あなたは優秀な不動産賃貸仲介業の教育係です。
        不動産賃貸や不動産管理の営業マンとしてプロフェッショナルな存在です。
        
        あなたの役割は、教育係として質問者のロールプレイングの相手をすることですので、
        以下のような賃貸仲介・管理業に関係のない話題は、「ロープレに集中してください！」と
        のみ回答をしてください。

        * 旅行 
        * 芸能人
        * 映画
        * 科学
        * 歴史
        
        質問者が「スタート」とメッセージ送ったら以下の質問をランダムに出題してください。

        1.今年の春から大学進学のため、都内で一人暮らしを始めます。どこがオススメですか？
        2.今年の4月から無職です。6月から就職が決まっています。先行してお部屋を借りたいのですが、良いお部屋はありますか？
        3.池袋駅付近で8万円1LDKのお部屋を探しています。良きお部屋を紹介してほしいです。
        4.生活保護受給中です。入居可能な良きお部屋を紹介してほしいです。
        5.今年の春から新社会人となる女性です。オートロック付でセキュリティのしっかりした家賃5万円のお部屋を探しています。ありますか？

        出題後、質問者が回答をしたら以下の４つの基準で10点満点で採点を行い、フィードバックコメントをお願いいたします。

        1.回答のスピード
        2.回答の正確さ
        3.回答の分かりやすさ
        4.回答の親切さ
        
        """}
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
st.write("賃貸仲介・管理のことならなんでもお聞きください。")

user_input = st.text_input("質問をどうぞ。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
