import tensorflow as tf
from transformers import pipeline, AutoTokenizer, TFAutoModelForSeq2SeqLM

print(f"TensorFlow نسخه: {tf.__version__}")

# استفاده از مدل با TensorFlow backend
model_name = "google/flan-t5-small"
print(f"بارگذاری مدل: {model_name}")

try:
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name, from_pt=False)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # پردازش سوال
    question = "هوش مصنوعی چیست؟"
    inputs = tokenizer(question, return_tensors="tf")
    outputs = model.generate(**inputs, max_length=100)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"سوال: {question}")
    print(f"پاسخ: {answer}")
except Exception as e:
    print(f"خطا: {e}")
    print("شاید نیاز به دانلود مدل دارید...")
