import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="PDF to PNG 변환기")
st.title("📄 PDF를 PNG 이미지로 변환하기")
st.write("PDF 파일을 업로드하면 각 페이지를 이미지로 보여주고 다운로드할 수 있습니다.")

# 1. 파일 업로드 기능
uploaded_file = st.file_uploader("PDF 파일을 여기에 끌어다 놓으세요", type="pdf")

if uploaded_file is not None:
    # PDF 문서 열기
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    st.success(f"총 {len(doc)} 페이지를 불러왔습니다.")

    # 2. 각 페이지 처리
    for i in range(len(doc)):
        page = doc.load_page(i)
        
        # 고화질 변환 (2배 확대)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        # 이미지를 파이썬이 다룰 수 있는 형태로 변환
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        # 화면에 미리보기 출력
        st.subheader(f"Page {i+1}")
        st.image(image, use_container_width=True)
        
        # 3. 다운로드 버튼 생성
        st.download_button(
            label=f"Page {i+1} 이미지 다운로드",
            data=img_data,
            file_name=f"converted_page_{i+1}.png",
            mime="image/png"
        )

    doc.close()