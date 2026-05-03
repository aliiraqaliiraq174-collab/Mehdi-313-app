import streamlit as st
import PyPDF2
import base64

st.set_page_config(page_title="مكتبة مهدي الذكية", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    [data-testid="stSidebar"] { text-align: right; direction: rtl; }
    .pdf-info { background-color: #e1f5fe; padding: 15px; border-radius: 10px; border-right: 5px solid #01579b; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 مكتبة القراءة والبحث (الإصدار المستقر)")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    file = st.file_uploader("ارفع كتابك (PDF)", type="pdf")
    
    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        pages = len(pdf_reader.pages)
        st.success(f"تم تحميل {pages} صفحة")
        
        query = st.text_input("🔍 ابحث عن كلمة:")
        if query:
            results = [i+1 for i, p in enumerate(pdf_reader.pages) if query.lower() in p.extract_text().lower()]
            if results: st.info(f"موجودة في صفحات: {results}")
            else: st.warning("لم يتم العثور عليها")

if file:
    # تحويل الملف للعرض
    base64_pdf = base64.b64encode(file.getvalue()).decode('utf-8')
    
    # رابط لفتح الملف في نافذة جديدة (حل مشكلة الصفحة البيضاء)
    pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" target="_blank" style="text-decoration: none;"><div style="background-color: #4CAF50; color: white; padding: 10px; text-align: center; border-radius: 5px; margin-bottom: 10px;">🔓 اضغط هنا لفتح الكتاب في نافذة كاملة (إذا لم يظهر بالأسفل)</div></a>'
    st.markdown(pdf_link, unsafe_allow_html=True)

    # عرض الملف داخل الصفحة
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info("قم برفع ملف من القائمة الجانبية.")
