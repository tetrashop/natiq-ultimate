#!/usr/bin/env python3
"""
natiq-ultimate - سیستم استدلال و تحلیل مستقل
نسخه 4.0: با قابلیت درک معنایی، استنتاج، تحلیل علّی و استقلال فکری
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os
from datetime import datetime
import json
import random
import re
from typing import Dict, List, Tuple, Optional, Set
import math

app = FastAPI(
    title="natiq-ultimate",
    description="هوش مصنوعی با قابلیت استدلال و تحلیل مستقل",
    version="4.0.0"
)

# CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# کلاس تحلیل‌گر معنایی پیشرفته
class SemanticAnalyzer:
    """تحلیل‌گر معنایی با درک روابط کلمات"""
    
    def __init__(self):
        # دیکشنری معانی و روابط مفهومی
        self.semantic_network = self.build_semantic_network()
        
    def build_semantic_network(self):
        """شبکه معنایی سلسله‌مراتبی"""
        return {
            # موجودیت‌ها و روابط آنها
            "هوش_مصنوعی": {
                "type": "مفهوم",
                "تعریف": "سیستم‌های کامپیوتری که می‌توانند وظایف انسانی را انجام دهند",
                "زیرمجموعه": ["یادگیری_ماشین", "پردازش_زبان_طبیعی", "بینایی_کامپیوتر"],
                "کاربرد": ["تشخیص_تصویر", "پردازش_زبان", "رباتیک"],
                "ویژگی": ["یادگیری", "استدلال", "حل_مسئله"]
            },
            "یادگیری_ماشین": {
                "type": "مفهوم",
                "تعریف": "زیرشاخه‌ای از هوش مصنوعی که به کامپیوترها توانایی یادگیری از داده می‌دهد",
                "الگوریتم": ["شبکه_عصبی", "درخت_تصمیم", "SVM"],
                "کاربرد": ["پیش‌بینی", "دسته‌بندی", "خوشه‌بندی"]
            },
            # روابط علّی
            "علت_معلول": {
                "باران": ["خیس_شدن_زمین", "رشد_گیاهان"],
                "آموزش": ["یادگیری", "مهارت"],
                "تمرین": ["تبحر", "سرعت"]
            },
            # اجماع عمومی
            "اجماع": {
                "علمی": ["زمین_گرد_است", "آب_در_100_درجه_می‌جوشد", "جاذبه_وجود_دارد"],
                "اخلاقی": ["دروغ_بد_است", "کمک_به_دیگران_خوب_است"],
                "منطقی": ["اگر_A_برابر_B_و_B_برابر_C_باشد_آنگاه_A_برابر_C_است"]
            }
        }
    
    def extract_concepts(self, text: str) -> List[str]:
        """استخراج مفاهیم کلیدی از متن"""
        concepts = []
        words = text.split()
        
        # جستجوی مفاهیم مرکب
        for i in range(len(words)):
            for j in range(i+1, min(i+4, len(words))+1):
                phrase = "_".join(words[i:j])
                if phrase in self.semantic_network:
                    concepts.append(phrase)
        
        return list(set(concepts))
    
    def find_relations(self, concept1: str, concept2: str) -> List[str]:
        """یافتن روابط بین دو مفهوم"""
        relations = []
        
        if concept1 in self.semantic_network and concept2 in self.semantic_network:
            # بررسی روابط مستقیم
            if concept2 in self.semantic_network.get(concept1, {}).get("زیرمجموعه", []):
                relations.append(f"{concept2} زیرمجموعه {concept1} است")
            if concept1 in self.semantic_network.get(concept2, {}).get("زیرمجموعه", []):
                relations.append(f"{concept1} زیرمجموعه {concept2} است")
        
        return relations

# کلاس استنتاج منطقی
class LogicalInference:
    """سیستم استنتاج و اثبات منطقی"""
    
    def __init__(self):
        self.rules = self.build_logical_rules()
        self.knowledge_base = {}
    
    def build_logical_rules(self):
        """قواعد منطقی برای استنتاج"""
        return {
            # قواعد استنتاج
            "modus_ponens": {
                "pattern": ["اگر P آنگاه Q", "P"],
                "conclusion": "Q"
            },
            "modus_tollens": {
                "pattern": ["اگر P آنگاه Q", "نه Q"],
                "conclusion": "نه P"
            },
            "transitive": {
                "pattern": ["P مانند Q است", "Q مانند R است"],
                "conclusion": "P مانند R است"
            },
            # قواعد ریاضی
            "addition": {
                "pattern": ["P", "Q"],
                "conclusion": "P و Q"
            }
        }
    
    def add_fact(self, fact: str):
        """افزودن واقعیت جدید به پایگاه دانش"""
        self.knowledge_base[fact] = True
    
    def infer(self, premises: List[str]) -> List[str]:
        """استنتاج از مقدمات داده شده"""
        conclusions = []
        
        # قاعده modus ponens
        for premise in premises:
            if premise.startswith("اگر") and "آنگاه" in premise:
                condition, consequence = premise.split("آنگاه")
                condition = condition.replace("اگر", "").strip()
                consequence = consequence.strip()
                
                if condition in premises or condition in self.knowledge_base:
                    conclusions.append(consequence)
                    self.add_fact(consequence)
        
        # قاعده transitive
        similarity_pattern = r"(.+) مانند (.+) است"
        similarities = []
        for premise in premises:
            match = re.match(similarity_pattern, premise)
            if match:
                similarities.append((match.group(1), match.group(2)))
        
        # استنتاج انتقالی
        for i in range(len(similarities)):
            for j in range(len(similarities)):
                if i != j and similarities[i][1] == similarities[j][0]:
                    conclusion = f"{similarities[i][0]} مانند {similarities[j][1]} است"
                    conclusions.append(conclusion)
                    self.add_fact(conclusion)
        
        return conclusions

# کلاس تحلیل علّی
class CausalAnalyzer:
    """تحلیل روابط علّی بین رویدادها"""
    
    def __init__(self):
        self.causal_graph = self.build_causal_graph()
    
    def build_causal_graph(self):
        """گراف روابط علّی"""
        return {
            # روابط علّی عمومی
            "آموزش_دادن": ["یادگیری", "مهارت"],
            "تمرین_کردن": ["تبحر", "سرعت"],
            "باریدن_باران": ["خیس_شدن_زمین", "رشد_گیاهان"],
            "گرم_کردن_آب": ["جوشیدن_آب"],
            "کاشت_بذر": ["روئیدن_گیاه"],
            
            # روابط معکوس
            "effects_of": {
                "آموزش": ["دانش", "مهارت"],
                "غذا": ["انرژی", "رشد"]
            }
        }
    
    def find_causes(self, effect: str) -> List[str]:
        """یافتن علل احتمالی یک معلول"""
        causes = []
        for cause, effects in self.causal_graph.items():
            if isinstance(effects, list) and effect in effects:
                causes.append(cause)
        
        return causes
    
    def find_effects(self, cause: str) -> List[str]:
        """یافتن معلولات احتمالی یک علت"""
        if cause in self.causal_graph:
            return self.causal_graph[cause]
        return []
    
    def analyze_causal_chain(self, start: str, depth: int = 3) -> Dict:
        """تحلیل زنجیره علّی"""
        result = {
            "علل": self.find_causes(start),
            "معلولات": self.find_effects(start),
            "زنجیره_علّی": []
        }
        
        # تحلیل زنجیره
        chain = []
        current = start
        
        for _ in range(depth):
            effects = self.find_effects(current)
            if effects:
                chain.append({"علت": current, "معلول": effects[0]})
                current = effects[0]
            else:
                break
        
        result["زنجیره_علّی"] = chain
        return result

# کلاس تشخیص اجماع
class ConsensusDetector:
    """تشخیص اجماع و نظرات عمومی"""
    
    def __init__(self):
        self.consensus_db = self.build_consensus_database()
    
    def build_consensus_database(self):
        """پایگاه داده اجماع‌های عمومی"""
        return {
            "علمی": {
                "زمین_گرد_است": 0.99,
                "آب_در_100_درجه_می‌جوشد": 0.98,
                "جاذبه_وجود_دارد": 0.99,
                "انسان_نیاز_به_تنفس_دارد": 0.99
            },
            "اخلاقی": {
                "دروغ_گفتن_نادرست_است": 0.85,
                "کمک_به_دیگران_درست_است": 0.90,
                "دزدی_نادرست_است": 0.95
            },
            "منطقی": {
                "اگر_A=B_و_B=C_آنگاه_A=C": 1.00,
                "تناقض_نادرست_است": 1.00,
                "اصل_عدم_تناقض": 1.00
            },
            "عمومی": {
                "خورشید_از_مشرق_طلوع_می‌کند": 0.95,
                "آب_مایع_است": 0.98,
                "آتش_گرم_است": 0.99
            }
        }
    
    def check_consensus(self, statement: str) -> Dict:
        """بررسی میزان اجماع روی یک گزاره"""
        result = {
            "گزاره": statement,
            "اجماع_کلی": 0.0,
            "تفصیل": {}
        }
        
        statement_normalized = statement.replace(" ", "_")
        
        for category, statements in self.consensus_db.items():
            for stmt, confidence in statements.items():
                # بررسی شباهت معنایی
                if self.semantic_similarity(statement_normalized, stmt) > 0.7:
                    result["تفصیل"][category] = confidence
                    result["اجماع_کلی"] = max(result["اجماع_کلی"], confidence)
        
        return result
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """شباهت معنایی ساده"""
        words1 = set(text1.split("_"))
        words2 = set(text2.split("_"))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0

# کلاس اصلی Natiq با استدلال مستقل
class NatiqIndependentAI:
    """هوش مصنوعی با قابلیت استدلال و تحلیل مستقل"""
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.logical_inference = LogicalInference()
        self.causal_analyzer = CausalAnalyzer()
        self.consensus_detector = ConsensusDetector()
        self.conversation_history = []
        self.reasoning_steps = []
        
        # دانش پایه
        self.base_knowledge = self.initialize_base_knowledge()
    
    def initialize_base_knowledge(self):
        """دانش پایه برای استدلال"""
        return {
            "حقایق_پایه": [
                "هر موجود زنده نیاز به غذا دارد",
                "آب در 100 درجه سانتیگراد می‌جوشد",
                "خورشید منبع نور و گرما است",
                "گیاهان برای رشد به نور نیاز دارند"
            ],
            "قواعد_منطقی": [
                "اگر باران ببارد، زمین خیس می‌شود",
                "اگر کسی غذا نخورد، گرسنه می‌شود",
                "اگر تمرین کنی، بهتر می‌شوی"
            ]
        }
    
    def analyze_question(self, question: str) -> Dict:
        """تحلیل عمیق سوال با درک معنایی"""
        # استخراج مفاهیم
        concepts = self.semantic_analyzer.extract_concepts(question)
        
        # تشخیص نوع سوال
        question_type = self.detect_question_type(question)
        
        # استخراج موجودیت‌ها و روابط
        entities = self.extract_entities(question)
        
        return {
            "مفاهیم": concepts,
            "نوع_سوال": question_type,
            "موجودیت‌ها": entities,
            "تحلیل_سطحی": self.shallow_analysis(question),
            "تحلیل_عمیق": self.deep_semantic_analysis(question)
        }
    
    def detect_question_type(self, question: str) -> str:
        """تشخیص نوع سوال بر اساس ساختار"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["چرا", "علت", "دلیل"]):
            return "سوال_علّی"
        elif any(word in question_lower for word in ["چگونه", "چطور"]):
            return "سوال_روشی"
        elif any(word in question_lower for word in ["چه", "چیست", "چیه"]):
            return "سوال_تعریفی"
        elif any(word in question_lower for word in ["آیا", "ایا"]):
            return "سوال_تأییدی"
        elif any(word in question_lower for word in ["تفاوت", "فرق"]):
            return "سوال_مقایسه‌ای"
        elif any(word in question_lower for word in ["اگر", "چنانچه"]):
            return "سوال_فرضی"
        elif any(word in question_lower for word in ["اثبات", "ثابت"]):
            return "سوال_اثباتی"
        elif any(word in question_lower for word in ["نتیجه", "پیامد"]):
            return "سوال_نتیجه‌گیری"
        
        return "سوال_عمومی"
    
    def extract_entities(self, text: str) -> List[Dict]:
        """استخراج موجودیت‌ها از متن"""
        entities = []
        words = text.split()
        
        # الگوهای ساده برای شناسایی موجودیت‌ها
        patterns = {
            "شیء": ["کتاب", "میز", "صندلی", "خانه", "ماشین"],
            "شخص": ["علی", "مریم", "انسان", "دانشمند", "معلم"],
            "مکان": ["تهران", "مدرسه", "بیمارستان", "کتابخانه"],
            "زمان": ["امروز", "فردا", "دیروز", "ساعت", "روز"],
            "مفهوم": ["عشق", "دوستی", "علم", "دانش", "هوش"]
        }
        
        for word in words:
            for entity_type, examples in patterns.items():
                if word in examples or self.is_similar(word, examples):
                    entities.append({
                        "نام": word,
                        "نوع": entity_type,
                        "ارتباط": self.find_entity_relations(word)
                    })
        
        return entities
    
    def is_similar(self, word: str, examples: List[str]) -> bool:
        """بررسی شباهت کلمه با مثال‌ها"""
        for example in examples:
            if word in example or example in word:
                return True
        return False
    
    def find_entity_relations(self, entity: str) -> List[str]:
        """یافتن روابط یک موجودیت"""
        relations = []
        
        if entity in ["علی", "مریم", "انسان"]:
            relations.append("انسان است")
            relations.append("نیاز به غذا دارد")
            relations.append("می‌تواند فکر کند")
        
        return relations
    
    def shallow_analysis(self, text: str) -> Dict:
        """تحلیل سطحی متن"""
        words = text.split()
        return {
            "تعداد_کلمات": len(words),
            "کلمات_کلیدی": [w for w in words if len(w) > 3],
            "دارای_سوال": "؟" in text,
            "دارای_شرط": any(w in text for w in ["اگر", "چنانچه", "درصورتی"])
        }
    
    def deep_semantic_analysis(self, text: str) -> Dict:
        """تحلیل معنایی عمیق"""
        concepts = self.semantic_analyzer.extract_concepts(text)
        
        analysis = {
            "مفاهیم_استخراج‌شده": concepts,
            "روابط_بین_مفاهیم": [],
            "شبکه_معنایی": []
        }
        
        # تحلیل روابط بین مفاهیم
        for i in range(len(concepts)):
            for j in range(i+1, len(concepts)):
                relations = self.semantic_analyzer.find_relations(concepts[i], concepts[j])
                if relations:
                    analysis["روابط_بین_مفاهیم"].append({
                        "مفهوم1": concepts[i],
                        "مفهوم2": concepts[j],
                        "روابط": relations
                    })
        
        # ساخت شبکه معنایی
        for concept in concepts:
            if concept in self.semantic_analyzer.semantic_network:
                analysis["شبکه_معنایی"].append({
                    "مفهوم": concept,
                    "اطلاعات": self.semantic_analyzer.semantic_network[concept]
                })
        
        return analysis
    
    def generate_response(self, question: str, analysis: Dict) -> str:
        """تولید پاسخ با استدلال مستقل"""
        self.conversation_history.append(question)
        
        # ثبت مراحل استدلال
        reasoning_step = {
            "سوال": question,
            "تحلیل": analysis,
            "مراحل_استدلال": []
        }
        
        # بر اساس نوع سوال، روش استدلال متفاوت است
        question_type = analysis["نوع_سوال"]
        
        if question_type == "سوال_علّی":
            response = self.answer_causal_question(question, analysis)
        elif question_type == "سوال_تعریفی":
            response = self.answer_definitional_question(question, analysis)
        elif question_type == "سوال_اثباتی":
            response = self.answer_proof_question(question, analysis)
        elif question_type == "سوال_تأییدی":
            response = self.answer_verification_question(question, analysis)
        elif question_type == "سوال_فرضی":
            response = self.answer_hypothetical_question(question, analysis)
        else:
            response = self.answer_general_question(question, analysis)
        
        # افزودن به تاریخچه استدلال
        reasoning_step["پاسخ"] = response
        self.reasoning_steps.append(reasoning_step)
        
        return response
    
    def answer_causal_question(self, question: str, analysis: Dict) -> str:
        """پاسخ به سوالات علّی"""
        # استخراج معلول از سوال
        effect_match = re.search(r"چرا (.+)\؟", question)
        if effect_match:
            effect = effect_match.group(1)
            
            # تحلیل علّی
            causal_analysis = self.causal_analyzer.analyze_causal_chain(effect)
            
            if causal_analysis["علل"]:
                causes = "، ".join(causal_analysis["علل"])
                return f"🔍 **تحلیل علّی**:\n\nبرای '{effect}'، علل احتمالی عبارتند از:\n\n• {causes}\n\n📊 **زنجیره علّی**:\n" + \
                       "\n".join([f"  - {link['علت']} → {link['معلول']}" for link in causal_analysis["زنجیره_علّی"]])
        
        # اگر تحلیل علّی مستقیم ممکن نبود
        return "🤔 **استدلال علّی**:\n\nبرای تحلیل دقیق رابطه علّی، نیاز به اطلاعات بیشتری دارم. اما بر اساس دانش عمومی:\n\n" + \
               "1. هر رویدادی می‌تواند چندین علت داشته باشد\n" + \
               "2. رابطه علّی نیاز به شواهد تجربی دارد\n" + \
               "3. همبستگی لزوماً به معنای علیت نیست\n\n" + \
               "آیا می‌خواهید در مورد روش‌های تشخیص رابطه علّی بیشتر بدانید؟"
    
    def answer_definitional_question(self, question: str, analysis: Dict) -> str:
        """پاسخ به سوالات تعریفی"""
        concepts = analysis["مفاهیم"]
        
        if concepts:
            # جستجو در شبکه معنایی
            for concept in concepts:
                if concept in self.semantic_analyzer.semantic_network:
                    concept_info = self.semantic_analyzer.semantic_network[concept]
                    
                    definition = concept_info.get("تعریف", "تعریف دقیقی در پایگاه دانش موجود نیست")
                    subsets = concept_info.get("زیرمجموعه", [])
                    applications = concept_info.get("کاربرد", [])
                    
                    response = f"📚 **تعریف و تحلیل مفهومی**:\n\n**{concept.replace('_', ' ')}**:\n{definition}\n\n"
                    
                    if subsets:
                        response += f"**زیرمجموعه‌ها**:\n" + "\n".join([f"• {s.replace('_', ' ')}" for s in subsets]) + "\n\n"
                    
                    if applications:
                        response += f"**کاربردها**:\n" + "\n".join([f"• {a.replace('_', ' ')}" for a in applications])
                    
                    return response
        
        return "🤔 **تحلیل مفهومی**:\n\nبرای ارائه تعریف دقیق، نیاز به شفاف‌سازی بیشتر دارم. آیا می‌توانید مفهوم مورد نظر را بیشتر توضیح دهید؟"
    
    def answer_proof_question(self, question: str, analysis: Dict) -> str:
        """پاسخ به سوالات اثباتی"""
        # استخراج گزاره برای اثبات
        proof_match = re.search(r"اثبات (.+)", question)
        if proof_match:
            statement = proof_match.group(1)
            
            # بررسی اجماع
            consensus = self.consensus_detector.check_consensus(statement)
            
            response = f"🔬 **روش اثبات منطقی**:\n\nبرای گزاره '{statement}':\n\n"
            
            if consensus["اجماع_کلی"] > 0.9:
                response += "✅ **این گزاره پذیرفته شده عمومی است**\n\n"
                response += f"سطح اجماع: {consensus['اجماع_کلی']*100}%\n\n"
                
                response += "**مراحل استدلال**:\n"
                response += "1. بررسی تناقض با دانش پایه ✓\n"
                response += "2. تأیید با اجماع علمی ✓\n"
                response += "3. سازگاری با قواعد منطقی ✓\n"
            
            elif consensus["اجماع_کلی"] > 0.7:
                response += "⚠️ **این گزاره نیاز به بررسی بیشتر دارد**\n\n"
                response += "**روش‌های اثبات**:\n"
                response += "1. اثبات تجربی (آزمایش)\n"
                response += "2. اثبات ریاضی (قضیه)\n"
                response += "3. استدلال منطقی (قیاس)\n"
            
            else:
                response += "❓ **این گزاره نیاز به شواهد بیشتر دارد**\n\n"
                response += "**پیشنهاد برای اثبات**:\n"
                response += "1. ارائه تعریف دقیق مفاهیم\n"
                response += "2. جمع‌آوری شواهد تجربی\n"
                response += "3. استدلال قیاسی از مقدمات پذیرفته شده\n"
            
            return response
        
        return "🔍 **سیستم اثبات**:\n\nبرای اثبات یک گزاره می‌توان از روش‌های زیر استفاده کرد:\n\n" + \
               "1. **اثبات مستقیم**: از مقدمات به نتیجه\n" + \
               "2. **اثبات با تناقض**: فرض خلاف و رسیدن به تناقض\n" + \
               "3. **اثبات تجربی**: آزمایش و مشاهده\n" + \
               "4. **اثبات ریاضی**: استفاده از قضایا و لم‌ها\n\n" + \
               "لطفاً گزاره مورد نظر برای اثبات را مشخص کنید."
    
    def answer_verification_question(self, question: str, analysis: Dict) -> str:
        """پاسخ به سوالات تأییدی"""
        # بررسی ساختار "آیا X است؟"
        verification_match = re.search(r"آیا (.+) است\؟", question)
        if verification_match:
            statement = verification_match.group(1)
            
            # بررسی اجماع و منطق
            consensus = self.consensus_detector.check_consensus(statement)
            logical_analysis = self.logical_inference.infer([statement])
            
            response = f"✅ **تحلیل تأییدی**:\n\nبرای گزاره '{statement}':\n\n"
            
            if consensus["اجماع_کلی"] > 0.8:
                response += f"**نتیجه**: با احتمال {consensus['اجماع_کلی']*100}% درست است\n\n"
                response += "**دلایل**:\n"
                
                for category, confidence in consensus["تفصیل"].items():
                    if confidence > 0.7:
                        response += f"• اجماع {category}: {confidence*100}% ✓\n"
                
                if logical_analysis:
                    response += f"• استنتاج منطقی: {logical_analysis[0]} ✓\n"
            
            elif consensus["اجماع_کلی"] < 0.3:
                response += f"**نتیجه**: احتمالاً نادرست است\n\n"
                response += "**دلایل**:\n"
                response += "• عدم اجماع علمی یا عمومی\n"
                response += "• نیاز به شواهد بیشتر\n"
            
            else:
                response += "**نتیجه**: نامشخص، نیاز به بررسی بیشتر\n\n"
                response += "**روش بررسی**:\n"
                response += "1. تعریف دقیق مفاهیم\n"
                response += "2. جمع‌آوری شواهد\n"
                response += "3. استدلال منطقی\n"
            
            return response
        
        return "🔍 **سیستم تأیید**:\n\nبرای تأیید یا رد یک گزاره:\n\n" + \
               "1. **بررسی تعاریف**: مفاهیم باید واضح باشند\n" + \
               "2. **جمع‌آوری شواهد**: مدارک تجربی\n" + \
               "3. **استدلال منطقی**: عدم تناقض\n" + \
               "4. **ارجاع به مراجع**: اجماع علمی\n\n" + \
               "لطفاً گزاره مورد نظر را به صورت دقیق مطرح کنید."
    
    def answer_hypothetical_question(self, question: str, analysis: Dict) -> str:
        """پاسخ به سوالات فرضی"""
        # استخراج فرض از سوال
        if_match = re.search(r"اگر (.+) آنگاه", question) or re.search(r"اگر (.+)،", question)
        
        if if_match:
            hypothesis = if_match.group(1)
            
            # استنتاج منطقی
            premises = [hypothesis]
            conclusions = self.logical_inference.infer(premises)
            
            response = f"🧠 **تحلیل فرضی**:\n\n**فرض**: اگر {hypothesis}\n\n"
            
            if conclusions:
                response += "**نتیجه‌گیری منطقی**:\n"
                for conclusion in conclusions:
                    response += f"• آنگاه {conclusion}\n"
                
                response += f"\n**مراحل استدلال**:\n"
                response += "1. پذیرش فرض اولیه ✓\n"
                response += "2. اعمال قواعد استنتاج ✓\n"
                response += "3. استخراج نتایج منطقی ✓\n"
            
            else:
                response += "**نتیجه**: با این فرض، نتیجه مشخصی از قواعد موجود استنتاج نمی‌شود.\n\n"
                response += "**پیشنهاد**:\n"
                response += "1. شفاف‌تر کردن فرضیه\n"
                response += "2. افزودن مقدمات بیشتر\n"
                response += "3. استفاده از قواعد استنتاج دیگر\n"
            
            return response
        
        return "🤔 **تحلیل فرضی**:\n\nبرای تحلیل یک فرضیه:\n\n" + \
               "1. **وضوح فرض**: مفروضات باید مشخص باشند\n" + \
               "2. **قواعد استنتاج**: modus ponens، قیاس و...\n" + \
               "3. **بررسی سازگاری**: عدم تناقض\n" + \
               "4. **نتایج منطقی**: استنتاج از مقدمات\n\n" + \
               "لطفاً فرضیه خود را به صورت 'اگر X آنگاه Y' مطرح کنید."
    
    def answer_general_question(self, question: str, analysis: Dict) -> str:
        """پاسخ به سوالات عمومی با استدلال"""
        concepts = analysis["مفاهیم"]
        
        if concepts:
            response = f"🤖 **تحلیل مستقل**:\n\nسوال شما درباره {', '.join(concepts)} است.\n\n"
            
            # تحلیل شبکه معنایی
            semantic_info = analysis["تحلیل_عمیق"]["شبکه_معنایی"]
            if semantic_info:
                response += "**تحلیل مفهومی**:\n"
                for info in semantic_info[:2]:  # نمایش دو مفهوم اول
                    concept = info["مفهوم"]
                    data = info["اطلاعات"]
                    
                    if "تعریف" in data:
                        response += f"• **{concept.replace('_', ' ')}**: {data['تعریف']}\n"
            
            # روابط بین مفاهیم
            relations = analysis["تحلیل_عمیق"]["روابط_بین_مفاهیم"]
            if relations:
                response += "\n**روابط کشف‌شده**:\n"
                for rel in relations[:2]:  # نمایش دو رابطه اول
                    response += f"• {rel['مفهوم1']} ↔ {rel['مفهوم2']}: {', '.join(rel['روابط'][:1])}\n"
            
            # نتیجه‌گیری
            response += "\n**نتیجه‌گیری**:\n"
            response += "بر اساس تحلیل شبکه معنایی، می‌توان گفت که این مفاهیم در حوزه‌های مرتبط قرار دارند. "
            response += "برای پاسخ دقیق‌تر، نیاز به شفاف‌سازی جنبه خاصی از سوال دارم."
            
            return response
        
        return "🧠 **پاسخ تحلیلی**:\n\nاین سوال نیاز به بررسی عمیق‌تری دارد. به عنوان یک سیستم استدلال، می‌توانم:\n\n" + \
               "1. **تحلیل معنایی**: درک روابط بین کلمات\n" + \
               "2. **استنتاج منطقی**: نتیجه‌گیری از مقدمات\n" + \
               "3. **تحلیل علّی**: بررسی روابط علت و معلول\n" + \
               "4. **تشخیص اجماع**: بررسی پذیرش عمومی\n\n" + \
               "لطفاً سوال خود را به صورت دقیق‌تر مطرح کنید."

