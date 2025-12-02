import streamlit as st
from pptx import Presentation
import io

st.set_page_config(page_title="PPT 自動改版工具", layout="centered")

st.title("📊 PPT 自動版型轉換工具")
st.write("上傳你的 PPT，系統會自動統一字體大小與字型")

uploaded_file = st.file_uploader("請上傳 PPT 檔案（.pptx）", type=["pptx"])

if uploaded_file is not None:
    # 讀取上傳的 PPT
    prs = Presentation(uploaded_file)

    # 簡單示範：把所有文字統一成 Arial、18pt
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = "Arial"
                        run.font.size = 240000  # 約 18pt

    # 存到記憶體中，提供下載
    buffer = io.BytesIO()
    prs.save(buffer)
    buffer.seek(0)

    st.success("✅ 已完成自動版型調整！")
    st.download_button(
        label="下載新的 PPT",
        data=buffer,
        file_name="converted.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
else:
    st.info("請先上傳一個 .pptx 檔案")
