#!/usr/bin/env python3
"""
فحص بيئة بايثون: التحقق من وجود الاعتمادات وإظهار الإصدارات واقتراح أمر التثبيت.
لا يقوم بالتثبيت تلقائياً ما لم تُمرِّر --auto-install بصراحة.
"""
from __future__ import annotations
import importlib
import importlib.util
import sys
import subprocess
import argparse

# مكتبات: مفتاح = اسم الاستيراد، القيمة = (وصف باللغة العربية، اسم التوزيعة pip إذا اختلف)
REQUIRED_LIBRARIES = {
    "streamlit": ("Streamlit (واجهة المستخدم)", "streamlit"),
    "docx": ("python-docx (التعامل مع ملفات Word)", "python-docx"),
    "pytest": ("Pytest (بيئة الاختبارات التلقائية)", "pytest"),
    "pathlib": ("Pathlib (إدارة المسارات)", None),  # مضمّنة في بايثون 3.4+
}

# محاولة استيراد importlib.metadata (بايثون 3.8+) أو pkg_resources كبديل
try:
    from importlib import metadata as importlib_metadata  # type: ignore
except Exception:
    importlib_metadata = None
    try:
        import pkg_resources  # type: ignore
    except Exception:
        pkg_resources = None

def get_distribution_version(distribution_name: str | None, import_name: str) -> str:
    """حاول الحصول على رقم الإصدار عبر importlib.metadata أو pkg_resources أو __version__ في الوحدة."""
    if distribution_name and importlib_metadata:
        try:
            return importlib_metadata.version(distribution_name)
        except Exception:
            pass
    if distribution_name and 'pkg_resources' in globals() and pkg_resources is not None:
        try:
            return pkg_resources.get_distribution(distribution_name).version
        except Exception:
            pass
    # أخيراً حاول قراءة __version__ من الوحدة إذا استُورِدت
    try:
        mod = importlib.import_module(import_name)
        return getattr(mod, "__version__", "مدمجة في النظام/غير معروفة")
    except Exception:
        return "غير متوفر"

def check_env(auto_install: bool = False, print_requirements_only: bool = False) -> int:
    print("=" * 60)
    print(" 🔍 جاري فحص بيئة بايثون والاعتمادات المطلوبة...")
    print("=" * 60)

    missing = []
    all_passed = True

    for import_name, (description, distribution_name) in REQUIRED_LIBRARIES.items():
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print(f"[X] {description:<35} | غير مثبتة! ❌")
            all_passed = False
            # استخدم اسم التوزيعة إن وُجِد، وإلا استخدم اسم الاستيراد كافتراض
            pkg_name = distribution_name or import_name
            missing.append(pkg_name)
        else:
            version = get_distribution_version(distribution_name, import_name)
            print(f"[✓] {description:<35} | مثبتة (الإصدار: {version})")

    print("=" * 60)
    if all_passed:
        print("🎉 جميع الاعتمادات مثبتة وجاهزة للعمل بنجاح!")
        print("=" * 60)
        return 0

    # طباعة أمر التثبيت المقترح
    pip_cmd = [sys.executable, "-m", "pip", "install"] + missing
    print("⚠️ بعض المكتبات مفقودة.")
    print("أمر التثبيت المقترح:")
    print("   " + " ".join(pip_cmd))
    if print_requirements_only:
        # طباعة نسخة لصيغة requirements.txt
        print("\nمحتوى مقترح لملف requirements.txt:")
        for pkg in missing:
            print(pkg)
        return 2

    if auto_install and missing:
        print("\nℹ️ بدء التثبيت التلقائي للمكتبات المفقودة...")
        try:
            subprocess.check_call(pip_cmd)
            print("✅ تم تثبيت الحزم بنجاح. يمكنك إعادة تشغيل الفحص للتأكد.")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ فشل التثبيت (رمز خروج {e.returncode}). حاول تشغيل الأمر السابق يدوياً.")
            return e.returncode

    print("للتثبيت اليدوي، شغّل الأمر أعلاه أو أنشئ ملف requirements.txt ثم شغّل:")
    print("   pip install -r requirements.txt")
    print("=" * 60)
    return 1

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="فحص اعتمادات بايثون للمشروع")
    parser.add_argument("--auto-install", action="store_true", help="حاول تثبيت الحزم المفقودة تلقائياً (يتطلب إذن)")
    parser.add_argument("--requirements", action="store_true", help="اطبع محتوى مناسب لملف requirements.txt ثم انتهِ")
    args = parser.parse_args(argv)

    exit_code = check_env(auto_install=args.auto_install, print_requirements_only=args.requirements)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
