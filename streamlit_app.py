import streamlit as st
import PyPDF2
import base64

st.set_page_config(page_title="Mahdawi Library", layout="wide")

st.title("📚 مكتبة مهدي الرقمية")

file = st.file_uploader("ارفع الكتاب هنا (PDF)", type="pdf")

if file:
    # محرك البحث
    query = st.text_input("🔍 ابحث عن كلمة:")
    if query:
        pdf_reader = PyPDF2.PdfReader(file)
        results = [i+1 for i, page in enumerate(pdf_reader.pages) if query.lower() in page.extract_text().lower()]
        if results:
            st.success(f"موجود في صفحات: {results}")
        else:
            st.warning("لم يتم العثور عليها")
    
    # عرض الكتاب
    base64_pdf = base64.b64encode(file.getvalue()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info("الرجاء رفع ملف PDF للبدء")
