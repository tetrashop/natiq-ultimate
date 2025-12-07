"""
سیستم عصبی natiq-ultimate
پردازش زبان طبیعی و تحلیل معنایی
"""
import re
import math
import random
import hashlib
from datetime import datetime

class NeuralSystem:
    """سیستم پردازش عصبی"""
    
    def __init__(self):
        self.word_vectors = self._initialize_embeddings()
        self.intent_patterns = self._initialize_intents()
        self.entity_patterns = self._initialize_entities()
        self.cache = {}
        print("🧠 Neural system initialized")
    
    def _initialize_embeddings(self):
        """ایجاد بردارهای کلمات (شبیه‌سازی شده)"""
        words = [
            "هوش", "مصنوعی", "یادگیری", "ماشین", "داده", "الگوریتم",
            "شبکه", "عصبی", "عمیق", "پایتون", "برنامه", "نویسی",
            "تحلیل", "پردازش", "زبان", "طبیعی", "بینایی", "کامپیوتر",
            "ربات", "رباتیک", "داده‌کاوی", "کاوش", "الگو", "شناسایی",
            "پیش‌بینی", "طبقه‌بندی", "خوشه‌بندی", "بازگشتی", "کانولوشن"
        ]
        
        vectors = {}
        for word in words:
            # بردار 10 بعدی شبیه‌سازی شده
            vector = [random.random() for _ in range(10)]
            norm = math.sqrt(sum(x*x for x in vector))
            if norm > 0:
                vector = [x/norm for x in vector]
            vectors[word] = vector
        
        return vectors
    
    def _initialize_intents(self):
        """الگوهای تشخیص هدف سوال"""
        return {
            "definition": {
                "patterns": ["چیست", "چیه", "تعریف", "منظور", "معنی", "چه"],
                "keywords": ["تعریف", "معنی", "مفهوم"],
                "weight": 1.0
            },
            "comparison": {
                "patterns": ["تفاوت", "فرق", "مقایسه", "اختلاف", "کدام بهتر"],
                "keywords": ["مقایسه", "تفاوت", "فرق"],
                "weight": 0.9
            },
            "causal": {
                "patterns": ["چرا", "علت", "دلیل", "چرایی", "سبب", "چگونه اتفاق"],
                "keywords": ["علت", "دلیل", "چرا"],
                "weight": 0.8
            },
            "howto": {
                "patterns": ["چگونه", "چطور", "روش", "طریق", "مراحل", "چکار کنم"],
                "keywords": ["چگونه", "روش", "طریق"],
                "weight": 0.85
            },
            "application": {
                "patterns": ["کاربرد", "استفاده", "فواید", "مزایا", "منافع", "کجا بکار"],
                "keywords": ["کاربرد", "استفاده", "مزایا"],
                "weight": 0.75
            },
            "component": {
                "patterns": ["اجزا", "قسمت‌ها", "مولفه‌ها", "بخش‌ها", "عناصر"],
                "keywords": ["اجزا", "بخش", "مولفه"],
                "weight": 0.7
            },
            "example": {
                "patterns": ["مثال", "نمونه", "مورد", "کاربرد عملی"],
                "keywords": ["مثال", "نمونه"],
                "weight": 0.65
            }
        }
    
    def _initialize_entities(self):
        """الگوهای تشخیص موجودیت‌ها"""
        return {
            "CONCEPT": ["هوش مصنوعی", "یادگیری ماشین", "شبکه عصبی", "یادگیری عمیق",
                       "پایتون", "داده کاوی", "الگوریتم", "پردازش زبان طبیعی",
                       "بینایی کامپیوتر", "رباتیک"],
            "TECHNOLOGY": ["تنسورفلو", "پایتورچ", "keras", "scikit-learn", "numpy", "pandas"],
            "ALGORITHM": ["درخت تصمیم", "ماشین بردار پشتیبان", "خوشه‌بندی", "رگرسیون",
                         "شبکه کانولوشن", "شبکه بازگشتی", "پرسپترون"],
            "PROCESS": ["پیش‌بینی", "طبقه‌بندی", "تشخیص", "تحلیل", "بهینه‌سازی"]
        }
    
    def analyze(self, text):
        """تحلیل کامل متن با سیستم عصبی"""
        text_lower = text.lower()
        
        # 1. تشخیص هدف
        intent = self._detect_intent(text_lower)
        
        # 2. استخراج موجودیت‌ها
        entities = self._extract_entities(text)
        
        # 3. استخراج مفاهیم
        concepts = self._extract_concepts(text)
        
        # 4. محاسبه embedding
        embedding = self._get_sentence_embedding(text)
        
        # 5. محاسبه اطمینان کلی
        confidence = self._calculate_confidence(intent, entities, concepts)
        
        return {
            "text": text,
            "intent": intent["type"],
            "intent_confidence": intent["confidence"],
            "intent_details": intent,
            "entities": entities,
            "concepts": concepts,
            "embedding": embedding[:5],  # فقط 5 بعد اول
            "confidence": confidence,
            "word_count": len(text.split()),
            "has_question": "؟" in text or "?" in text,
            "timestamp": datetime.now().isoformat(),
            "neural_version": "1.0.0"
        }
    
    def _detect_intent(self, text):
        """تشخیص هدف سوال"""
        scores = {}
        
        for intent_type, intent_data in self.intent_patterns.items():
            score = 0
            
            # بررسی الگوها
            for pattern in intent_data["patterns"]:
                if pattern in text:
                    score += 1
            
            # بررسی کلمات کلیدی
            for keyword in intent_data["keywords"]:
                if keyword in text:
                    score += 2
            
            # اعمال وزن
            scores[intent_type] = (score * intent_data["weight"]) / 10
        
        # نرمال‌سازی امتیازات
        max_score = max(scores.values()) if scores else 0
        if max_score > 0:
            for intent_type in scores:
                scores[intent_type] = min(scores[intent_type] / max_score, 1.0)
        
        # انتخاب هدف اصلی
        primary_intent = max(scores.items(), key=lambda x: x[1]) if scores else ("general", 0.5)
        
        return {
            "type": primary_intent[0],
            "confidence": round(primary_intent[1], 2),
            "all_scores": scores,
            "details": self.intent_patterns.get(primary_intent[0], {})
        }
    
    def _extract_entities(self, text):
        """استخراج موجودیت‌ها از متن"""
        entities = []
        text_lower = text.lower()
        
        for entity_type, entity_list in self.entity_patterns.items():
            for entity in entity_list:
                if entity.lower() in text_lower:
                    # پیدا کردن موقعیت
                    start = text_lower.find(entity.lower())
                    end = start + len(entity)
                    
                    entities.append({
                        "entity": entity,
                        "type": entity_type,
                        "start": start,
                        "end": end,
                        "confidence": random.uniform(0.7, 0.95)  # شبیه‌سازی شده
                    })
        
        # استخراج کلمات کلیدی دیگر
        words = text.split()
        for i, word in enumerate(words):
            if len(word) > 3 and word in self.word_vectors:
                entities.append({
                    "entity": word,
                    "type": "KEYWORD",
                    "start": i,
                    "end": i + 1,
                    "confidence": 0.6
                })
        
        return entities
    
    def _extract_concepts(self, text):
        """استخراج مفاهیم از متن"""
        concepts = []
        text_lower = text.lower()
        
        # لیست مفاهیم شناخته شده
        known_concepts = [
            "هوش مصنوعی", "یادگیری ماشین", "شبکه عصبی", "یادگیری عمیق",
            "پایتون", "داده کاوی", "الگوریتم", "پردازش زبان طبیعی",
            "بینایی کامپیوتر", "رباتیک", "تنسورفلو", "پایتورچ"
        ]
        
        for concept in known_concepts:
            if concept.lower() in text_lower:
                concepts.append(concept)
        
        # استخراج کلمات تخصصی
        for word in text.split():
            if word in self.word_vectors and len(word) > 2:
                # محاسبه شباهت با مفاهیم شناخته شده
                similarity = self._calculate_word_similarity(word, known_concepts)
                if similarity > 0.5:
                    concepts.append(word)
        
        # حذف تکراری‌ها
        return list(dict.fromkeys(concepts))
    
    def _get_sentence_embedding(self, text):
        """محاسبه embedding جمله"""
        words = text.split()
        vectors = []
        
        for word in words:
            if word in self.word_vectors:
                vectors.append(self.word_vectors[word])
            else:
                # بردار پیش‌فرض برای کلمات ناشناخته
                vec = [random.random() for _ in range(10)]
                norm = math.sqrt(sum(x*x for x in vec))
                if norm > 0:
                    vec = [x/norm for x in vec]
                vectors.append(vec)
        
        if vectors:
            # میانگین بردارها
            result = [0.0] * 10
            for vec in vectors:
                for i in range(10):
                    result[i] += vec[i]
            return [x/len(vectors) for x in result]
        
        return [0.0] * 10
    
    def _calculate_word_similarity(self, word1, word2_list):
        """محاسبه شباهت بین کلمه و لیست کلمات"""
        if word1 not in self.word_vectors:
            return 0.0
        
        max_similarity = 0.0
        vec1 = self.word_vectors[word1]
        
        for word2 in word2_list:
            for w in word2.split():
                if w in self.word_vectors:
                    vec2 = self.word_vectors[w]
                    similarity = self._cosine_similarity(vec1, vec2)
                    max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _cosine_similarity(self, vec1, vec2):
        """محاسبه شباهت کسینوسی"""
        dot_product = sum(a*b for a,b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a*a for a in vec1))
        norm2 = math.sqrt(sum(b*b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_confidence(self, intent, entities, concepts):
        """محاسبه اطمینان کلی تحلیل"""
        base_confidence = intent["confidence"]
        
        # افزایش اطمینان بر اساس موجودیت‌ها
        if entities:
            base_confidence += min(len(entities) * 0.05, 0.2)
        
        # افزایش اطمینان بر اساس مفاهیم
        if concepts:
            base_confidence += min(len(concepts) * 0.1, 0.3)
        
        # محدود کردن به بازه [0, 1]
        return min(max(base_confidence, 0.1), 0.95)
    
    def semantic_search(self, query, documents, top_k=3):
        """جستجوی معنایی (شبیه‌سازی شده)"""
        # در نسخه واقعی، این بخش با مدل embedding پیاده‌سازی می‌شود
        results = []
        
        for i, doc in enumerate(documents[:10]):  # محدود کردن برای عملکرد
            # شباهت ساده (شبیه‌سازی شده)
            similarity = random.uniform(0.1, 0.9)
            
            results.append({
                "document": doc[:100] + "..." if len(doc) > 100 else doc,
                "similarity": round(similarity, 2),
                "index": i
            })
        
        # مرتب‌سازی بر اساس شباهت
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def cache_key(self, text):
        """ایجاد کلید کش"""
        return hashlib.md5(text.encode()).hexdigest()[:16]
