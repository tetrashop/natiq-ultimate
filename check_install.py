import sys
import platform

print("🔍 بررسی نصب کتابخانه‌ها")
print("=" * 50)

print(f"پایتون: {sys.version}")
print(f"سیستم: {platform.system()} {platform.machine()}")

libs_to_check = [
    ('torch', 'PyTorch'),
    ('tensorflow', 'TensorFlow'),
    ('transformers', 'Transformers'),
    ('numpy', 'NumPy'),
]

for module, name in libs_to_check:
    try:
        m = __import__(module)
        version = getattr(m, '__version__', 'unknown')
        print(f"✅ {name}: {version}")
    except ImportError:
        print(f"❌ {name}: نصب نیست")

print("\n🧪 تست عملی:")
try:
    # تست ساده tensorflow یا torch
    try:
        import torch
        x = torch.tensor([1, 2, 3])
        print(f"PyTorch تانسور تست: {x}")
    except:
        import tensorflow as tf
        x = tf.constant([1, 2, 3])
        print(f"TensorFlow تانسور تست: {x}")
except Exception as e:
    print(f"⚠️ تست ناموفق: {e}")

print("\n🎯 توصیه:")
print("اگر PyTorch نصب نیست، دستور زیر را اجرا کنید:")
print("pip install torch --index-url https://download.pytorch.org/whl/cpu")
