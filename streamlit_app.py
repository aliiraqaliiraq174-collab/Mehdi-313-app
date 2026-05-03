import streamlit as st
import PyPDF2
from pdf2image import convert_from_bytes
import io
import base64

st.set_page_config(page_title="مكتبة مهدي الاحترافية", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    [data-testid="stSidebar"] { text-align: right; direction: rtl; }
    .page-container { border: 1px solid #ddd; margin-bottom: 20px; padding: 10px; background: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 المكتبة الرقمية المتكاملة")

with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    uploaded_file = st.file_uploader("ارفع الكتاب (PDF)", type="pdf")
    
    if uploaded_file:
        # للقراءة والبحث
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        st.success(f"تم تحميل {num_pages} صفحة")
        
        query = st.text_input("🔍 ابحث عن نص داخل الكتاب:")
        if query:
            matches = [i+1 for i, p in enumerate(pdf_reader.pages) if query.lower() in p.extract_text().lower()]
            if matches: st.info(f"موجود في صفحات: {matches}")
            else: st.warning("لم يتم العثور على الكلمة")

if uploaded_file:
    st.subheader("📖 تصفح الكتاب")
    
    # تحويل صفحات الـ PDF إلى صور لعرضها بشكل مضمون
    # ملاحظة: سنعرض أول 10 صفحات كمثال لتجنب الثقل، ويمكنك التغيير
    bytes_data = uploaded_file.getvalue()
    
    # محرك العرض الاحترافي (عرض مباشر للـ PDF بطريقة معدلة)
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    
    # إنشاء "محيط قراءة" يمنع الصفحة البيضاء
    pdf_html = f'''
        <object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="1000px">
            <div style="padding:20px; text-align:center; background:#fff3cd;">
                <h3>⚠️ عذراً، متصفحك يرفض العرض المباشر</h3>
                <p>لحل المشكلة، اضغط على الزر أدناه لفتح الكتاب في نافذة مستقلة للنسخ والقراءة.</p>
                <a href="data:application/pdf;base64,{base64_pdf}" download="my_book.pdf" style="text-decoration:none;">
                    <button style="padding:10px 20px; background:#856404; color:white; border:none; border-radius:5px;">تحميل الكتاب وفتحه</button>
                </a>
            </div>
        </object>
    '''
    st.markdown(pdf_html, unsafe_allow_html=True)
else:
    st.info("ارفع ملفك الدراسي لفتحه في المكتبة.")