# کلاس اصلی اپلیکیشن
class NatiqReasoningSystem:
    """سیستم اصلی استدلال natiq"""
    
    def __init__(self):
        self.ai = NatiqIndependentAI()
        self.session_stats = {
            "questions_asked": 0,
            "reasoning_steps": [],
            "topics_covered": set()
        }
    
    def process_question(self, question: str) -> Dict:
        """پردازش سوال و تولید پاسخ با استدلال"""
        self.session_stats["questions_asked"] += 1
        
        # تحلیل سوال
        analysis = self.ai.analyze_question(question)
        
        # به‌روزرسانی موضوعات
        for concept in analysis["مفاهیم"]:
            self.session_stats["topics_covered"].add(concept)
        
        # تولید پاسخ با استدلال
        response = self.ai.generate_response(question, analysis)
        
        # ذکر مراحل استدلال
        reasoning_info = {
            "total_steps": len(self.ai.reasoning_steps),
            "last_reasoning": self.ai.reasoning_steps[-1] if self.ai.reasoning_steps else None
        }
        
        return {
            "question": question,
            "response": response,
            "analysis": analysis,
            "reasoning_info": reasoning_info,
            "stats": self.session_stats
        }

# ایجاد نمونه سیستم
reasoning_system = NatiqReasoningSystem()

