import streamlit as st
import PyPDF2
import base64

st.set_page_config(page_title="مكتبة مهدي", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4CAF50; color: white; height: 3em; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 مساعد مهدي الدراسي (النسخة المستقرة)")

file = st.file_uploader("ارفع كتابك أو ملزمتك (PDF)", type="pdf")

if file:
    # تحويل الملف لبيانات قابلة للقراءة
    bytes_data = file.getvalue()
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    
    # محرك البحث الجانبي
    pdf_reader = PyPDF2.PdfReader(file)
    st.sidebar.header(f"عدد الصفحات: {len(pdf_reader.pages)}")
    query = st.sidebar.text_input("🔍 ابحث عن تعريف أو سؤال:")
    
    if query:
        matches = [i+1 for i, p in enumerate(pdf_reader.pages) if query.lower() in p.extract_text().lower()]
        st.sidebar.write(f"موجود في صفحات: {matches}" if matches else "غير موجود")

    st.write("---")
    
    # هذا الزر هو الحل النهائي للشاشة البيضاء
    st.success("تم تحميل الكتاب بنجاح!")
    
    # رابط يفتح الكتاب في المتصفح نفسه بطريقة "المعاينة"
    pdf_url = f"data:application/pdf;base64,{base64_pdf}"
    st.markdown(f'<a href="{pdf_url}" target="_blank" style="text-decoration: none;"><button style="width: 100%; background-color: #1E3A8A; color: white; padding: 15px; border: none; border-radius: 10px; font-size: 18px; cursor: pointer;">📖 اضغط هنا لفتح الكتاب للقراءة والنسخ</button></a>', unsafe_allow_html=True)
    
    st.warning("ملاحظة: عند الضغط على الزر، سيفتح الكتاب في نافذة جديدة، وهناك يمكنك تصفحه ونسخ ما تريد بكل سهولة.")

else:
    st.info("أهلاً بك يا بطل.. ارفع ملزمة السادس الآن وابدأ الدراسة.")
