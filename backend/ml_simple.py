import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import json

print("🧪 مدل یادگیری ماشین ساده با scikit-learn")
print("=" * 50)

# یک مدل ساده برای پیش‌بینی
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

model = LinearRegression()
model.fit(X, y)

print(f"✅ مدل آموزش داده شد")
print(f"   ضرایب: {model.coef_}")
print(f"   عرض از مبدا: {model.intercept_}")

# پیش‌بینی
prediction = model.predict([[6]])
print(f"📊 پیش‌بینی برای 6: {prediction[0]}")

print("\n🎯 می‌توانید از این مدل برای پردازش متن هم استفاده کنید!")
