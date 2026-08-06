# ATP Internal Auditor Toolkit (Streamlit)

هذا المشروع يحتوي على تطبيق Streamlit بسيط لإنشاء حزمة أدوات مدققي الحسابات الداخلية (ATP) بصيغ Word و ZIP.

التشغيل محليًا:

1. أنشئ بيئة افتراضية:

```bash
python -m venv .venv
source .venv/bin/activate  # على Windows: .\.venv\Scripts\activate
```

2. ثبّت المتطلبات:

```bash
pip install -r requirements.txt
```

3. شغّل التطبيق:

```bash
streamlit run app.py
```

Docker:

```bash
docker build -t atp-toolkit .
docker run -p 8501:8501 atp-toolkit
```

ملاحظات:
- التطبيق يولّد ملفات Word أساسية ثم يضغطها في ملف ZIP للتنزيل.
- تأكد من أن لديك صلاحيات الكتابة على المجلد الذي تشغّل منه التطبيق.
