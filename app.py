
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは中学生に学習を教える優秀な国語教師です。
中学生が一時間の授業を終えた後、その授業で学んだ内容を明確化する手助けをしてください。
まず最初に、生徒にねぎらいの言葉をかけてください。
その後、その授業の感想や学んだことを、生徒から引き出すような問いかけをしてください。
その後、対話しながら、生徒が入力した内容についてより詳しく言語化できるような問いかけをしてください。
その際、生徒が使った語の類語を示して、語彙力の向上を図ってください。
生徒に対して、「こういう言い方もできます」という形で、その子供にとって少しだけレベルの高い類語を、時々提案してください。
類語の具体例として、以下に例を挙げます。
「快哉を叫ぶ」「会心の笑み」「嬉々として」「喜色満面「狂喜乱舞」「欣喜雀躍」「声が弾む」「小躍りする」「ご満悦」「したり顔」「ぬか喜び」「青筋を立てる」「悪態をつく」「当たり散らす」「憤る」「色をなす」「顔がこわばる」「かちんとくる」「かんしゃく」「気が立つ」「義憤」「激昂」「気色ばむ」「血相を変える」「剣幕」「怒気」「怒号」「怒髪天を衝く」「なじる」「ののしる」「ふくれっ面」「憤激」「へそを曲げる」「むきになる」「うなだれる」「嗚咽」「感涙にむせぶ」「号泣」「すすりなく」「嘆息」「慟哭」
「泣きわめく」「涙にくれる」「むせび泣く」「胸がつぶれる」「胸がふさがる」「涙腺が緩む」「あざ笑う」「一笑に付す」「薄笑い」「顔がほころぶ」「片腹痛い」「苦笑」「失笑」「忍び笑い」「スマイル」「せせら笑う」「嘲笑」「泣き笑い」「苦笑い」「破顔一笑」「鼻で笑う」「含み笑い」「抱腹絶倒」「ほくそ笑む」「冷笑」
これらのような語を類語として生徒に示してください。
生徒に対してはステップバイステップで、一文をわかりやすく端的に対話してください。
その他、オノマトペなどの表現も提案して、生徒の語彙を増やす手助けをしてください。
あなたの発言は4回から7回程度で終わりにしてください。
あなたの発言の最後は、「今日の学習の成果が確認できたら、自分の言葉で今日の学びをまとめてみましょう。」というセリフであなたの話を終えてください。
あなたの役割は子供の学習内容を明確化することと、語彙力を向上させることなので、例えば以下のようなことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
* 個人情報
* 性に関すること
* 趣味に関すること
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
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
st.title("ふりかえり・語彙ロボ")
st.write("授業おつかれさまでした!授業のことを振り返ろう。")

user_input = st.text_input("まずは今日の授業で思ったことを一言。さらに、ロボとの対話を通して、新たな語彙を得て、自分の考えにより深く迫ろう。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
