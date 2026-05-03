import streamlit as st
import PyPDF2
import base64

# إعداد الصفحة لتكون احترافية وعريضة
st.set_page_config(page_title="المكتبة الذكية", layout="wide")

# تصميم الواجهة الاحترافي
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; font-family: 'Arial'; }
    [data-testid="stSidebar"] { text-align: right; direction: rtl; }
    .stTextInput > div > div > input { text-align: right; }
    .pdf-frame { border: 2px solid #1E3A8A; border-radius: 10px; width: 100%; height: 900px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 مكتبة مهدي الرقمية المتكاملة")
st.write("الإصدار النهائي المستقر للقراءة والبحث والنسخ")

# القائمة الجانبية للأدوات
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    file = st.file_uploader("ارفع كتابك (PDF)", type="pdf")
    
    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        pages_count = len(pdf_reader.pages)
        st.success(f"تم تحميل الكتاب: {pages_count} صفحة")
        
        st.write("---")
        st.subheader("🔍 البحث داخل النص")
        query = st.text_input("اكتب الكلمة هنا:")
        
        if query:
            matches = [i+1 for i, p in enumerate(pdf_reader.pages) if query.lower() in p.extract_text().lower()]
            if matches:
                st.info(f"موجود في صفحات: {matches}")
            else:
                st.warning("الكلمة غير موجودة")

# المنطقة الرئيسية لعرض الكتاب
if file:
    # تحويل الملف للعرض بطريقة تمنع الصفحة البيضاء وتدعم النسخ
    base64_pdf = base64.b64encode(file.getvalue()).decode('utf-8')
    
    # استخدام تقنية الـ Iframe المدعومة في التطبيقات
    pdf_display = f'''
        <iframe class="pdf-frame" 
                src="data:application/pdf;base64,{base64_pdf}#toolbar=1" 
                type="application/pdf">
        </iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info("قم برفع ملف PDF من القائمة الجانبية لفتحه في القارئ الذكي.")
    
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