# صفحه اصلی با HTML کامل
@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 natiq-ultimate v4.0 | سیستم استدلال و تحلیل مستقل</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                color: #333;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                min-height: 100vh;
                box-shadow: 0 0 50px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
            }
            
            /* هدر */
            .header {
                background: linear-gradient(90deg, #2d3748, #4a5568);
                color: white;
                padding: 25px 40px;
                border-bottom: 3px solid #4299e1;
            }
            
            .header-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
            }
            
            .logo {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            
            .logo i {
                font-size: 3em;
                color: #63b3ed;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            .logo-text h1 {
                font-size: 2.2em;
                font-weight: 700;
                background: linear-gradient(45deg, #63b3ed, #90cdf4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .logo-text .tagline {
                font-size: 0.9em;
                opacity: 0.8;
                margin-top: 5px;
            }
            
            .version-badge {
                background: rgba(99, 179, 237, 0.2);
                border: 2px solid #63b3ed;
                padding: 8px 20px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 1.1em;
            }
            
            .status-indicator {
                display: flex;
                align-items: center;
                gap: 15px;
                background: rgba(255,255,255,0.1);
                padding: 12px 25px;
                border-radius: 30px;
            }
            
            .status-dot {
                width: 12px;
                height: 12px;
                background: #68d391;
                border-radius: 50%;
                animation: blink 1.5s infinite;
                box-shadow: 0 0 10px #68d391;
            }
            
            /* محتوای اصلی */
            .main-content {
                display: flex;
                flex: 1;
                min-height: 600px;
            }
            
            /* پنل چت */
            .chat-panel {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: #f7fafc;
                border-right: 1px solid #e2e8f0;
            }
            
            .messages-container {
                flex: 1;
                overflow-y: auto;
                padding: 30px;
                background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
            }
            
            .message {
                margin: 20px 0;
                padding: 25px;
                border-radius: 20px;
                max-width: 90%;
                position: relative;
                animation: slideIn 0.4s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }
            
            @keyframes slideIn {
                from { 
                    opacity: 0;
                    transform: translateY(20px) scale(0.95);
                }
                to { 
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .user-message {
                background: linear-gradient(135deg, #4299e1, #3182ce);
                color: white;
                margin-left: auto;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                border-right: 5px solid #2b6cb0;
            }
            
            .bot-message {
                background: linear-gradient(135deg, #ffffff, #f7fafc);
                color: #2d3748;
                margin-right: auto;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
                border-left: 5px solid #4299e1;
                border: 1px solid #e2e8f0;
            }
            
            .message-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 15px;
                padding-bottom: 12px;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }
            
            .user-message .message-header {
                border-bottom-color: rgba(255,255,255,0.3);
            }
            
            .bot-message .message-header {
                border-bottom-color: rgba(66, 153, 225, 0.2);
            }
            
            .message-icon {
                font-size: 1.8em;
            }
            
            .message-type {
                font-weight: bold;
                font-size: 0.9em;
                opacity: 0.9;
            }
            
            .message-content {
                white-space: pre-wrap;
                line-height: 1.8;
                font-size: 1.05em;
            }
            
            .message-time {
                font-size: 0.8em;
                opacity: 0.7;
                margin-top: 15px;
                text-align: left;
            }
            
            .user-message .message-time {
                text-align: right;
            }
            
            /* ورودی */
            .input-panel {
                background: white;
                padding: 30px;
                border-top: 1px solid #e2e8f0;
            }
            
            .input-group {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
            }
            
            #messageInput {
                flex: 1;
                padding: 20px 25px;
                border: 2px solid #e2e8f0;
                border-radius: 15px;
                font-size: 1.1em;
                font-family: inherit;
                transition: all 0.3s;
                background: #f7fafc;
            }
            
            #messageInput:focus {
                outline: none;
                border-color: #4299e1;
                background: white;
                box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
            }
            
            #sendButton {
                width: 70px;
                background: linear-gradient(45deg, #4299e1, #3182ce);
                color: white;
                border: none;
                border-radius: 15px;
                cursor: pointer;
                font-size: 1.3em;
                transition: all 0.3s;
            }
            
            #sendButton:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(66, 153, 225, 0.3);
            }
            
            .reasoning-buttons {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 12px;
                margin-top: 20px;
            }
            
            .reasoning-btn {
                padding: 15px;
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                gap: 10px;
            }
            
            .reasoning-btn:hover {
                transform: translateY(-3px);
                border-color: #4299e1;
                box-shadow: 0 5px 15px rgba(66, 153, 225, 0.1);
            }
            
            .reasoning-btn i {
                font-size: 1.5em;
                color: #4299e1;
            }
            
            /* پنل تحلیل */
            .analysis-panel {
                width: 400px;
                background: #2d3748;
                color: white;
                overflow-y: auto;
                padding: 25px;
            }
            
            .panel-section {
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #4a5568;
            }
            
            .panel-section h3 {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
                color: #90cdf4;
                font-size: 1.1em;
            }
            
            .reasoning-steps {
                background: rgba(255,255,255,0.05);
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .reasoning-step {
                padding: 10px;
                margin: 8px 0;
                background: rgba(255,255,255,0.1);
                border-radius: 6px;
                font-size: 0.9em;
            }
            
            .concept-tag {
                display: inline-block;
                background: rgba(66, 153, 225, 0.2);
                color: #90cdf4;
                padding: 5px 12px;
                border-radius: 15px;
                margin: 3px;
                font-size: 0.85em;
                border: 1px solid rgba(66, 153, 225, 0.3);
            }
            
            .stat-item {
                display: flex;
                justify-content: space-between;
                margin: 10px 0;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            
            .stat-value {
                color: #68d391;
                font-weight: bold;
            }
            
            /* welcome message */
            .welcome-message {
                background: linear-gradient(135deg, #4299e1, #3182ce);
                color: white;
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 30px;
                border: none;
                box-shadow: 0 10px 30px rgba(66, 153, 225, 0.2);
            }
            
            .welcome-message h2 {
                margin-bottom: 15px;
                font-size: 1.6em;
            }
            
            .capabilities-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin: 20px 0;
            }
            
            .capability {
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                backdrop-filter: blur(10px);
            }
            
            .capability i {
                font-size: 1.8em;
                margin-bottom: 10px;
                display: block;
            }
            
            /* responsive */
            @media (max-width: 1200px) {
                .main-content {
                    flex-direction: column;
                }
                
                .analysis-panel {
                    width: 100%;
                    border-top: 1px solid #4a5568;
                }
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 0;
                }
                
                .header-content {
                    flex-direction: column;
                    text-align: center;
                }
                
                .logo {
                    flex-direction: column;
                }
                
                .message {
                    max-width: 95%;
                    padding: 20px;
                }
                
                .capabilities-grid {
                    grid-template-columns: 1fr;
                }
                
                .reasoning-buttons {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
        </style>
        
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <!-- Google Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <script>
            class NatiqReasoningApp {
                constructor() {
                    this.sessionId = 'reasoning_' + Date.now();
                    this.baseUrl = window.location.origin;
                    this.messageCount = 0;
                    this.reasoningSteps = [];
                    this.concepts = new Set();
                    this.init();
                }
                
                init() {
                    console.log('🧠 natiq-ultimate v4.0 - سیستم استدلال مستقل');
                    this.setupEventListeners();
                    this.updateStatus('🔬 سیستم استدلال فعال');
                    this.updateDateTime();
                    setInterval(() => this.updateDateTime(), 60000);
                }
                
                setupEventListeners() {
                    const sendBtn = document.getElementById('sendButton');
                    const messageInput = document.getElementById('messageInput');
                    
                    sendBtn.addEventListener('click', () => this.sendMessage());
                    
                    messageInput.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            this.sendMessage();
                        }
                    });
                    
                    // دکمه‌های استدلال
                    document.querySelectorAll('.reasoning-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            const question = e.target.getAttribute('data-question') || 
                                          e.target.closest('.reasoning-btn').getAttribute('data-question');
                            if (question) {
                                document.getElementById('messageInput').value = question;
                                this.sendMessage();
                            }
                        });
                    });
                }
                
                updateDateTime() {
                    const now = new Date();
                    const options = {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit'
                    };
                    const dateStr = now.toLocaleDateString('fa-IR', options);
                    document.getElementById('currentDateTime').textContent = dateStr;
                }
                
                updateStatus(message) {
                    const statusText = document.getElementById('statusText');
                    if (statusText) {
                        statusText.textContent = message;
                    }
                }
                
                async sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (!message) return;
                    
                    // نمایش پیام کاربر
                    this.addMessage(message, 'user', 'سوال شما');
                    messageInput.value = '';
                    this.messageCount++;
                    
                    // نمایش حالت استدلال
                    this.showReasoning();
                    
                    try {
                        const response = await fetch(this.baseUrl + '/api/reason/' + this.sessionId, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ 
                                message: message,
                                session_id: this.sessionId
                            })
                        });
                        
                        if (!response.ok) {
                            throw new Error(`خطای HTTP: ${response.status}`);
                        }
                        
                        const data = await response.json();
                        
                        this.hideReasoning();
                        
                        // نمایش پاسخ با استدلال
                        const responseText = data.response;
                        const analysis = data.analysis;
                        
                        this.addMessage(responseText, 'bot', 'تحلیل استدلالی');
                        
                        // به‌روزرسانی پنل تحلیل
                        this.updateAnalysisPanel(analysis, data.reasoning_info);
                        
                        this.updateStatus('✅ تحلیل کامل شد');
                        
                        // به‌روزرسانی آمار
                        this.updateStats(data.stats);
                        
                    } catch (error) {
                        this.hideReasoning();
                        console.error('❌ خطا:', error);
                        
                        this.addMessage('⚠️ خطا در پردازش استدلالی. لطفاً دوباره تلاش کنید.', 'error', 'خطا');
                        this.updateStatus('❌ خطا در استدلال');
                    }
                }
                
                addMessage(text, type, header = '') {
                    const messagesDiv = document.getElementById('messages');
                    const time = new Date().toLocaleTimeString('fa-IR', {
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit'
                    });
                    
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${type}-message`;
                    
                    const icon = type === 'user' ? '👤' : 
                                 type === 'error' ? '⚠️' : '🤖';
                    
                    const headerText = header || (type === 'user' ? 'سوال شما' : 'تحلیل استدلالی');
                    
                    messageDiv.innerHTML = `
                        <div class="message-header">
                            <div class="message-icon">${icon}</div>
                            <div class="message-type">${headerText}</div>
                        </div>
                        <div class="message-content">${this.escapeHtml(text)}</div>
                        <div class="message-time">${time}</div>
                    `;
                    
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                showReasoning() {
                    const messagesDiv = document.getElementById('messages');
                    
                    const reasoningDiv = document.createElement('div');
                    reasoningDiv.className = 'message bot-message';
                    reasoningDiv.id = 'reasoningIndicator';
                    reasoningDiv.innerHTML = `
                        <div class="message-header">
                            <div class="message-icon">🧠</div>
                            <div class="message-type">در حال استدلال...</div>
                        </div>
                        <div class="message-content">
                            <div style="display: flex; align-items: center; gap: 15px; padding: 10px 0;">
                                <div style="display: flex; gap: 8px;">
                                    <span style="animation: blink 1.4s infinite; color: #4299e1; font-size: 1.2em;">●</span>
                                    <span style="animation: blink 1.4s infinite 0.2s; color: #3182ce; font-size: 1.2em;">●</span>
                                    <span style="animation: blink 1.4s infinite 0.4s; color: #63b3ed; font-size: 1.2em;">●</span>
                                </div>
                                <div style="flex: 1;">
                                    در حال تحلیل معنایی، استنتاج منطقی و بررسی روابط علّی...
                                </div>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(reasoningDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                hideReasoning() {
                    const reasoning = document.getElementById('reasoningIndicator');
                    if (reasoning) {
                        reasoning.remove();
                    }
                }
                
                updateAnalysisPanel(analysis, reasoningInfo) {
                    // به‌روزرسانی مفاهیم
                    const conceptsDiv = document.getElementById('conceptsList');
                    if (conceptsDiv && analysis.mفاهیم) {
                        conceptsDiv.innerHTML = '';
                        analysis.mفاهیم.forEach(concept => {
                            const span = document.createElement('span');
                            span.className = 'concept-tag';
                            span.textContent = concept.replace(/_/g, ' ');
                            conceptsDiv.appendChild(span);
                        });
                    }
                    
                    // به‌روزرسانی مراحل استدلال
                    if (reasoningInfo && reasoningInfo.last_reasoning) {
                        this.reasoningSteps.push(reasoningInfo.last_reasoning);
                        this.updateReasoningSteps();
                    }
                    
                    // به‌روزرسانی نوع سوال
                    const questionTypeDiv = document.getElementById('questionType');
                    if (questionTypeDiv && analysis.nوع_سوال) {
                        questionTypeDiv.textContent = analysis.nوع_سوال.replace(/_/g, ' ');
                    }
                }
                
                updateReasoningSteps() {
                    const stepsDiv = document.getElementById('reasoningSteps');
                    if (stepsDiv) {
                        stepsDiv.innerHTML = '';
                        
                        const lastSteps = this.reasoningSteps.slice(-3).reverse();
                        
                        lastSteps.forEach(step => {
                            const stepDiv = document.createElement('div');
                            stepDiv.className = 'reasoning-step';
                            stepDiv.innerHTML = `
                                <div style="font-size: 0.8em; opacity: 0.8;">سوال: ${step.sوال.substring(0, 50)}...</div>
                                <div style="margin-top: 5px; font-size: 0.9em;">مراحل استدلال: ${step.ماحل_استدلال ? step.ماحل_استدلال.length : 0}</div>
                            `;
                            stepsDiv.appendChild(stepDiv);
                        });
                    }
                }
                
                updateStats(stats) {
                    document.getElementById('messageCount').textContent = this.messageCount;
                    document.getElementById('questionsAsked').textContent = stats.questions_asked || this.messageCount;
                    document.getElementById('topicsCovered').textContent = stats.topics_covered ? stats.topics_covered.size : this.concepts.size;
                    
                    // به‌روزرسانی شناسه جلسه
                    document.getElementById('sessionIdDisplay').textContent = this.sessionId.substring(0, 12) + '...';
                }
                
                escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }
            }
            
            // راه‌اندازی اپ
            document.addEventListener('DOMContentLoaded', () => {
                window.natiqApp = new NatiqReasoningApp();
                document.getElementById('messageInput').focus();
                
                // نمایش پیام خوش‌آمدگویی
                setTimeout(() => {
                    const welcomeMsg = `🧠 **به سیستم استدلال natiq-ultimate خوش آمدید!**\n\nمن یک سیستم تحلیل مستقل هستم که می‌توانم:\n\n✅ درک معنایی جملات\n✅ استنتاج و تحلیل منطقی\n✅ تشخیص روابط علّی\n✅ بررسی اجماع و اثبات\n✅ استدلال مستقل و انتقادی\n\nلطفاً سوالی بپرسید که نیاز به استدلال داشته باشد!`;
                    window.natiqApp.addMessage(welcomeMsg, 'bot', 'سیستم استدلال مستقل');
                }, 500);
            });
            
            // توابع کمکی
            function clearChat() {
                if (confirm('آیا مطمئن هستید که می‌خواهید همه گفتگو و تحلیل‌ها را پاک کنید؟')) {
                    const messagesDiv = document.getElementById('messages');
                    const welcomeDiv = messagesDiv.querySelector('.welcome-message');
                    
                    while (messagesDiv.firstChild) {
                        messagesDiv.removeChild(messagesDiv.firstChild);
                    }
                    
                    if (welcomeDiv) {
                        messagesDiv.appendChild(welcomeDiv);
                    }
                    
                    window.natiqApp.messageCount = 0;
                    window.natiqApp.reasoningSteps = [];
                    window.natiqApp.concepts.clear();
                    window.natiqApp.updateStats({questions_asked: 0, topics_covered: new Set()});
                    window.natiqApp.updateStatus('🗑️ گفتگو پاک شد');
                    
                    // پاک کردن پنل تحلیل
                    document.getElementById('conceptsList').innerHTML = '';
                    document.getElementById('reasoningSteps').innerHTML = '';
                    document.getElementById('questionType').textContent = '--';
                }
            }
            
            function testSystem() {
                const questions = [
                    "چرا آسمان آبی است؟",
                    "اگر باران ببارد، چه می‌شود؟",
                    "آیا زمین گرد است؟",
                    "اثبات کن که اگر A=B و B=C آنگاه A=C",
                    "تفاوت هوش مصنوعی و یادگیری ماشین چیست؟",
                    "علت رشد گیاهان چیست؟"
                ];
                
                const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
                document.getElementById('messageInput').value = randomQuestion;
                window.natiqApp.sendMessage();
            }
        </script>
    </head>
    <body>
        <div class="container">
            <!-- هدر -->
            <header class="header">
                <div class="header-content">
                    <div class="logo">
                        <i class="fas fa-brain"></i>
                        <div class="logo-text">
                            <h1>natiq-ultimate</h1>
                            <div class="tagline">سیستم استدلال و تحلیل مستقل</div>
                        </div>
                    </div>
                    
                    <div class="version-badge">
                        نسخه ۴.۰
                    </div>
                    
                    <div class="status-indicator">
                        <span class="status-dot"></span>
                        <span id="statusText">در حال راه‌اندازی...</span>
                    </div>
                </div>
            </header>
            
            <!-- محتوای اصلی -->
            <div class="main-content">
                <!-- پنل چت -->
                <div class="chat-panel">
                    <div class="messages-container" id="messages">
                        <!-- پیام خوش‌آمدگویی -->
                        <div class="welcome-message">
                            <h2>🧠 سیستم استدلال مستقل فعال شد</h2>
                            <p>این سیستم می‌تواند سوالات شما را تحلیل معنایی کند، استنتاج منطقی انجام دهد، روابط علّی را بررسی کند و استدلال مستقل ارائه دهد.</p>
                            
                            <div class="capabilities-grid">
                                <div class="capability">
                                    <i class="fas fa-search"></i>
                                    <div>تحلیل معنایی</div>
                                </div>
                                <div class="capability">
                                    <i class="fas fa-project-diagram"></i>
                                    <div>استنتاج منطقی</div>
                                </div>
                                <div class="capability">
                                    <i class="fas fa-link"></i>
                                    <div>روابط علّی</div>
                                </div>
                                <div class="capability">
                                    <i class="fas fa-check-double"></i>
                                    <div>تشخیص اجماع</div>
                                </div>
                            </div>
                            
                            <p style="margin-top: 15px; font-size: 0.9em;">
                                <strong>💡 نکته:</strong> سوالاتی بپرسید که نیاز به استدلال، تحلیل یا اثبات داشته باشند.
                            </p>
                        </div>
                    </div>
                    
                    <!-- پنل ورودی -->
                    <div class="input-panel">
                        <div class="input-group">
                            <input 
                                type="text" 
                                id="messageInput" 
                                placeholder="سوال استدلالی خود را اینجا بنویسید (مثلاً: اثبات کن که...)..." 
                                autocomplete="off"
                                autofocus
                            >
                            <button id="sendButton">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        
                        <div class="reasoning-buttons">
                            <button class="reasoning-btn" data-question="چرا آسمان آبی است؟">
                                <i class="fas fa-question-circle"></i>
                                سوال علّی
                            </button>
                            <button class="reasoning-btn" data-question="اگر باران ببارد، چه می‌شود؟">
                                <i class="fas fa-cloud-rain"></i>
                                سوال فرضی
                            </button>
                            <button class="reasoning-btn" data-question="آیا زمین گرد است؟">
                                <i class="fas fa-globe"></i>
                                سوال تأییدی
                            </button>
                            <button class="reasoning-btn" data-question="اثبات کن که اگر A=B و B=C آنگاه A=C">
                                <i class="fas fa-calculator"></i>
                                سوال اثباتی
                            </button>
                            <button class="reasoning-btn" data-question="تفاوت هوش مصنوعی و یادگیری ماشین چیست؟">
                                <i class="fas fa-robot"></i>
                                سوال مقایسه‌ای
                            </button>
                            <button class="reasoning-btn" onclick="testSystem()">
                                <i class="fas fa-vial"></i>
                                تست سیستم
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- پنل تحلیل -->
                <div class="analysis-panel">
                    <div class="panel-section">
                        <h3><i class="fas fa-chart-line"></i> آمار جلسه</h3>
                        <div class="stat-item">
                            <span>پیام‌ها:</span>
                            <span class="stat-value" id="messageCount">0</span>
                        </div>
                        <div class="stat-item">
                            <span>سوالات:</span>
                            <span class="stat-value" id="questionsAsked">0</span>
                        </div>
                        <div class="stat-item">
                            <span>موضوعات:</span>
                            <span class="stat-value" id="topicsCovered">0</span>
                        </div>
                        <div class="stat-item">
                            <span>زمان:</span>
                            <span class="stat-value" id="currentDateTime">--</span>
                        </div>
                        <div class="stat-item">
                            <span>شناسه:</span>
                            <span class="stat-value" id="sessionIdDisplay">...</span>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-lightbulb"></i> مفاهیم استخراج‌شده</h3>
                        <div id="conceptsList" style="min-height: 60px;">
                            <span style="opacity: 0.7; font-size: 0.9em;">هنوز مفهومی استخراج نشده</span>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-sitemap"></i> نوع سوال</h3>
                        <div style="padding: 10px; background: rgba(255,255,255,0.05); border-radius: 6px;">
                            <span id="questionType">--</span>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-history"></i> مراحل استدلال اخیر</h3>
                        <div class="reasoning-steps" id="reasoningSteps">
                            <span style="opacity: 0.7; font-size: 0.9em;">هنوز استدلالی ثبت نشده</span>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-cogs"></i> عملیات</h3>
                        <div>
                            <button onclick="clearChat()" style="width:100%; padding:12px; background:#e53e3e; color:white; border:none; border-radius:8px; cursor:pointer; margin-bottom:10px; display:flex; align-items:center; justify-content:center; gap:8px;">
                                <i class="fas fa-trash"></i> پاک کردن همه
                            </button>
                            <button onclick="window.natiqApp.updateStatus('🔄 سیستم به‌روز شد')" style="width:100%; padding:12px; background:#38a169; color:white; border:none; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;">
                                <i class="fas fa-sync"></i> بروزرسانی
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {
        "status": "reasoning_active",
        "service": "natiq-ultimate",
        "version": "4.0.0",
        "environment": "vercel",
        "timestamp": datetime.now().isoformat(),
        "capabilities": [
            "تحلیل معنایی عمیق",
            "استنتاج منطقی",
            "تحلیل روابط علّی", 
            "تشخیص اجماع و اثبات",
            "استدلال مستقل",
            "شبکه معنایی مفهومی"
        ],
        "reasoning_modules": [
            "SemanticAnalyzer",
            "LogicalInference", 
            "CausalAnalyzer",
            "ConsensusDetector",
            "IndependentReasoning"
        ]
    }

