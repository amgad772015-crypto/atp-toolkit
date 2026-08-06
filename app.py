import os
import zipfile
import streamlit as st
from docx import Document

# 1. إعدادات واجهة المستخدم للتناسب مع كل الشاشات
st.set_page_config(
    page_title="ATP Auditor Toolkit",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. دالة توليد المستندات وضغطها في ملف ZIP واحد
def create_zip_package():
    output_dir = "ATP_Toolkit_Files"
    os.makedirs(output_dir, exist_ok=True)

    files_data = {
        "01_Audit_Manual.docx": "01 - دليل المراجع الداخلي\n\n1. مقدمة المراجعة الداخلية\n2. أهداف المراجعة\n3. منهجية العمل\n4. تقييم المخاطر\n5. أساليب جمع الأدلة\n6. كتابة الملاحظات\n7. إعداد التقرير النهائي",
        "02_Audit_Programs.docx": "02 - برامج المراجعة التفصيلية\n\n• الخزينة والنقدية\n• المشتريات والعقود\n• المخازن واللوجستيات\n• الأصول الثابتة\n• القوائم والتقارير المالية",
        "03_Findings_Library.docx": "03 - مكتبة الملاحظات المعتمدة\n\n• ATP-TRE: الخزينة (45 ملاحظة)\n• ATP-PRO: المشتريات (45 ملاحظة)\n• ATP-WHS: المخازن (36 ملاحظة)\n• ATP-FIX: الأصول (27 ملاحظة)\n• ATP-FS: المالية (27 ملاحظة)",
        "04_Audit_Forms.docx": "04 - النماذج المعتمدة\n\n• ATP-F01: خطة المراجعة\n• ATP-F02: برنامج الاختبار\n• ATP-F03: ورقة الملاحظة\n• ATP-F04: التقرير النهائي\n• ATP-F05: متابعة الإجراءات\n• ATP-F06: تقييم المخاطر",
        "05_Fraud_Matrix.docx": "05 - مصفوفة الاحتيال\n\n1. مؤشر الاحتيال\n2. الإدارة المعنية\n3. درجة الخطورة\n4. اختبار المراجع\n5. الإجراء الوقائي",
        "06_Pocket_Edition.docx": "06 - النسخة السريعة\n\n☑ قائمة فحص الخزينة، المشتريات، المخازن، الأصول، والمالية"
    }

    for filename, content in files_data.items():
        doc = Document()
        doc.add_heading(filename.replace(".docx", ""), level=1)
        doc.add_paragraph(content)
        doc.save(os.path.join(output_dir, filename))

    zip_path = "ATP_Internal_Auditor_Toolkit_Beta_v0.1.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    
    return zip_path

# 3. بناء الواجهة والتنقل
st.title("🟢 ATP Internal Auditor Toolkit")
st.caption("Beta v0.1 | متوافق مع الهاتف والحاسوب")

# القائمة الجانبية
st.sidebar.header("قائمة التنقل")
section = st.sidebar.radio(
    "اختر المجلد:",
    ["01 - الدليل", "02 - برامج المراجعة", "03 - مكتبة الملاحظات", "04 - النماذج", "05 - مصفوفة الاحتيال", "06 - النسخة السريعة"]
)

# زر تحميل الملفات المضغوطة
st.sidebar.divider()
zip_file_path = create_zip_package()
with open(zip_file_path, "rb") as fp:
    st.sidebar.download_button(
        label="📦 تنزيل الحزمة الكاملة (ZIP)",
        data=fp,
        file_name="ATP_Internal_Auditor_Toolkit_Beta_v0.1.zip",
        mime="application/zip",
        use_container_width=True
    )

# 4. عرض محتوى الأقسام
if section == "01 - الدليل":
    st.header("📁 01 - دليل المراجع الداخلي")
    st.text_area("المحتويات المعتمدة:", "1. مقدمة المراجعة الداخلية\n2. أهداف المراجعة وتحديد النطاق\n3. منهجية العمل والتخطيط\n4. تقييم المخاطر\n5. أساليب جمع الأدلة\n6. صياغة الملاحظات\n7. إعداد التقرير النهائي", height=200)

elif section == "03 - مكتبة الملاحظات":
    st.header("🔍 03 - مكتبة الملاحظات")
    search_term = st.text_input("ابحث عن ملاحظة أو كود:")
    
    findings = [
        {"code": "ATP-TRE-01", "cat": "الخزينة", "title": "عدم مطابقة رصيد النقدية الفعلي مع الدفاتر"},
        {"code": "ATP-PRO-01", "cat": "المشتريات", "title": "الشراء بدون أوامر توريد معتمدة"},
        {"code": "ATP-WHS-01", "cat": "المخازن", "title": "وجود أصناف تالفة دون اتخاذ إجراءات استبعاد"},
        {"code": "ATP-FIX-01", "cat": "الأصول", "title": "عدم وجود ترميز (Tagging) على الأصول"},
        {"code": "ATP-FS-01", "cat": "القوائم المالية", "title": "غياب التسويات الشهرية لحسابات البنوك"}
    ]

    for item in findings:
        if not search_term or search_term.lower() in item['code'].lower() or search_term in item['title']:
            st.info(f"**[{item['code']}]** ({item['cat']}): {item['title']}")

else:
    st.header(f"📂 {section}")
    st.write("المحتوى جاهز للتنزيل ضمن الحزمة الموحدة بصيغة Word.")
