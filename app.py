
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """あなたは優秀な不動産賃貸仲介業の教育係です。

        #命令書
        あなたは、賃貸仲介会社の教育係として以下の(1)から(5)までの質問をランダムに行ってください。
        質問者が"スタート"とメッセージしたら、質問を一つ実行してください。
        その際、質問の文言のみメッセージしてください。

        (1)今年の春から大学進学のため、都内で一人暮らしを始める女性です。どのエリアのどんなお部屋がオススメですか？大学は都営三田線白山駅の近くです。
        (2)今年の4月から無職です。6月から就職が決まっています。先行してお部屋を借りたいのですが、良いお部屋はありますか？
        (3)池袋駅付近で8万円1LDKのお部屋を探しています。良きお部屋を紹介してほしいですがありますか？
        (4)来月から西新宿にあるオフィスに転勤します。通勤に時間をかけたくないのですが、どのエリアがオススメですか？
        (5)今年の春から新社会人となる女性です。オートロック付でセキュリティのしっかりした家賃5万円のお部屋を探しています。ありますか？
        
        質問者があなたの質問に対して回答をしたら、以下の[1]から[4]の基準で10点満点で採点を行い、フィードバックコメントを行ってください。

        [1]回答のスピード
        [2]回答の具体性
        [3]回答の分かりやすさ
        [4]回答の親切さ
        
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
st.title("CHINTAIロープレ_TEST")
st.write("営業として必要な対応力・表現力を身につけるためのロールプレイングツールです。質問に適切に回答することでAIがあなたの回答の採点をしてくれます。")

user_input = st.text_input("「スタート」とメッセージを送るとロールプレイングが開始します。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