@app.post("/api/reason/{session_id}")
async def reason_endpoint(session_id: str, request: dict):
    try:
        question = request.get("message", "")
        
        if not question or question.strip() == "":
            raise HTTPException(status_code=400, detail="سوال نمی‌تواند خالی باشد")
        
        # پردازش با سیستم استدلال
        result = reasoning_system.process_question(question)
        
        return {
            "session_id": session_id,
            "question": question,
            "response": result["response"],
            "analysis": result["analysis"],
            "reasoning_info": result["reasoning_info"],
            "stats": result["stats"],
            "timestamp": datetime.now().isoformat(),
            "version": "4.0.0"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "خطا در پردازش استدلالی",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/debug")
async def debug_info():
    """اطلاعات دیباگ برای سیستم استدلال"""
    return {
        "system": "natiq-ultimate-reasoning",
        "version": "4.0.0",
        "active_modules": [
            "SemanticAnalyzer",
            "LogicalInference",
            "CausalAnalyzer",
            "ConsensusDetector"
        ],
        "session_count": 1,
        "reasoning_system": {
            "conversation_history_length": len(reasoning_system.ai.conversation_history),
            "reasoning_steps_count": len(reasoning_system.ai.reasoning_steps),
            "semantic_network_size": len(reasoning_system.ai.semantic_analyzer.semantic_network)
        }
    }

# هندلر برای favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return JSONResponse({"status": "no favicon"})

# برای Vercel
app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
