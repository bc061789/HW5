import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------
# Step 1：自行加入 Human / AI 文本
# -------------------------
def get_dataset():
    # Human 文章（例如維基百科、新聞、你自己寫的）
    human_texts = [
        "人類文章示範：台灣位於東亞島弧，在地理與氣候上具有高度多樣性，孕育出豐富的自然環境與文化特色。每年吸引大量旅客前來體驗山海景觀與城市生活。",
        "人類文章示範：棒球是台灣最受歡迎的運動之一，無論是職業聯盟或國際賽事都能吸引大量觀眾支持。許多選手也在海外職棒舞台上展現實力。",
    ]

    # AI 文章（建議用 ChatGPT 生成 20 段左右）
    ai_texts = [
        "AI 文章示範：台灣擁有獨特的自然地理環境，使其在生態與旅遊發展上具有多元優勢。旅客常在短時間內即可體驗山海景觀的強烈對比。",
        "AI 文章示範：棒球在台灣具有深厚文化意義，不僅是運動，更是一種凝聚社會情感的象徵。球迷對比賽的投入反映了運動的社會價值。",
    ]

    texts = ai_texts + human_texts
    labels = [1] * len(ai_texts) + [0] * len(human_texts)   # 1 = AI, 0 = Human
    return texts, labels

# -------------------------
# Step 2：訓練模型（加 cache 避免 Cloud 重訓）
# -------------------------
@st.cache_resource
def train_model():
    texts, labels = get_dataset()

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        min_df=1
    )
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=2000)
    model.fit(X, labels)

    return vectorizer, model

vectorizer, model = train_model()

# -------------------------
# Step 3：Streamlit UI
# -------------------------
st.set_page_config(page_title="AI / Human 文章偵測器", layout="wide")

st.title("Q1 — AI / Human 文章偵測器（AI Detector）")
st.write("輸入一段文字，我會幫你估計這段文字較像是 **AI** 還是 **Human**。")

user_text = st.text_area("請輸入要分析的文字：", height=200)

if st.button("開始偵測"):

    if not user_text.strip():
        st.warning("請先輸入文字才能偵測喔！")
    else:
        X_input = vectorizer.transform([user_text])
        proba = model.predict_proba(X_input)[0]  # [P(Human=0), P(AI=1)]

        ai_prob = float(proba[1])
        human_prob = float(proba[0])

        ai_percent = ai_prob * 100
        human_percent = human_prob * 100

        col1, col2 = st.columns(2)
        with col1:
            st.metric("AI %", f"{ai_percent:.1f}%")
        with col2:
            st.metric("Human %", f"{human_percent:.1f}%")

        st.write("---")
        st.subheader("機率視覺化")

        st.progress(ai_prob)
        st.caption("進度條越靠右，越像 AI 生成。")

        st.bar_chart({
            "probability": [ai_prob, human_prob]
        })

        st.info("此分類器使用自行蒐集的資料訓練：Human 來自維基與新聞，AI 來自 ChatGPT。資料量越多，結果越精準。")
