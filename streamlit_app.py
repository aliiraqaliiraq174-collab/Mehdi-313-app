import streamlit as st
import PyPDF2
import base64

# إعداد الصفحة لتكون احترافية
st.set_page_config(page_title="مكتبة مهدي الرقمية", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    [data-testid="stSidebar"] { text-align: right; direction: rtl; }
    /* تحسين شكل قارئ الكتب */
    .pdf-container {
        border: 2px solid #1E3A8A;
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 مكتبة القراءة والبحث المتكاملة")

with st.sidebar:
    st.header("📂 لوحة التحكم")
    uploaded_file = st.file_uploader("ارفع ملف الـ PDF هنا", type="pdf")
    
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        st.success(f"✅ تم تحميل {num_pages} صفحة")
        
        st.write("---")
        query = st.text_input("🔍 ابحث عن نص:")
        if query:
            matches = [i + 1 for i, page in enumerate(pdf_reader.pages) if query.lower() in page.extract_text().lower()]
            if matches:
                st.success(f"موجود في صفحات: {matches}")
            else:
                st.warning("لم يتم العثور على النص.")

if uploaded_file:
    st.subheader("📄 عرض الكتاب")
    
    # تحويل الملف بصيغة تضمن ظهوره في أغلب المتصفحات
    bytes_data = uploaded_file.getvalue()
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    
    # استخدام كود عرض متطور مع خيار التحميل إذا فشل العرض
    pdf_display = f'''
        <div class="pdf-container">
            <iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" 
            width="100%" height="800" type="application/pdf">
                <p>متصفحك لا يدعم عرض الملف مباشرة، يمكنك تحميله أو فتحه بمتصفح آخر.</p>
            </iframe>
        </div>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    # إضافة زر تحميل احتياطي في حال بقيت الصفحة بيضاء
    st.download_button(
        label="📥 تحميل الكتاب أو فتحه في نافذة جديدة",
        data=bytes_data,
        file_name=uploaded_file.name,
        mime='application/pdf'
    )
else:
    st.info("💡 يرجى رفع ملف PDF من القائمة الجانبية للبدء.")
