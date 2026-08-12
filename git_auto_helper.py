#!/usr/bin/env python3
"""
مساعد Git التلقائي (محسّن) — Git Auto Helper v1.1
- دعم: التحقق من git، اكتشاف الفرع، dry-run، فحص وجود تغييرات قبل commit،
  التعامل مع عدم وجود upstream أثناء push، وطباعة مخرجات واضحة باللغـة العربية.
"""

from __future__ import annotations
import subprocess
import sys
import shutil
import argparse


def run_command(command: list[str], description: str, check: bool = True, capture: bool = True):
    """تشغيل أمر نظامي وإرجاع (returncode, stdout, stderr). يطبع ملخصاً موجزاً."""
    cmd_display = " ".join(command)
    print(f"\n🔄 [{description}]")
    print(f"🖥️ الأمر: {cmd_display}")
    try:
        result = subprocess.run(
            command,
            check=check,
            text=True,
            capture_output=capture
        )
        stdout = result.stdout.strip() if result.stdout else ""
        stderr = result.stderr.strip() if result.stderr else ""
        if stdout:
            print(f"✅ stdout:\n{stdout}")
        if stderr:
            # بعض أوامر git تكتب رسائل معلوماتية على stderr (مثل progress)
            print(f"⚠️ stderr:\n{stderr}")
        return result.returncode, stdout, stderr
    except subprocess.CalledProcessError as e:
        stdout = e.stdout.strip() if e.stdout else ""
        stderr = e.stderr.strip() if e.stderr else ""
        if stdout:
            print(f"✅ stdout:\n{stdout}")
        if stderr:
            print(f"❌ stderr:\n{stderr}")
        return e.returncode, stdout, stderr


def check_git_installed() -> bool:
    if shutil.which("git") is None:
        print("❌ خطأ: الأمر 'git' غير مثبت أو غير متوفر في PATH.")
        return False
    code, out, err = run_command(["git", "--version"], "التحقق من نسخة Git", check=True)
    return code == 0


def current_branch() -> str:
    code, out, err = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], "اكتشاف الفرع الحالي", check=False)
    if code == 0 and out:
        return out.strip()
    return "main"


def has_working_changes() -> bool:
    code, out, err = run_command(["git", "status", "--porcelain"], "التحقق من وجود تغييرات (porcelain)", check=False)
    return bool(out.strip())


def ensure_upstream(branch: str) -> bool:
    # حاول استعلام upstream، إن لم يوجد نضعه تلقائياً عند push
    code, out, err = run_command(["git", "rev-parse", "--abbrev-ref", f"{branch}@{{u}}"], "التحقق من وجود upstream للفرع", check=False)
    return code == 0


def git_workflow_helper(branch: str | None = None, do_push: bool = True, dry_run: bool = False):
    print("=" * 60)
    print(" 🛠️ مساعد أدوات Git و GitHub (محسّن) — تفاعلي")
    print("=" * 60)

    if not check_git_installed():
        return

    # 1. حالة المستودع
    run_command(["git", "status"], "فحص حالة المستودع (git status)")

    # اكتشاف الفرع أو استخدام الفرع الممرر
    branch_name = branch or current_branch()
    print(f"\nℹ️ الفرع المستخدم حالياً: {branch_name}")

    # هل هناك تغييرات في الشجرة؟
    if not has_working_changes():
        print("\nℹ️ لا توجد تغييرات للعمل عليها (لم يتم العثور على ملفات جديدة/معدّلة/محذوفة).")
        if do_push:
            print("ملاحظة: لا يوجد شيء لتوثيقه، لكن يمكنك محاولة سحب آخر التغييرات أو التحقق من الفرع.")
        return

    # سؤال التأكيد العام
    user_choice = input("\nهل ترغب في إضافة كافة التعديلات وتوثيقها ورفعها الآن؟ (y/n): ")
    if user_choice.lower() not in ['y', 'yes']:
        print("تم إيقاف العملية بناءً على طلبك.")
        return

    commit_msg = input("أدخل رسالة التوثيق (Commit Message). اتركها فارغة لرسالة افتراضية: ").strip()
    if not commit_msg:
        commit_msg = "update: Automatic commit via git_auto_helper"

    add_cmd = ["git", "add", "-A"]
    commit_cmd = ["git", "commit", "-m", commit_msg]

    print("\n🔎 المعاينة:")
    print(" - أمر الإضافة:", " ".join(add_cmd))
    print(" - أمر التوثيق:", " ".join(commit_cmd))
    if do_push:
        print(" - سيتم محاولة الرفع (push) إلى 'origin' على الفرع:", branch_name)

    if dry_run:
        print("\n🛑 [وضع المعاينة] لم يتم تنفيذ أي أوامر. للخروج من المعاينة قم بإزالة --dry-run.")
        return

    # تنفيذ git add
    code, out, err = run_command(add_cmd, "تجهيز كافة الملفات (git add -A)")
    if code != 0:
        print("❌ فشل أثناء git add — تحقق من المخرجات أعلاه.")
        return

    # التحقق من وجود شيء للتوثيق بعد git add
    if not has_working_changes():
        # قد يحدث أن git add لم يغيّر شيئًا (مثلاً كل التغييرات مدمجة سابقاً)
        print("\nℹ️ بعد git add لا يوجد شيء جديد لتوثيقه (nothing to commit).")
        return

    # تنفيذ git commit
    code, out, err = run_command(commit_cmd, "تسجيل التغييرات محلياً (git commit)", check=False)
    if code != 0:
        # تعامل مع حالة "nothing to commit" أو أخطاء أخرى
        if "nothing to commit" in (out + err).lower():
            print("⚠️ لا يوجد شيء لتوثيقه — ربما تم توثيق التغييرات بالفعل.")
            return
        print("❌ فشل أثناء git commit — تحقق من المخرجات أعلاه.")
        return

    # تنفيذ git push إذا طُلب ذلك
    if do_push:
        if not ensure_upstream(branch_name):
            print(f"⚠️ الفرع {branch_name} لا يحتوي على upstream مضبوط. سيتم ضبطه تلقائياً عند push.")
            push_cmd = ["git", "push", "--set-upstream", "origin", branch_name]
        else:
            push_cmd = ["git", "push", "origin", branch_name]

        code, out, err = run_command(push_cmd, f"رفع التحديثات إلى المستودع البعيد (git push {'--set-upstream' if '--set-upstream' in push_cmd else ''})", check=False)
        if code != 0:
            print("❌ فشل أثناء git push — تحقق من رسائل الخطأ (قد تحتاج لإعداد بيانات اعتماد أو حل تعارضات).")
            return

    print("\n✅ تمت العملية بنجاح! بإمكانك الآن تنفيذ 'git status' أو 'git log' لمراجعة التاريخ.")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="مساعد Git التلقائي المحسّن")
    parser.add_argument("--branch", "-b", type=str, help="اسم الفرع الذي تريد العمل عليه (افتراضي: الفرع الحالي)")
    parser.add_argument("--no-push", action="store_true", help="عدم تنفيذ git push بعد commit")
    parser.add_argument("--dry-run", action="store_true", help="عرض الأوامر دون تنفيذها")
    args = parser.parse_args(argv)

    git_workflow_helper(branch=args.branch, do_push=not args.no_push, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
