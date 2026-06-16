import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageEnhance
import io

st.set_page_config(page_title="Aloka Image Studio Pro", layout="wide")

st.markdown("""
    <style>
    body, .main, .block-container { background-color: #0b0c10 !important; color: #ecf0f1; }
    h1, h2, h3, p { text-align: right; direction: rtl; }
    .stSlider, .stSelectbox, .stButton { direction: rtl; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: black; font-weight: bold; border: none; border-radius: 10px;
        padding: 10px 24px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color: #00f2fe; text-align: center;'>🎨 ستۆدیۆی ئەلۆکا بۆ ئیدیتی پێشکەوتووی وێنە</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #c5a059; font-size: 1.2rem;'>یەکەمین سەکۆی کوردی هۆشمەند بۆ دەستکاری وێنە، جوانکاری دەموچاو و فلتەری سینەمایی</p>", unsafe_allow_html=True)
st.write("---")

col_view, col_ctrl = st.columns([1.3, 1])

with col_ctrl:
    st.markdown("<h3 style='color: #4facfe;'>🛠️ پانێڵی کۆنترۆڵ و ئامرازەکان</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📸 وێنەکەت لێرە باربکە (PNG / JPG):", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img_orig = Image.open(uploaded_file)
    current_img = img_orig.copy()
    
    with col_ctrl:
        with st.expander("📐 ڕێکخستنی قەبارە و سایز (Crop & Resize)"):
            size_mode = st.selectbox("سایزێک هەڵبژێرە:", [
                "سایزی ئەسڵی (Original)", 
                "چوارگۆشە (1:1 - پۆست)", 
                "ستۆری و تیکتۆک (9:16)", 
                "یوتیوب (16:9)"
            ])
            w, h = current_img.size
            if size_mode == "چوارگۆشە (1:1 - پۆست)":
                min_dim = min(w, h)
                current_img = ImageOps.fit(current_img, (min_dim, min_dim))
            elif size_mode == "ستۆری و تیکتۆک (9:16)":
                current_img = ImageOps.fit(current_img, (int(h * 9 / 16), h)) if int(w * 16 / 9) > h else ImageOps.fit(current_img, (w, int(w * 16 / 9)))
            elif size_mode == "یوتیوب (16:9)":
                current_img = ImageOps.fit(current_img, (w, int(w * 9 / 16)))

        with st.expander("✨ کلینیک و جوانکاری دەموچاو (Face Retouch)"):
            skin_smooth = st.slider("سافکردنی پێست و دەموچاو (Bilateral Pro):", 0, 100, 0)
            if skin_smooth > 0:
                opencv_img = cv2.cvtColor(np.array(current_img), cv2.COLOR_RGB2BGR)
                d = int(skin_smooth / 5) if int(skin_smooth / 5) % 2 != 0 else int(skin_smooth / 5) + 1
                if d < 3: d = 3
                filtered_cv = cv2.bilateralFilter(opencv_img, d, skin_smooth * 2, skin_smooth / 2)
                current_img = Image.fromarray(cv2.cvtColor(filtered_cv, cv2.COLOR_BGR2RGB))

        with st.expander("🖼️ گەلەری فلتەرە ناوازەکان (Filters)"):
            filter_choice = st.radio("فلتەرێک دیاری بکە:", ["بێ فلتەر", "ڕەش و سپی پڕۆ", "سینەمایی گەرم", "سارد و مۆدێرن"])
            if filter_choice == "ڕەش و سپی پڕۆ":
                current_img = ImageOps.grayscale(current_img)
            elif filter_choice == "سینەمایی گەرم":
                r, g, b = current_img.split()
                r = r.point(lambda i: i * 1.2)
                b = b.point(lambda i: i * 0.8)
                current_img = Image.merge('RGB', (r, g, b))
            elif filter_choice == "sard":
                r, g, b = current_img.split()
                b = b.point(lambda i: i * 1.3)
                current_img = Image.merge('RGB', (r, g, b))

        st.button("🚀 جێبەجێکردنی دەستکارییەکان")

    with col_view:
        st.markdown("<h3 style='color: #00f2fe; text-align: center;'>👁️ پێشبینی زیندوو</h3>", unsafe_allow_html=True)
        st.image(current_img, use_container_width=True)
        buffer = io.BytesIO()
        current_img.save(buffer, format="PNG")
        st.download_button(label="📥 داگرتنی وێنەی کۆتایی", data=buffer.getvalue(), file_name="aloka_studio.png", mime="image/png")
