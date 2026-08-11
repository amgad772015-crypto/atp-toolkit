import os
import unittest
import zipfile
from docx import Document

# ==========================================
# إعداد المسارات وقوائم الأسماء المتوقعة
# ==========================================
BASE_PATH = "ATP_Internal_Auditor_Toolkit_v1.0"

BATCH1_DIR = os.path.join(BASE_PATH, "01 - Foundational Documents")
BATCH2_DIR = os.path.join(BASE_PATH, "02 - Planning & Governance Documents")
BATCH3_DIR = os.path.join(BASE_PATH, "03 - Core Audit Working Papers")

BATCH1_EXPECTED_FILES = [
    "01_Audit_Manual.docx", "02_Audit_Programs_Master.docx",
    "03_Findings_Library.docx", "04_Audit_Forms_and_Templates.docx",
    "05_Fraud_Risk_Matrix.docx", "06_Pocket_Guide.docx",
    "00_BATCH_1_MANIFEST.docx"
]

BATCH2_EXPECTED_FILES = [
    "01_Audit_Charter.docx", "02_Annual_Audit_Plan.docx",
    "03_Resource_Allocation_Worksheet.docx", "04_Audit_Committee_Reporting_Template.docx",
    "05_Audit_KPIs_Dashboard.docx", "06_Process_Mapping_Templates.docx",
    "00_BATCH_2_MANIFEST.docx"
]

BATCH3_EXPECTED_FILES = [
    "01_Audit_Engagement_Planning.docx", "02_Preliminary_Survey_Workpaper.docx",
    "03_Risk_Assessment_Workpaper.docx", "04_Audit_Program_Template.docx",
    "05_Audit_Checklist_Master.docx", "06_Test_of_Controls_Workpaper.docx",
    "07_Substantive_Testing_Workpaper.docx", "08_Sampling_Workpaper.docx",
    "09_Audit_Evidence_Register.docx", "10_Audit_Findings_Workpaper.docx",
    "11_Observation_and_Recommendation_Workpaper.docx", "12_Management_Response_Workpaper.docx",
    "13_Follow_Up_Workpaper.docx", "14_Audit_Conclusion_Workpaper.docx",
    "15_Workpaper_Index_and_Cross_Reference.docx", "00_BATCH_3_MANIFEST.docx"
]

# ==========================================
# فئة الاختبارات التلقائية (Test Suite)
# ==========================================
class TestToolkitIntegrity(unittest.TestCase):

    def test_01_directories_exist(self):
        """اختبار وجود جميع مجلدات الحزم الرئيسية"""
        self.assertTrue(os.path.exists(BATCH1_DIR), "مجلد Batch 1 غير موجود!")
        self.assertTrue(os.path.exists(BATCH2_DIR), "مجلد Batch 2 غير موجود!")
        self.assertTrue(os.path.exists(BATCH3_DIR), "مجلد Batch 3 غير موجود!")

    def test_02_batch1_file_completeness(self):
        """اختبار وجود واكتمال ملفات Batch 1"""
        for filename in BATCH1_EXPECTED_FILES:
            filepath = os.path.join(BATCH1_DIR, filename)
            self.assertTrue(os.path.exists(filepath), f"الملف المفقود في Batch 1: {filename}")
            # التحقق من حجم الملف (أكبر من 7 كيلوبايت)
            self.assertGreater(os.path.getsize(filepath), 7000, f"حجم الملف صغير جداً: {filename}")

    def test_03_batch2_file_completeness(self):
        """اختبار وجود واكتمال ملفات Batch 2"""
        for filename in BATCH2_EXPECTED_FILES:
            filepath = os.path.join(BATCH2_DIR, filename)
            self.assertTrue(os.path.exists(filepath), f"الملف المفقود في Batch 2: {filename}")
            self.assertGreater(os.path.getsize(filepath), 7000, f"حجم الملف صغير جداً: {filename}")

    def test_04_batch3_file_completeness(self):
        """اختبار وجود واكتمال ملفات Batch 3"""
        for filename in BATCH3_EXPECTED_FILES:
            filepath = os.path.join(BATCH3_DIR, filename)
            self.assertTrue(os.path.exists(filepath), f"الملف المفقود في Batch 3: {filename}")
            self.assertGreater(os.path.getsize(filepath), 8000, f"حجم الملف صغير جداً: {filename}")

    def test_05_docx_structure_and_tables(self):
        """اختبار قابلية الفتح البرمجي وجودة البنية الجداولية داخل المستندات"""
        all_checks = [
            (BATCH1_DIR, BATCH1_EXPECTED_FILES),
            (BATCH2_DIR, BATCH2_EXPECTED_FILES),
            (BATCH3_DIR, BATCH3_EXPECTED_FILES)
        ]
        
        for folder, file_list in all_checks:
            for filename in file_list:
                filepath = os.path.join(folder, filename)
                try:
                    doc = Document(filepath)
                    # التأكد من وجود جدول واحد على الأقل في كل مستند
                    self.assertGreaterEqual(len(doc.tables), 1, f"المستند يفتقر للجداول: {filename}")
                except Exception as e:
                    self.fail(f"فشل فتح المستند {filename} برمجياً: {str(e)}")

    def test_06_zip_archives_validity(self):
        """اختبار سلامة وقابلية فتح الملفات المضغوطة الناتجة"""
        zip_files = [
            "ATP_Internal_Auditor_Toolkit_v1.0_Batch1.zip",
            "ATP_Internal_Auditor_Toolkit_v1.0_Batch3_Remediated.zip",
            "ATP_Internal_Auditor_Toolkit_v1.0_Final_Master.zip"
        ]
        for zf in zip_files:
            if os.path.exists(zf):
                self.assertTrue(zipfile.is_zipfile(zf), f"الملف المضغوط معطوب: {zf}")

# ==========================================
# تشغيل الاختبارات
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print("تشغيل وحدة الاختبارات التلقائية (Automated Testing)...")
    print("==================================================")
    unittest.main(verbosity=2)
          
