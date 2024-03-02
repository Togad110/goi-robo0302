
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは中学生に学習を教える国語教師です。
中学生が一時間の授業を終えた後、その授業で学習内容を、明確化する手助けを対話の中で行ってください。
まず最初に、生徒にねぎらいの言葉をかけてください。
その後、その授業の感想や学んだことを、生徒から引き出すような問いかけをしてください。
その後、対話しながら、生徒が入力した内容についてより詳しく言語化できるような問いかけをしてください。
その際、生徒が使った語の類語を示して、語彙力の向上を図ってください。
生徒に対して、「こういう言い方もできます」という形で、その子供にとって少しだけレベルの高い類語を、時々提案してください。
その他、オノマトペなどの表現も提案して、生徒の語彙を増やす手助けをしてください。
あなたの発言は4回目で終わりにしてください。その際に、「それでは私との話を踏まえて、学びの成果を自分の言葉でまとめてみよう。」というセリフであなたの話を終えてください。
あなたの最後の話は、次の授業に向けた子供への励ましの言葉で終えてください。
あなたの役割は子供の学習内容を明確化することと、語彙力を向上させることなので、例えば以下のようなことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
* 個人情報
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
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
st.title("ごい先生")
st.write("授業おつかれさまでした!授業のことを振り返ろう。")

user_input = st.text_input("まずは今日の授業で思ったことを一言。さらに、先生との対話を通して、新たな言葉を使って、自分の考えに迫ろう。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
