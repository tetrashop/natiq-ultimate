"""
پایگاه دانش natiq-ultimate
شامل مفاهیم هوش مصنوعی، یادگیری ماشین، شبکه عصبی و ...
"""
import json
import random
from datetime import datetime

class KnowledgeGraph:
    """گراف دانش با مفاهیم و روابط"""
    
    def __init__(self):
        self.graph = self._initialize_knowledge()
        self.cache = {}
        print(f"📚 Knowledge graph initialized with {len(self.graph)} concepts")
    
    def _initialize_knowledge(self):
        """ایجاد پایگاه دانش اولیه"""
        return {
            "هوش مصنوعی": {
                "definition": "شاخه‌ای از علوم کامپیوتر که به ساخت ماشین‌های هوشمند می‌پردازد",
                "category": "fundamental",
                "importance": "very_high",
                "examples": ["یادگیری ماشین", "پردازش زبان طبیعی", "بینایی کامپیوتر", "رباتیک"],
                "relations": ["یادگیری_ماشین", "شبکه_عصبی", "الگوریتم"],
                "sources": ["wikipedia", "academic_papers"],
                "last_updated": datetime.now().isoformat()
            },
            "یادگیری ماشین": {
                "definition": "توانایی سیستم‌ها برای یادگیری از داده بدون برنامه‌نویسی صریح",
                "category": "subfield",
                "importance": "high",
                "examples": ["شبکه عصبی", "درخت تصمیم", "ماشین بردار پشتیبان", "خوشه‌بندی"],
                "relations": ["هوش_مصنوعی", "داده_کاوی", "پیش‌بینی"],
                "applications": ["تشخیص تصویر", "پیش‌بینی قیمت", "تشخیص تقلب", "پیشنهاد محصول"],
                "sources": ["wikipedia", "research_papers"],
                "last_updated": datetime.now().isoformat()
            },
            "شبکه عصبی": {
                "definition": "مدل محاسباتی الهام گرفته از شبکه عصبی مغز",
                "category": "algorithm",
                "importance": "high",
                "examples": ["پرسپترون", "شبکه کانولوشن", "شبکه بازگشتی", "شبکه عصبی عمیق"],
                "layers": ["لایه ورودی", "لایه پنهان", "لایه خروجی"],
                "relations": ["یادگیری_عمیق", "پردازش_تصویر", "پردازش_زبان"],
                "sources": ["academic_papers", "technical_docs"],
                "last_updated": datetime.now().isoformat()
            },
            "یادگیری عمیق": {
                "definition": "زیرشاخه‌ای از یادگیری ماشین که از شبکه‌های عصبی با لایه‌های متعدد استفاده می‌کند",
                "category": "advanced",
                "importance": "high",
                "examples": ["شبکه عصبی کانولوشن", "شبکه عصبی بازگشتی", "مبدل‌ها"],
                "applications": ["تشخیص گفتار", "ترجمه ماشینی", "تولید متن", "تولید تصویر"],
                "relations": ["شبکه_عصبی", "پردازش_زبان_طبیعی", "بینایی_کامپیوتر"],
                "sources": ["research_papers", "conference_proceedings"],
                "last_updated": datetime.now().isoformat()
            },
            "پایتون": {
                "definition": "زبان برنامه‌نویسی سطح بالا، مفسری و همه‌منظوره",
                "category": "tool",
                "importance": "very_high",
                "examples": ["تنسورفلو", "پایتورچ", "scikit-learn", "numpy", "pandas"],
                "ai_libraries": ["tensorflow", "pytorch", "keras", "scikit-learn", "nltk"],
                "relations": ["هوش_مصنوعی", "یادگیری_ماشین", "داده_کاوی"],
                "sources": ["official_docs", "community"],
                "last_updated": datetime.now().isoformat()
            },
            "داده کاوی": {
                "definition": "فرآیند کشف الگوها و دانش از داده‌های بزرگ",
                "category": "process",
                "importance": "high",
                "steps": ["پاکسازی داده", "تبدیل داده", "کاوش داده", "ارزیابی الگو"],
                "techniques": ["خوشه‌بندی", "قانون‌یابی", "طبقه‌بندی", "رگرسیون"],
                "relations": ["یادگیری_ماشین", "تحلیل_داده", "هوش_تجاری"],
                "sources": ["academic_books", "technical_guides"],
                "last_updated": datetime.now().isoformat()
            },
            "الگوریتم": {
                "definition": "مجموعه‌ای از دستورالعمل‌های مرحله به مرحله برای حل یک مسئله",
                "category": "fundamental",
                "importance": "high",
                "types": ["ترتیبی", "بازگشتی", "حریصانه", "تقسیم و غلبه", "پویا"],
                "examples": ["مرتب‌سازی سریع", "جستجوی دودویی", "دایجسترا", "درخت پوشا"],
                "relations": ["برنامه‌نویسی", "ساختمان_داده", "پیچیدگی_زمانی"],
                "sources": ["computer_science_textbooks"],
                "last_updated": datetime.now().isoformat()
            },
            "پردازش زبان طبیعی": {
                "definition": "زمینه‌ای از هوش مصنوعی که به تعامل بین کامپیوتر و زبان انسان می‌پردازد",
                "category": "application",
                "importance": "high",
                "tasks": ["تجزیه‌گر نحوی", "تشخیص موجودیت‌ها", "تحلیل احساسات", "ترجمه ماشینی"],
                "models": ["BERT", "GPT", "Transformer", "LSTM"],
                "relations": ["هوش_مصنوعی", "یادگیری_ماشین", "یادگیری_عمیق"],
                "sources": ["research_papers", "nlp_books"],
                "last_updated": datetime.now().isoformat()
            },
            "بینایی کامپیوتر": {
                "definition": "زمینه‌ای از هوش مصنوعی که کامپیوترها را قادر به درک و تفسیر دنیای بصری می‌سازد",
                "category": "application",
                "importance": "high",
                "tasks": ["تشخیص اشیا", "طبقه‌بندی تصویر", "بخش‌بندی معنایی", "تشخیص چهره"],
                "models": ["CNN", "YOLO", "ResNet", "Vision Transformer"],
                "relations": ["یادگیری_عمیق", "شبکه_عصبی", "پردازش_تصویر"],
                "sources": ["computer_vision_papers", "conferences"],
                "last_updated": datetime.now().isoformat()
            },
            "رباتیک": {
                "definition": "شاخه‌ای از مهندسی و علوم که به طراحی، ساخت و بهره‌برداری از ربات‌ها می‌پردازد",
                "category": "application",
                "importance": "medium",
                "components": ["حسگرها", "عملگرها", "کنترل‌گر", "پردازشگر"],
                "types": ["صنعتی", "خدماتی", "پزشکی", "نظامی"],
                "relations": ["هوش_مصنوعی", "کنترل_خودکار", "مکاترونیک"],
                "sources": ["robotics_journals", "engineering_books"],
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def search(self, concept):
        """جستجوی مفهوم در پایگاه دانش"""
        # نرمال‌سازی مفهوم
        normalized = concept.replace(" ", "_")
        
        # جستجوی مستقیم
        if normalized in self.graph:
            return {
                "found": True,
                "concept": concept,
                "data": self.graph[normalized],
                "source": "knowledge_graph",
                "confidence": 0.95
            }
        
        # جستجوی مشابه
        similar = []
        for known_concept in self.graph:
            if concept.lower() in known_concept.lower() or known_concept.lower() in concept.lower():
                similar.append(known_concept)
        
        if similar:
            return {
                "found": True,
                "concept": similar[0],
                "data": self.graph[similar[0]],
                "similar_found": similar,
                "source": "similarity_match",
                "confidence": 0.7
            }
        
        # جستجوی کلمه‌ای
        words = concept.split()
        for word in words:
            if len(word) > 2:  # فقط کلمات معنی‌دار
                for known_concept in self.graph:
                    if word.lower() in known_concept.lower():
                        return {
                            "found": True,
                            "concept": known_concept,
                            "data": self.graph[known_concept],
                            "matched_word": word,
                            "source": "word_match",
                            "confidence": 0.6
                        }
        
        return {
            "found": False,
            "concept": concept,
            "message": "مفهوم در پایگاه دانش یافت نشد",
            "suggestions": list(self.graph.keys())[:3],
            "confidence": 0.0
        }
    
    def get_related(self, concept, max_results=5):
        """دریافت مفاهیم مرتبط"""
        if concept not in self.graph:
            return []
        
        related = []
        data = self.graph[concept]
        
        # روابط مستقیم
        if 'relations' in data:
            for rel in data['relations']:
                if rel in self.graph:
                    related.append(rel)
        
        # روابط معکوس (چه مفاهیمی به این مفهوم اشاره دارند)
        for other_concept, other_data in self.graph.items():
            if 'relations' in other_data and concept in other_data['relations']:
                related.append(other_concept)
        
        # حذف تکراری‌ها و محدود کردن نتایج
        related = list(dict.fromkeys(related))
        return related[:max_results]
    
    def get_categories(self):
        """دریافت دسته‌بندی‌های موجود"""
        categories = {}
        for concept, data in self.graph.items():
            category = data.get('category', 'unknown')
            if category not in categories:
                categories[category] = []
            categories[category].append(concept)
        
        return categories
    
    def add_concept(self, concept, data):
        """افزودن مفهوم جدید به پایگاه دانش"""
        normalized = concept.replace(" ", "_")
        if normalized not in self.graph:
            data['last_updated'] = datetime.now().isoformat()
            data['added_by'] = "user_interaction"
            self.graph[normalized] = data
            return True
        return False
    
    def export(self):
        """خروجی کل پایگاه دانش"""
        return {
            "total_concepts": len(self.graph),
            "concepts": list(self.graph.keys()),
            "categories": self.get_categories(),
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
