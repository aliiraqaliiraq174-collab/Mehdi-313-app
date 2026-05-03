import streamlit as st
import PyPDF2
from pdf2image import convert_from_bytes
import io

st.set_page_config(page_title="مكتبة مهدي", layout="wide")

st.title("📚 مكتبة مهدي - عرض مضمون 100%")

file = st.file_uploader("ارفع الكتاب (PDF)", type="pdf")

if file:
    # الجزء الأول: البحث (شغال تمام)
    pdf_reader = PyPDF2.PdfReader(file)
    st.sidebar.success(f"عدد الصفحات: {len(pdf_reader.pages)}")
    query = st.sidebar.text_input("🔍 ابحث عن كلمة:")
    if query:
        results = [i+1 for i, p in enumerate(pdf_reader.pages) if query.lower() in p.extract_text().lower()]
        st.sidebar.write(f"وُجدت في: {results}" if results else "غير موجودة")

    # الجزء الثاني: الحل لمشكلة الشاشة البيضاء (العرض كصور)
    st.subheader("📖 تصفح الصفحات")
    images = convert_from_bytes(file.getvalue(), first_page=1, last_page=20) # عرض أول 20 صفحة للسرعة
    
    for i, image in enumerate(images):
        st.image(image, caption=f"صفحة {i+1}", use_container_width=True)
        st.write("---")
else:
    st.info("ارفع الملزمة هنا لتظهر لك فوراً بدون شاشة بيضاء.")
