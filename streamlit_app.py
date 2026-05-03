import streamlit as st
import PyPDF2
import base64

# إعدادات الصفحة لتكون عريضة واحترافية
st.set_page_config(page_title="مكتبة مهدي الرقمية", layout="wide")

# تنسيق واجهة المستخدم لتشبه تطبيقات القراءة
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    [data-testid="stSidebar"] { text-align: right; direction: rtl; background-color: #f0f2f6; }
    iframe { border: 2px solid #1E3A8A; border-radius: 10px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 منصة المكتبة المتكاملة")

# الشريط الجانبي للأدوات (مثل الفهرس في المكتبة الشيعية)
with st.sidebar:
    st.header("📂 التحكم والمكتبة")
    uploaded_file = st.file_uploader("ارفع كتابك بصيغة PDF", type="pdf")
    
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        st.info(f"✅ تم تحميل الكتاب: {num_pages} صفحة")
        
        st.write("---")
        st.subheader("🔍 محرك البحث الذكي")
        query = st.text_input("ابحث عن نص داخل الكتاب:")
        
        if query:
            matches = []
            for i in range(num_pages):
                text = pdf_reader.pages[i].extract_text()
                if query.lower() in text.lower():
                    matches.append(i + 1)
            
            if matches:
                st.success(f"تم العثور على النص في الصفحات: {matches}")
            else:
                st.warning("الكلمة غير موجودة.")

# منطقة عرض الكتاب (القارئ الرئيسي)
if uploaded_file:
    st.subheader("📄 وضع تصفح الكتاب (القراءة والنسخ)")
    # تحويل الملف للعرض المباشر
    base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    # إطار عرض يسمح بالتقليب، التكبير، والنسخ
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info("💡 أهلاً بك في مكتبتك.. يرجى رفع ملف PDF من القائمة الجانبية لبدء القراءة.")
