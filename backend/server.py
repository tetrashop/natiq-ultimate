#!/usr/bin/env python3
"""
natiq-ultimate - سیستم یکپارچه مبتنی بر گراف دانش
نسخه 5.0: یک معماری یکپارچه با گراف دانش، استنتاج یکپارچه و درک واحد
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import json
import re
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
import heapq

app = FastAPI(
    title="natiq-ultimate",
    description="سیستم هوش مصنوعی یکپارچه مبتنی بر گراف دانش",
    version="5.0.0"
)

# CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== سیستم گراف دانش یکپارچه ====================

class UnifiedKnowledgeGraph:
    """گراف دانش یکپارچه که همه مفاهیم، روابط و قوانین را در یک ساختار نگه می‌دارد"""
    
    def __init__(self):
        self.graph = defaultdict(dict)  # گراف اصلی
        self.concepts = {}  # مفاهیم و ویژگی‌های آنها
        self.rules = []  # قواعد استنتاج
        self.causal_chains = []  # زنجیره‌های علّی
        self.consensus_levels = {}  # سطوح اجماع
        self.initialize_unified_knowledge()
    
    def initialize_unified_knowledge(self):
        """ایجاد دانش یکپارچه اولیه"""
        
        # ========== مفاهیم پایه با ویژگی‌های یکپارچه ==========
        self.concepts = {
            "هوش_مصنوعی": {
                "type": "مفهوم_علمی",
                "definition": "سیستم‌های کامپیوتری که می‌توانند وظایف نیازمند هوش انسانی را انجام دهند",
                "properties": ["یادگیری", "استدلال", "درک_زبان", "حل_مسئله"],
                "subclasses": ["یادگیری_ماشین", "پردازش_زبان_طبیعی", "بینایی_کامپیوتر"],
                "causes": ["اتوماسیون", "بهینه‌سازی", "تحلیل_داده"],
                "effects": ["پیشرفت_تکنولوژی", "تغییر_شغل‌ها", "تحول_صنعت"],
                "consensus": 0.95,
                "examples": ["دستیار_هوشمند", "سیستم_توصیه‌گر", "ربات_چت"],
                "relations": {
                    "شامل": ["یادگیری_ماشین"],
                    "کاربرد": ["تشخیص_تصویر", "پردازش_متن"],
                    "مبنا": ["ریاضیات", "علوم_کامپیوتر"]
                }
            },
            
            "یادگیری_ماشین": {
                "type": "زیرشاخه",
                "definition": "زیرشاخه‌ای از هوش مصنوعی که به سیستم‌ها توانایی یادگیری از داده بدون برنامه‌نویسی صریح می‌دهد",
                "properties": ["یادگیری_از_داده", "پیش‌بینی", "طبقه‌بندی"],
                "subclasses": ["یادگیری_نظارت‌شده", "یادگیری_بدون_نظارت", "یادگیری_تقویتی"],
                "causes": ["نیاز_به_پیش‌بینی", "حجم_بالای_داده", "پیچیدگی_مسائل"],
                "effects": ["مدل‌های_پیش‌بینی", "سیستم‌های_توصیه‌گر", "تشخیص_الگو"],
                "consensus": 0.98,
                "examples": ["مدل_تشخیص_تصویر", "سیستم_پیشنهاد_فیلم", "پیش‌بینی_قیمت"],
                "relations": {
                    "جزء": ["هوش_مصنوعی"],
                    "استفاده_می‌کند": ["الگوریتم", "داده"],
                    "تولید_می‌کند": ["پیش‌بینی", "طبقه‌بندی"]
                }
            },
            
            "علت": {
                "type": "مفهوم_منطقی",
                "definition": "عاملی که رویداد یا حالت دیگری را به وجود می‌آورد",
                "properties": ["تقدم_زمانی", "ارتباط_ضروری", "تأثیرگذاری"],
                "subclasses": ["علت_فعال", "علت_مادی", "علت_صوری", "علت_غایی"],
                "examples": ["بارش_باران", "آموزش_دیدین", "کاشت_بذر"],
                "consensus": 0.99,
                "relations": {
                    "منجر_می‌شود_به": ["معلول"],
                    "نیاز_دارد_به": ["شرایط_لازم"],
                    "همراه_است_با": ["همبستگی"]
                }
            },
            
            "معلول": {
                "type": "مفهوم_منطقی",
                "definition": "رویداد یا حالتی که در نتیجه علت به وجود می‌آید",
                "properties": ["تأخر_زمانی", "وابستگی", "نتیجه‌گیری"],
                "examples": ["خیس_شدن_زمین", "یادگیری", "روئیدن_گیاه"],
                "consensus": 0.99,
                "relations": {
                    "ناشی_می‌شود_از": ["علت"],
                    "منجر_می‌شود_به": ["معلول_ثانویه"]
                }
            },
            
            "اجماع": {
                "type": "مفهوم_اجتماعی",
                "definition": "توافق جمعی بر سر یک موضوع بین افراد صاحب نظر",
                "properties": ["اتفاق_نظر", "پذیرش_جمعی", "اعتبار"],
                "subclasses": ["اجماع_علمی", "اجماع_اخلاقی", "اجماع_منطقی"],
                "examples": ["گردی_زمین", "جوشیدن_آب_در_100_درجه", "اصل_عدم_تناقض"],
                "consensus": 0.97,
                "relations": {
                    "ناشی_می‌شود_از": ["شواهد", "استدلال"],
                    "منجر_می‌شود_به": ["اعتماد", "پذیرش"]
                }
            }
        }
        
        # ========== روابط در گراف ==========
        # هر رابطه: (مفهوم1, رابطه, مفهوم2, وزن)
        self.graph = {
            "هوش_مصنوعی": {
                "شامل": [("یادگیری_ماشین", 0.9)],
                "نیاز_دارد_به": [("داده", 0.8), ("الگوریتم", 0.85)],
                "تولید_می‌کند": [("اتوماسیون", 0.75), ("تحلیل", 0.8)],
                "نوعی_است_از": [("تکنولوژی", 0.9)]
            },
            "یادگیری_ماشین": {
                "جزء": [("هوش_مصنوعی", 0.9)],
                "استفاده_می‌کند": [("داده", 0.95), ("آمار", 0.85)],
                "تولید_می‌کند": [("پیش‌بینی", 0.88), ("مدل", 0.9)]
            },
            "بارش_باران": {
                "علت_است_برای": [("خیس_شدن_زمین", 0.95), ("رشد_گیاهان", 0.7)],
                "نیاز_دارد_به": [("ابر", 0.9), ("رطوبت", 0.85)]
            },
            "آموزش": {
                "علت_است_برای": [("یادگیری", 0.85), ("مهارت", 0.8)],
                "شامل": [("تمرین", 0.75), ("مطالعه", 0.8)]
            }
        }
        
        # ========== قواعد استنتاج یکپارچه ==========
        self.rules = [
            {
                "name": "انتقال_علّی",
                "condition": ["A علت_است_برای B", "B علت_است_برای C"],
                "conclusion": "A علت_است_برای C",
                "confidence": 0.8,
                "type": "causal_transitive"
            },
            {
                "name": "تعریف_مفهوم",
                "condition": ["X نوعی_است_از Y", "Y دارای_ویژگی Z"],
                "conclusion": "X دارای_ویژگی Z",
                "confidence": 0.75,
                "type": "property_inheritance"
            },
            {
                "name": "اجماع_علمی",
                "condition": ["X تایید_شده_توسط جامعه_علمی", "جامعه_علمی دارای_اعتبار بالا"],
                "conclusion": "X درست_است",
                "confidence": 0.9,
                "type": "consensus_based"
            },
            {
                "name": "استنتاج_منطقی",
                "condition": ["اگر P آنگاه Q", "P درست_است"],
                "conclusion": "Q درست_است",
                "confidence": 1.0,
                "type": "modus_ponens"
            }
        ]
        
        # ========== زنجیره‌های علّی از پیش تعریف شده ==========
        self.causal_chains = [
            ["آموزش", "یادگیری", "مهارت", "عملکرد_بهتر"],
            ["بارش_باران", "خیس_شدن_زمین", "رشد_گیاهان", "تولید_اکسیژن"],
            ["تمرین", "تجربه", "تبحر", "کارایی_بالاتر"],
            ["تحقیق", "کشف", "اختراع", "پیشرفت_علمی"]
        ]
        
        # ========== سطوح اجماع ==========
        self.consensus_levels = {
            "علمی_قطعی": 0.99,  # مانند گردی زمین
            "علمی_قوی": 0.95,   # مانند تغییرات اقلیمی
            "علمی_متوسط": 0.85, # مانند فواید برخی داروها
            "اخلاقی_قوی": 0.9,  # مانند بد بودن دزدی
            "اخلاقی_متوسط": 0.7, # مانند مسائل پیچیده اخلاقی
            "منطقی_قطعی": 1.0,   # مانند اصول منطق
            "عمومی_قوی": 0.95,   # مانند خورشید از شرق طلوع می‌کند
        }
    
    def find_path(self, start: str, end: str, max_depth: int = 4) -> List[List[str]]:
        """یافتن مسیر بین دو مفهوم در گراف"""
        if start not in self.graph or end not in self.concepts:
            return []
        
        paths = []
        visited = set()
        
        def dfs(current: str, path: List[Tuple[str, str, str]], depth: int):
            if depth > max_depth:
                return
            
            visited.add(current)
            
            if current == end:
                paths.append(path.copy())
                visited.remove(current)
                return
            
            # جستجو در همسایه‌ها
            if current in self.graph:
                for relation, targets in self.graph[current].items():
                    for target, weight in targets:
                        if target not in visited:
                            new_path = path + [(current, relation, target)]
                            dfs(target, new_path, depth + 1)
            
            # جستجو معکوس (کسانی که به این مفهوم اشاره دارند)
            for source, relations in self.graph.items():
                for relation, targets in relations.items():
                    for target, weight in targets:
                        if target == current and source not in visited:
                            new_path = path + [(source, relation, current)]
                            dfs(source, new_path, depth + 1)
            
            visited.remove(current)
        
        dfs(start, [], 0)
        return paths
    
    def infer_causal_chain(self, start_concept: str) -> List[List[str]]:
        """استنتاج زنجیره علّی از یک مفهوم"""
        chains = []
        
        # بررسی زنجیره‌های از پیش تعریف شده
        for chain in self.causal_chains:
            if start_concept in chain:
                idx = chain.index(start_concept)
                chains.append(chain[idx:])
        
        # استنتاج از گراف
        if start_concept in self.graph:
            for relation, targets in self.graph[start_concept].items():
                if "علت" in relation or "منجر" in relation:
                    for target, _ in targets:
                        # ادامه زنجیره از هدف
                        sub_chains = self.infer_causal_chain(target)
                        for sub_chain in sub_chains:
                            chains.append([start_concept] + sub_chain)
        
        return chains[:5]  # برگرداندن 5 زنجیره اول
    
    def check_consensus(self, concept: str, statement: str = None) -> Dict:
        """بررسی اجماع روی یک مفهوم یا گزاره"""
        result = {
            "concept": concept,
            "statement": statement,
            "consensus_level": 0.0,
            "confidence": 0.0,
            "sources": [],
            "type": None
        }
        
        # اگر مفهوم در پایگاه دانش باشد
        if concept in self.concepts:
            concept_data = self.concepts[concept]
            result["consensus_level"] = concept_data.get("consensus", 0.5)
            result["type"] = concept_data.get("type")
            result["confidence"] = 0.8
            
            # اضافه کردن منابع
            if "examples" in concept_data:
                result["sources"].extend(concept_data["examples"])
        
        # تطبیق با سطوح اجماع شناخته شده
        for level_name, level_value in self.consensus_levels.items():
            if concept in level_name or (statement and any(word in statement for word in level_name.split("_"))):
                if level_value > result["consensus_level"]:
                    result["consensus_level"] = level_value
                    result["type"] = level_name.split("_")[0]
                    result["confidence"] = 0.9
        
        return result
    
    def unified_inference(self, premises: List[str], query_type: str = "general") -> Dict:
        """استنتاج یکپارچه از مقدمات"""
        results = {
            "premises": premises,
            "inferences": [],
            "confidence": 0.0,
            "method": "unified_graph_traversal"
        }
        
        # استخراج مفاهیم از مقدمات
        concepts_in_premises = set()
        for premise in premises:
            # استخراج کلمات کلیدی
            words = premise.replace("_", " ").split()
            for word in words:
                if word in self.concepts:
                    concepts_in_premises.add(word)
        
        # اعمال قواعد استنتاج
        for rule in self.rules:
            if self._rule_applies(rule["condition"], premises):
                inference = {
                    "conclusion": rule["conclusion"],
                    "rule": rule["name"],
                    "confidence": rule["confidence"],
                    "type": rule["type"]
                }
                results["inferences"].append(inference)
        
        # اگر استنتاجی انجام نشد، از گراف استفاده کن
        if not results["inferences"] and concepts_in_premises:
            # یافتن روابط بین مفاهیم
            for concept in concepts_in_premises:
                if concept in self.graph:
                    for relation, targets in self.graph[concept].items():
                        for target, weight in targets:
                            if target in concepts_in_premises or target in self.concepts:
                                inference = {
                                    "conclusion": f"{concept} {relation} {target}",
                                    "rule": "graph_relation",
                                    "confidence": weight,
                                    "type": "direct_relation"
                                }
                                results["inferences"].append(inference)
        
        # محاسبه اطمینان کلی
        if results["inferences"]:
            total_confidence = sum(inf["confidence"] for inf in results["inferences"])
            results["confidence"] = total_confidence / len(results["inferences"])
        
        return results
    
    def _rule_applies(self, conditions: List[str], premises: List[str]) -> bool:
        """بررسی اینکه آیا شرایط یک قاعده برقرار است"""
        for condition in conditions:
            condition_met = False
            for premise in premises:
                # تطبیق ساده الگو
                if condition in premise or premise in condition:
                    condition_met = True
                    break
            
            if not condition_met:
                return False
        
        return True

# ==================== سیستم پردازش زبان یکپارچه ====================

class UnifiedLanguageProcessor:
    """پردازشگر زبان یکپارچه که با گراف دانش کار می‌کند"""
    
    def __init__(self, knowledge_graph: UnifiedKnowledgeGraph):
        self.kg = knowledge_graph
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self):
        """الگوهای استخراج یکپارچه"""
        return {
            "causal_question": [
                r"چرا (.+)\؟",
                r"علت (.+) چیست\؟",
                r"دلیل (.+) چه هست\؟"
            ],
            "definition_question": [
                r"(.+) چیست\؟",
                r"تعریف (.+) چیست\؟",
                r"منظور از (.+) چیست\؟"
            ],
            "comparison_question": [
                r"تفاوت (.+) و (.+) چیست\؟",
                r"فرق (.+) با (.+) در چیست\؟"
            ],
            "proof_question": [
                r"اثبات کن (.+)",
                r"ثابت کن (.+)",
                r"چگونه ثابت می‌شود (.+)\؟"
            ],
            "consensus_question": [
                r"آیا (.+) درست است\؟",
                r"نظر علمی درباره (.+) چیست\؟",
                r"اجماع درباره (.+) چیست\؟"
            ],
            "hypothetical_question": [
                r"اگر (.+) آنگاه (.+)\؟",
                r"چنانچه (.+) چه می‌شود\؟"
            ]
        }
    
    def analyze_question(self, question: str) -> Dict:
        """تحلیل یکپارچه سوال"""
        # تشخیص نوع سوال
        question_type = "general"
        extracted_info = {}
        
        for q_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, question)
                if match:
                    question_type = q_type
                    extracted_info = match.groups()
                    break
        
        # استخراج مفاهیم کلیدی
        concepts = self._extract_concepts(question)
        
        # تشخیص سطح پیچیدگی
        complexity = self._assess_complexity(question, concepts)
        
        return {
            "question": question,
            "type": question_type,
            "extracted_info": extracted_info,
            "concepts": concepts,
            "complexity": complexity,
            "requires": self._determine_requirements(question_type, concepts)
        }
    
    def _extract_concepts(self, text: str) -> List[Dict]:
        """استخراج مفاهیم از متن با استفاده از گراف دانش"""
        concepts = []
        words = text.replace("؟", "").replace("!", "").replace(".", "").split()
        
        # جستجوی مستقیم
        for word in words:
            if word in self.kg.concepts:
                concepts.append({
                    "concept": word,
                    "type": self.kg.concepts[word].get("type", "unknown"),
                    "confidence": 1.0
                })
        
        # جستجوی ترکیبی
        for i in range(len(words)):
            for j in range(i+1, min(i+3, len(words))):
                compound = "_".join(words[i:j])
                if compound in self.kg.concepts:
                    concepts.append({
                        "concept": compound,
                        "type": self.kg.concepts[compound].get("type", "unknown"),
                        "confidence": 0.9
                    })
        
        return concepts
    
    def _assess_complexity(self, question: str, concepts: List[Dict]) -> str:
        """ارزیابی پیچیدگی سوال"""
        word_count = len(question.split())
        concept_count = len(concepts)
        
        if word_count > 15 or concept_count > 3:
            return "high"
        elif word_count > 8 or concept_count > 1:
            return "medium"
        else:
            return "low"
    
    def _determine_requirements(self, question_type: str, concepts: List[Dict]) -> List[str]:
        """تعیین نیازمندی‌های پاسخ"""
        requirements = []
        
        if question_type == "causal_question":
            requirements.extend(["causal_analysis", "graph_traversal", "chain_inference"])
        
        if question_type == "proof_question":
            requirements.extend(["logical_inference", "consensus_check", "evidence_evaluation"])
        
        if any(concept.get("type") == "مفهوم_علمی" for concept in concepts):
            requirements.append("scientific_consensus")
        
        if any(concept.get("type") == "مفهوم_منطقی" for concept in concepts):
            requirements.append("logical_reasoning")
        
        return list(set(requirements))

# ==================== سیستم پاسخ‌دهی یکپارچه ====================

class UnifiedResponseGenerator:
    """تولیدکننده پاسخ یکپارچه"""
    
    def __init__(self, knowledge_graph: UnifiedKnowledgeGraph, language_processor: UnifiedLanguageProcessor):
        self.kg = knowledge_graph
        self.lp = language_processor
    
    def generate_response(self, question_analysis: Dict) -> str:
        """تولید پاسخ یکپارچه بر اساس تحلیل سوال"""
        question_type = question_analysis["type"]
        concepts = [c["concept"] for c in question_analysis["concepts"]]
        extracted_info = question_analysis["extracted_info"]
        
        # تولید پاسخ بر اساس نوع سوال
        response_methods = {
            "causal_question": self._answer_causal,
            "definition_question": self._answer_definition,
            "comparison_question": self._answer_comparison,
            "proof_question": self._answer_proof,
            "consensus_question": self._answer_consensus,
            "hypothetical_question": self._answer_hypothetical
        }
        
        if question_type in response_methods:
            response = response_methods[question_type](extracted_info, concepts)
        else:
            response = self._answer_general(question_analysis)
        
        # اضافه کردن تحلیل پشتیبان
        response += self._add_supporting_analysis(concepts)
        
        return response
    
    def _answer_causal(self, extracted_info: tuple, concepts: List[str]) -> str:
        """پاسخ به سوالات علّی"""
        if not extracted_info:
            return "🤔 **سوال علّی**:\n\nلطفاً پدیده‌ای را که می‌خواهید علت آن را بدانید مشخص کنید."
        
        effect = extracted_info[0].replace(" ", "_")
        
        # یافتن علل در گراف دانش
        causes = []
        for source, relations in self.kg.graph.items():
            for relation, targets in relations.items():
                if "علت" in relation:
                    for target, weight in targets:
                        if effect in target or target in effect:
                            causes.append((source, relation, weight))
        
        if causes:
            response = f"🔍 **تحلیل علّی یکپارچه**:\n\nبرای '{effect.replace('_', ' ')}'، علل احتمالی:\n\n"
            
            for cause, relation, weight in sorted(causes, key=lambda x: x[2], reverse=True)[:3]:
                response += f"• **{cause.replace('_', ' ')}** ({relation.replace('_', ' ')}) - اطمینان: {weight*100:.0f}%\n"
            
            # بررسی زنجیره‌های علّی
            chains = self.kg.infer_causal_chain(effect)
            if chains:
                response += "\n**زنجیره‌های علّی مرتبط**:\n"
                for chain in chains[:2]:
                    chain_text = " → ".join([c.replace("_", " ") for c in chain])
                    response += f"  ├─ {chain_text}\n"
        else:
            response = "🔍 **تحلیل علّی**:\n\nبرای این پدیده، رابطه علّی مستقیمی در دانش من یافت نشد.\n\n"
            response += "**روش‌های تحلیل علّی**:\n"
            response += "1. شناسایی همبستگی‌های زمانی\n"
            response += "2. بررسی مکانیسم‌های ممکن\n"
            response += "3. آزمایش‌های کنترل شده\n"
            response += "4. حذف سایر علل احتمالی\n"
        
        return response
    
    def _answer_definition(self, extracted_info: tuple, concepts: List[str]) -> str:
        """پاسخ به سوالات تعریفی"""
        if not extracted_info:
            return "📚 **سوال تعریفی**:\n\nلطفاً مفهوم مورد نظر را مشخص کنید."
        
        target_concept = extracted_info[0].replace(" ", "_")
        
        if target_concept in self.kg.concepts:
            concept_data = self.kg.concepts[target_concept]
            
            response = f"📚 **تعریف یکپارچه**:\n\n**{target_concept.replace('_', ' ')}**:\n"
            response += f"{concept_data.get('definition', 'تعریف موجود نیست')}\n\n"
            
            # ویژگی‌ها
            if "properties" in concept_data:
                response += "**ویژگی‌ها**:\n"
                for prop in concept_data["properties"]:
                    response += f"• {prop.replace('_', ' ')}\n"
            
            # روابط
            if target_concept in self.kg.graph:
                response += "\n**روابط**:\n"
                for relation, targets in self.kg.graph[target_concept].items():
                    for target, weight in targets[:2]:  # دو رابطه اول
                        response += f"• {relation.replace('_', ' ')} **{target.replace('_', ' ')}**\n"
        else:
            response = f"📚 **تحلیل مفهومی**:\n\nمفهوم '{target_concept.replace('_', ' ')}' در پایگاه دانش یکپارچه من موجود نیست.\n\n"
            response += "می‌توانم از راه‌های زیر کمک کنم:\n"
            response += "1. تحلیل اجزای کلمه\n"
            response += "2. جستجوی مفاهیم مرتبط\n"
            response += "3. استنتاج از زمینه سوال\n"
        
        return response
    
    def _answer_proof(self, extracted_info: tuple, concepts: List[str]) -> str:
        """پاسخ به سوالات اثباتی"""
        if not extracted_info:
            return "🔬 **سوال اثباتی**:\n\nلطفاً گزاره‌ای که می‌خواهید اثبات شود را مشخص کنید."
        
        statement = extracted_info[0]
        
        # بررسی اجماع
        consensus_result = self.kg.check_consensus("", statement)
        
        response = f"🔬 **روش اثبات یکپارچه**:\n\nبرای گزاره '{statement}':\n\n"
        
        if consensus_result["consensus_level"] > 0.9:
            response += "✅ **این گزاره پذیرفته شده است**\n\n"
            response += f"سطح اجماع: {consensus_result['consensus_level']*100:.0f}%\n\n"
            response += "**مراحل اثبات**:\n"
            response += "1. تعریف دقیق مفاهیم ✓\n"
            response += "2. بررسی شواهد تجربی ✓\n"
            response += "3. استدلال منطقی ✓\n"
            response += "4. بازبینی توسط جامعه علمی ✓\n"
        
        elif consensus_result["consensus_level"] > 0.7:
            response += "⚠️ **این گزاره نیاز به بررسی بیشتر دارد**\n\n"
            response += "**روش‌های ممکن اثبات**:\n"
            response += "1. اثبات ریاضی (برای گزاره‌های صوری)\n"
            response += "2. اثبات تجربی (برای گزاره‌های تجربی)\n"
            response += "3. استدلال منطقی (برای گزاره‌های تحلیلی)\n"
            response += "4. شواهد آماری (برای گزاره‌های آماری)\n"
        
        else:
            response += "❓ **این گزاره نیاز به شواهد بیشتر دارد**\n\n"
            response += "**پیشنهاد برای اثبات**:\n"
            response += "1. ارائه تعاریف دقیق\n"
            response += "2. جمع‌آوری داده‌ها\n"
            response += "3. طراحی آزمایش\n"
            response += "4. تحلیل نتایج\n"
            response += "5. بازبینی همتایان\n"
        
        return response
    
    def _answer_consensus(self, extracted_info: tuple, concepts: List[str]) -> str:
        """پاسخ به سوالات اجماع"""
        if not extracted_info:
            return "👥 **سوال اجماع**:\n\nلطفاً موضوع مورد نظر برای بررسی اجماع را مشخص کنید."
        
        topic = extracted_info[0].replace(" ", "_")
        
        # بررسی اجماع
        consensus_result = self.kg.check_consensus(topic)
        
        response = f"👥 **تحلیل اجماع یکپارچه**:\n\nبرای '{topic.replace('_', ' ')}':\n\n"
        
        if consensus_result["consensus_level"] > 0.9:
            response += "✅ **اجماع قوی وجود دارد**\n\n"
            response += f"سطح توافق: {consensus_result['consensus_level']*100:.0f}%\n"
            response += f"نوع: {consensus_result.get('type', 'ناشناخته')}\n"
            response += f"اطمینان تحلیل: {consensus_result['confidence']*100:.0f}%\n"
        
        elif consensus_result["consensus_level"] > 0.7:
            response += "⚠️ **اجماع نسبی وجود دارد**\n\n"
            response += "**نکات مهم**:\n"
            response += "• هنوز اختلاف نظرهایی وجود دارد\n"
            response += "• نیاز به شواهد بیشتر\n"
            response += "• موضوع در حال تحقیق است\n"
        
        elif consensus_result["consensus_level"] > 0.5:
            response += "🤔 **اجماع ضعیف است**\n\n"
            response += "**وضعیت**:\n"
            response += "• نظرات مختلفی وجود دارد\n"
            response += "• نیاز به تحقیقات بیشتر\n"
            response += "• موضوع پیچیده یا جدید است\n"
        
        else:
            response += "❓ **اجماع مشخصی وجود ندارد**\n\n"
            response += "**دلایل احتمالی**:\n"
            response += "1. موضوع بسیار جدید است\n"
            response += "2. شواهد کافی وجود ندارد\n"
            response += "3. نظرات کاملاً متضاد هستند\n"
            response += "4. موضوع چندوجهی و پیچیده است\n"
        
        return response
    
    def _answer_hypothetical(self, extracted_info: tuple, concepts: List[str]) -> str:
        """پاسخ به سوالات فرضی"""
        if len(extracted_info) < 2:
            return "🧪 **سوال فرضی**:\n\nلطفاً فرضیه و نتیجه مورد نظر را مشخص کنید."
        
        hypothesis = extracted_info[0].replace(" ", "_")
        consequence = extracted_info[1].replace(" ", "_") if len(extracted_info) > 1 else ""
        
        # استنتاج از گراف
        response = f"🧪 **تحلیل فرضی یکپارچه**:\n\n**فرض**: {hypothesis.replace('_', ' ')}\n"
        
        if consequence:
            response += f"**سوال**: آنگاه {consequence.replace('_', ' ')}\n\n"
        
        # بررسی مسیر در گراف
        if hypothesis in self.kg.concepts:
            # یافتن مسیرهای احتمالی
            paths = []
            if consequence:
                paths = self.kg.find_path(hypothesis, consequence)
            
            if paths:
                response += "✅ **ارتباط منطقی پیدا شد**:\n\n"
                for path in paths[:2]:  # دو مسیر اول
                    response += "مسیر:\n"
                    for step in path:
                        source, relation, target = step
                        response += f"  {source.replace('_', ' ')} → {relation.replace('_', ' ')} → {target.replace('_', ' ')}\n"
                    response += "\n"
            else:
                response += "🔍 **تحلیل فرضی**:\n\n"
                response += "برای تحلیل این فرضیه:\n\n"
                response += "1. **تعریف متغیرها**: مشخص کردن دقیق مفاهیم\n"
                response += "2. **بررسی پیش‌نیازها**: شرایط لازم برای فرض\n"
                response += "3. **استنتاج منطقی**: استفاده از قواعد استنتاج\n"
                response += "4. **بررسی نتایج**: تحلیل پیامدهای فرض\n"
        else:
            response += "🔍 **تحلیل فرضی**:\n\n"
            response += "برای تحلیل فرضیه‌ها به اطلاعات بیشتری نیاز دارم:\n\n"
            response += "• تعریف دقیق فرض\n"
            response += "• زمینه و شرایط\n"
            response += "• مفاهیم به کار رفته\n"
        
        return response
    
    def _answer_comparison(self, extracted_info: tuple, concepts: List[str]) -> str:
        """پاسخ به سوالات مقایسه‌ای"""
        if len(extracted_info) < 2:
            return "⚖️ **سوال مقایسه‌ای**:\n\nلطفاً دو چیزی که می‌خواهید مقایسه شوند را مشخص کنید."
        
        item1 = extracted_info[0].replace(" ", "_")
        item2 = extracted_info[1].replace(" ", "_")
        
        response = f"⚖️ **تحلیل مقایسه‌ای یکپارچه**:\n\n"
        response += f"مقایسه **{item1.replace('_', ' ')}** و **{item2.replace('_', ' ')}**:\n\n"
        
        # جمع‌آوری اطلاعات هر کدام
        info1 = self.kg.concepts.get(item1, {})
        info2 = self.kg.concepts.get(item2, {})
        
        # مقایسه ویژگی‌ها
        comparison_points = []
        
        if info1 and info2:
            # تعریف
            if "definition" in info1 and "definition" in info2:
                comparison_points.append(("تعریف", info1["definition"], info2["definition"]))
            
            # نوع
            if "type" in info1 and "type" in info2:
                comparison_points.append(("نوع", info1["type"], info2["type"]))
            
            # ویژگی‌ها
            if "properties" in info1 and "properties" in info2:
                common = set(info1["properties"]).intersection(set(info2["properties"]))
                unique1 = set(info1["properties"]) - set(info2["properties"])
                unique2 = set(info2["properties"]) - set(info1["properties"])
                
                comparison_points.append(("ویژگی‌های مشترک", ", ".join(common), ", ".join(common)))
                comparison_points.append(("ویژگی‌های منحصر به فرد اولی", ", ".join(unique1), ""))
                comparison_points.append(("ویژگی‌های منحصر به فرد دومی", "", ", ".join(unique2)))
        
        if comparison_points:
            response += "**جدول مقایسه**:\n\n"
            response += "| معیار | اولی | دومی |\n"
            response += "|-------|------|------|\n"
            
            for point, val1, val2 in comparison_points:
                val1_display = str(val1)[:30] + "..." if len(str(val1)) > 30 else str(val1)
                val2_display = str(val2)[:30] + "..." if len(str(val2)) > 30 else str(val2)
                response += f"| {point} | {val1_display} | {val2_display} |\n"
        else:
            response += "**تحلیل مقایسه**:\n\n"
            response += "برای مقایسه دقیق‌تر:\n"
            response += "1. تعریف مشخص از هر دو مفهوم\n"
            response += "2. معیارهای مقایسه\n"
            response += "3. زمینه و کاربرد\n"
            response += "4. شباهت‌ها و تفاوت‌های کلیدی\n"
        
        return response
    
    def _answer_general(self, question_analysis: Dict) -> str:
        """پاسخ به سوالات عمومی"""
        concepts = [c["concept"] for c in question_analysis["concepts"]]
        
        response = "🧠 **تحلیل یکپارچه**:\n\n"
        
        if concepts:
            response += f"سوال شما شامل مفاهیم: {', '.join([c.replace('_', ' ') for c in concepts])}\n\n"
            
            # ارائه اطلاعات درباره اولین مفهوم
            main_concept = concepts[0]
            if main_concept in self.kg.concepts:
                concept_data = self.kg.concepts[main_concept]
                
                if "definition" in concept_data:
                    response += f"**{main_concept.replace('_', ' ')}**: {concept_data['definition']}\n\n"
                
                # روابط
                if main_concept in self.kg.graph:
                    response += "**برخی روابط**:\n"
                    relations = list(self.kg.graph[main_concept].items())[:3]
                    for relation, targets in relations:
                        for target, weight in targets[:2]:
                            response += f"• {relation.replace('_', ' ')} **{target.replace('_', ' ')}**\n"
        else:
            response += "سوال شما نیاز به تحلیل عمیق‌تری دارد.\n\n"
            response += "**سیستم من می‌تواند**:\n"
            response += "1. تحلیل مفاهیم و روابط آنها\n"
            response += "2. استنتاج منطقی از اطلاعات\n"
            response += "3. بررسی روابط علّی\n"
            response += "4. تحلیل اجماع و شواهد\n\n"
            response += "لطفاً سوال خود را به صورت مشخص‌تر مطرح کنید."
        
        return response
    
    def _add_supporting_analysis(self, concepts: List[str]) -> str:
        """اضافه کردن تحلیل پشتیبان"""
        if not concepts:
            return ""
        
        analysis = "\n\n---\n**تحلیل پشتیبان**:\n"
        
        for concept in concepts[:2]:  # برای دو مفهوم اول
            if concept in self.kg.concepts:
                concept_data = self.kg.concepts[concept]
                
                # اجماع
                consensus = concept_data.get("consensus", 0.5)
                if consensus > 0.8:
                    analysis += f"\n• **{concept.replace('_', ' ')}** دارای اجماع قوی ({consensus*100:.0f}%) است"
                elif consensus > 0.6:
                    analysis += f"\n• **{concept.replace('_', ' ')}** اجماع متوسط دارد"
                
                # روابط کلیدی
                if concept in self.kg.graph:
                    key_relations = []
                    for relation, targets in self.kg.graph[concept].items():
                        if targets:
                            key_relations.append(f"{relation.replace('_', ' ')} {targets[0][0].replace('_', ' ')}")
                    
                    if key_relations:
                        analysis += f"\n• روابط کلیدی: {', '.join(key_relations[:2])}"
        
        return analysis

# ==================== سیستم اصلی یکپارچه ====================

class UnifiedNatiqSystem:
    """سیستم اصلی یکپارچه natiq"""
    
    def __init__(self):
        # ایجاد اجزای یکپارچه
        self.knowledge_graph = UnifiedKnowledgeGraph()
        self.language_processor = UnifiedLanguageProcessor(self.knowledge_graph)
        self.response_generator = UnifiedResponseGenerator(self.knowledge_graph, self.language_processor)
        
        # آمار و تاریخچه
        self.session_stats = {
            "total_questions": 0,
            "question_types": defaultdict(int),
            "concepts_used": set(),
            "reasoning_depth": []
        }
    
    def process(self, question: str) -> Dict:
        """پردازش کامل یک سوال"""
        self.session_stats["total_questions"] += 1
        
        # تحلیل سوال
        analysis = self.language_processor.analyze_question(question)
        
        # ثبت آمار
        self.session_stats["question_types"][analysis["type"]] += 1
        for concept in analysis["concepts"]:
            self.session_stats["concepts_used"].add(concept["concept"])
        
        # تولید پاسخ
        response = self.response_generator.generate_response(analysis)
        
        # ارزیابی عمق استدلال
        reasoning_depth = self._evaluate_reasoning_depth(analysis, response)
        self.session_stats["reasoning_depth"].append(reasoning_depth)
        
        return {
            "question": question,
            "analysis": analysis,
            "response": response,
            "stats": {
                "session_total": self.session_stats["total_questions"],
                "question_type": analysis["type"],
                "concepts_count": len(analysis["concepts"]),
                "reasoning_depth": reasoning_depth,
                "unified_system": True
            },
            "system_info": {
                "version": "5.0.0",
                "architecture": "unified_knowledge_graph",
                "components": ["knowledge_graph", "language_processor", "response_generator"]
            }
        }
    
    def _evaluate_reasoning_depth(self, analysis: Dict, response: str) -> str:
        """ارزیابی عمق استدلال استفاده شده"""
        concepts_count = len(analysis["concepts"])
        response_length = len(response)
        
        if concepts_count >= 3 and response_length > 500:
            return "deep"
        elif concepts_count >= 2 and response_length > 300:
            return "medium"
        else:
            return "basic"

# ایجاد نمونه سیستم
unified_system = UnifiedNatiqSystem()

# ==================== API Endpoints ====================

@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 natiq-ultimate v5.0 | سیستم یکپارچه مبتنی بر گراف دانش</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Vazirmatn', system-ui, sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #f1f5f9;
                min-height: 100vh;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: rgba(30, 41, 59, 0.95);
                min-height: 100vh;
                box-shadow: 0 0 50px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* هدر */
            .header {
                background: linear-gradient(90deg, #1e40af, #3b82f6);
                padding: 25px 40px;
                border-bottom: 3px solid #60a5fa;
                position: relative;
                overflow: hidden;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path fill="rgba(255,255,255,0.05)" d="M0,0 L100,100 M100,0 L0,100"/></svg>');
                background-size: 50px;
                opacity: 0.3;
            }
            
            .header-content {
                position: relative;
                z-index: 1;
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
            
            .logo-icon {
                font-size: 3.5em;
                color: #93c5fd;
                filter: drop-shadow(0 0 10px rgba(147, 197, 253, 0.5));
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { filter: drop-shadow(0 0 10px rgba(147, 197, 253, 0.5)); }
                to { filter: drop-shadow(0 0 20px rgba(147, 197, 253, 0.8)); }
            }
            
            .logo-text h1 {
                font-size: 2.4em;
                font-weight: 800;
                background: linear-gradient(45deg, #93c5fd, #60a5fa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 2px 10px rgba(96, 165, 250, 0.3);
            }
            
            .logo-text .subtitle {
                font-size: 0.9em;
                opacity: 0.9;
                margin-top: 5px;
                color: #cbd5e1;
            }
            
            .system-badge {
                background: rgba(96, 165, 250, 0.2);
                border: 2px solid #60a5fa;
                padding: 10px 25px;
                border-radius: 30px;
                font-weight: bold;
                font-size: 1.1em;
                backdrop-filter: blur(5px);
                box-shadow: 0 5px 15px rgba(96, 165, 250, 0.2);
            }
            
            /* محتوای اصلی */
            .main-content {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 0;
                min-height: 80vh;
            }
            
            /* پنل چت */
            .chat-panel {
                background: rgba(15, 23, 42, 0.7);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                flex-direction: column;
            }
            
            .messages-container {
                flex: 1;
                overflow-y: auto;
                padding: 30px;
                background: linear-gradient(180deg, 
                    rgba(15, 23, 42, 0.9) 0%,
                    rgba(15, 23, 42, 0.7) 100%);
            }
            
            .message {
                margin: 20px 0;
                padding: 25px;
                border-radius: 20px;
                max-width: 90%;
                position: relative;
                animation: slideIn 0.4s cubic-bezier(0.18, 0.89, 0.32, 1.28);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            }
            
            @keyframes slideIn {
                from { 
                    opacity: 0;
                    transform: translateY(30px) scale(0.95);
                }
                to { 
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .user-message {
                background: linear-gradient(135deg, 
                    rgba(59, 130, 246, 0.3), 
                    rgba(37, 99, 235, 0.3));
                margin-left: auto;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                border-right: 4px solid #3b82f6;
            }
            
            .bot-message {
                background: linear-gradient(135deg,
                    rgba(30, 41, 59, 0.8),
                    rgba(15, 23, 42, 0.9));
                margin-right: auto;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
                border-left: 4px solid #60a5fa;
            }
            
            .message-header {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 15px;
                padding-bottom: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .message-icon {
                font-size: 1.8em;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.1);
            }
            
            .message-type {
                font-weight: bold;
                font-size: 0.95em;
                color: #93c5fd;
            }
            
            .message-content {
                white-space: pre-wrap;
                line-height: 1.8;
                font-size: 1.05em;
                color: #e2e8f0;
            }
            
            .message-time {
                font-size: 0.8em;
                opacity: 0.7;
                margin-top: 15px;
                text-align: left;
                color: #94a3b8;
            }
            
            /* ورودی */
            .input-panel {
                background: rgba(15, 23, 42, 0.9);
                padding: 25px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .input-group {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
            }
            
            #messageInput {
                flex: 1;
                padding: 18px 25px;
                background: rgba(30, 41, 59, 0.8);
                border: 2px solid rgba(96, 165, 250, 0.3);
                border-radius: 15px;
                font-size: 1.1em;
                font-family: inherit;
                color: #f1f5f9;
                transition: all 0.3s;
            }
            
            #messageInput:focus {
                outline: none;
                border-color: #60a5fa;
                background: rgba(30, 41, 59, 0.9);
                box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
            }
            
            #sendButton {
                width: 65px;
                background: linear-gradient(45deg, #3b82f6, #2563eb);
                color: white;
                border: none;
                border-radius: 15px;
                cursor: pointer;
                font-size: 1.3em;
                transition: all 0.3s;
            }
            
            #sendButton:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
            }
            
            /* پنل دانش */
            .knowledge-panel {
                background: rgba(15, 23, 42, 0.9);
                padding: 25px;
                overflow-y: auto;
                border-left: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .panel-section {
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .panel-section h3 {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
                color: #60a5fa;
                font-size: 1.1em;
            }
            
            .section-icon {
                font-size: 1.2em;
            }
            
            .concept-tag {
                display: inline-block;
                background: rgba(96, 165, 250, 0.2);
                color: #93c5fd;
                padding: 8px 15px;
                border-radius: 20px;
                margin: 5px;
                font-size: 0.85em;
                border: 1px solid rgba(96, 165, 250, 0.3);
                transition: all 0.3s;
            }
            
            .concept-tag:hover {
                background: rgba(96, 165, 250, 0.3);
                transform: translateY(-2px);
            }
            
            .stat-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-top: 15px;
            }
            
            .stat-item {
                background: rgba(30, 41, 59, 0.8);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .stat-value {
                font-size: 1.8em;
                font-weight: bold;
                color: #60a5fa;
                margin-bottom: 5px;
            }
            
            .stat-label {
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            .knowledge-structure {
                background: rgba(30, 41, 59, 0.6);
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
                font-size: 0.9em;
                line-height: 1.6;
            }
            
            /* دکمه‌های نمونه */
            .sample-questions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 12px;
                margin-top: 20px;
            }
            
            .sample-btn {
                padding: 15px;
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(96, 165, 250, 0.3);
                border-radius: 12px;
                color: #e2e8f0;
                cursor: pointer;
                transition: all 0.3s;
                text-align: center;
                font-size: 0.9em;
            }
            
            .sample-btn:hover {
                background: rgba(96, 165, 250, 0.2);
                border-color: #60a5fa;
                transform: translateY(-3px);
            }
            
            /* پیام خوش‌آمدگویی */
            .welcome-message {
                background: linear-gradient(135deg, 
                    rgba(59, 130, 246, 0.3), 
                    rgba(37, 99, 235, 0.3));
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 30px;
                border: 1px solid rgba(96, 165, 250, 0.3);
                backdrop-filter: blur(10px);
            }
            
            .welcome-message h2 {
                color: #93c5fd;
                margin-bottom: 15px;
                font-size: 1.6em;
            }
            
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin: 20px 0;
            }
            
            .feature {
                background: rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                backdrop-filter: blur(5px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: transform 0.3s;
            }
            
            .feature:hover {
                transform: translateY(-5px);
                border-color: rgba(96, 165, 250, 0.5);
            }
            
            .feature i {
                font-size: 2em;
                color: #60a5fa;
                margin-bottom: 10px;
                display: block;
            }
            
            /* responsive */
            @media (max-width: 1024px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
                
                .knowledge-panel {
                    border-left: none;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
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
                
                .feature-grid {
                    grid-template-columns: 1fr;
                }
                
                .sample-questions {
                    grid-template-columns: 1fr;
                }
                
                .stat-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            /* اسکرول بار سفارشی */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(30, 41, 59, 0.5);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: rgba(96, 165, 250, 0.5);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(96, 165, 250, 0.7);
            }
        </style>
        
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <!-- Google Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <script>
            class NatiqUnifiedApp {
                constructor() {
                    this.sessionId = 'unified_' + Date.now();
                    this.baseUrl = window.location.origin;
                    this.messageCount = 0;
                    this.conceptsUsed = new Set();
                    this.init();
                }
                
                init() {
                    console.log('🧠 natiq-ultimate v5.0 - سیستم یکپارچه مبتنی بر گراف دانش');
                    this.setupEventListeners();
                    this.updateStatus('🔄 سیستم یکپارچه فعال');
                    this.updateSystemInfo();
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
                    
                    // دکمه‌های نمونه
                    document.querySelectorAll('.sample-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            const question = e.target.getAttribute('data-question');
                            if (question) {
                                document.getElementById('messageInput').value = question;
                                this.sendMessage();
                            }
                        });
                    });
                }
                
                updateStatus(message) {
                    const statusElement = document.getElementById('systemStatus');
                    if (statusElement) {
                        statusElement.textContent = message;
                    }
                }
                
                updateSystemInfo() {
                    // به‌روزرسانی اطلاعات سیستم
                    const now = new Date();
                    document.getElementById('currentTime').textContent = 
                        now.toLocaleTimeString('fa-IR');
                    
                    document.getElementById('sessionIdDisplay').textContent = 
                        this.sessionId.substring(0, 12) + '...';
                }
                
                async sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (!message) return;
                    
                    // نمایش پیام کاربر
                    this.addMessage(message, 'user', 'سوال شما');
                    messageInput.value = '';
                    this.messageCount++;
                    
                    // نمایش حالت پردازش
                    this.showProcessing();
                    
                    try {
                        const response = await fetch(this.baseUrl + '/api/unified/' + this.sessionId, {
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
                        
                        this.hideProcessing();
                        
                        // نمایش پاسخ
                        this.addMessage(data.response, 'bot', 'تحلیل یکپارچه');
                        
                        // به‌روزرسانی پنل دانش
                        this.updateKnowledgePanel(data.analysis, data.stats);
                        
                        this.updateStatus('✅ تحلیل کامل شد');
                        
                    } catch (error) {
                        this.hideProcessing();
                        console.error('❌ خطا:', error);
                        
                        this.addMessage('⚠️ خطا در پردازش یکپارچه. لطفاً دوباره تلاش کنید.', 'error', 'خطا');
                        this.updateStatus('❌ خطا در پردازش');
                    }
                }
                
                addMessage(text, type, header = '') {
                    const messagesDiv = document.getElementById('messages');
                    const time = new Date().toLocaleTimeString('fa-IR', {
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                    
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${type}-message`;
                    
                    const icon = type === 'user' ? '👤' : 
                                 type === 'error' ? '⚠️' : '🧠';
                    
                    const headerText = header || (type === 'user' ? 'سوال شما' : 'تحلیل یکپارچه');
                    
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
                
                showProcessing() {
                    const messagesDiv = document.getElementById('messages');
                    
                    const processingDiv = document.createElement('div');
                    processingDiv.className = 'message bot-message';
                    processingDiv.id = 'processingIndicator';
                    processingDiv.innerHTML = `
                        <div class="message-header">
                            <div class="message-icon">⚡</div>
                            <div class="message-type">در حال پردازش یکپارچه</div>
                        </div>
                        <div class="message-content">
                            <div style="display: flex; align-items: center; gap: 15px; padding: 10px 0;">
                                <div style="display: flex; gap: 8px;">
                                    <span style="animation: pulse 1s infinite; color: #60a5fa;">●</span>
                                    <span style="animation: pulse 1s infinite 0.2s; color: #3b82f6;">●</span>
                                    <span style="animation: pulse 1s infinite 0.4s; color: #2563eb;">●</span>
                                </div>
                                <div style="flex: 1;">
                                    در حال تحلیل با گراف دانش یکپارچه...
                                </div>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(processingDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                hideProcessing() {
                    const processing = document.getElementById('processingIndicator');
                    if (processing) {
                        processing.remove();
                    }
                }
                
                updateKnowledgePanel(analysis, stats) {
                    // به‌روزرسانی مفاهیم
                    const conceptsDiv = document.getElementById('conceptsList');
                    if (conceptsDiv && analysis.concepts) {
                        conceptsDiv.innerHTML = '';
                        analysis.concepts.forEach(concept => {
                            const span = document.createElement('span');
                            span.className = 'concept-tag';
                            span.textContent = concept.concept.replace(/_/g, ' ');
                            conceptsDiv.appendChild(span);
                            
                            // ذخیره برای آمار
                            this.conceptsUsed.add(concept.concept);
                        });
                    }
                    
                    // به‌روزرسانی آمار
                    document.getElementById('questionsCount').textContent = this.messageCount;
                    document.getElementById('conceptsCount').textContent = this.conceptsUsed.size;
                    document.getElementById('reasoningDepth').textContent = stats.reasoning_depth || 'متوسط';
                    
                    // به‌روزرسانی نوع سوال
                    const questionTypeDiv = document.getElementById('questionType');
                    if (questionTypeDiv && analysis.type) {
                        questionTypeDiv.textContent = analysis.type.replace(/_/g, ' ');
                    }
                }
                
                escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }
            }
            
            // راه‌اندازی اپ
            document.addEventListener('DOMContentLoaded', () => {
                window.natiqApp = new NatiqUnifiedApp();
                document.getElementById('messageInput').focus();
                
                // نمایش پیام خوش‌آمدگویی
                setTimeout(() => {
                    const welcomeMsg = `🧠 **به natiq-ultimate نسخه ۵.۰ خوش آمدید!**\n\nاین سیستم از یک **گراف دانش یکپارچه** استفاده می‌کند که:\n\n✅ همه مفاهیم در یک ساختار مرتبط هستند\n✅ استنتاج‌ها از روابط مستقیم گراف می‌آیند\n✅ تحلیل علّی، اجماع و منطق همگی یکپارچه کار می‌کنند\n✅ پاسخ‌ها مبتنی بر روابط واقعی بین مفاهیم هستند\n\nلطفاً سوالی بپرسید تا سیستم یکپارچه را تست کنید!`;
                    window.natiqApp.addMessage(welcomeMsg, 'bot', 'سیستم یکپارچه');
                }, 500);
            });
            
            // توابع کمکی
            function clearChat() {
                if (confirm('آیا مطمئن هستید که می‌خواهید همه گفتگو را پاک کنید؟')) {
                    const messagesDiv = document.getElementById('messages');
                    const welcomeDiv = messagesDiv.querySelector('.welcome-message');
                    
                    while (messagesDiv.firstChild) {
                        messagesDiv.removeChild(messagesDiv.firstChild);
                    }
                    
                    if (welcomeDiv) {
                        messagesDiv.appendChild(welcomeDiv);
                    }
                    
                    window.natiqApp.messageCount = 0;
                    window.natiqApp.conceptsUsed.clear();
                    window.natiqApp.updateStatus('🗑️ گفتگو پاک شد');
                    
                    // پاک کردن پنل دانش
                    document.getElementById('conceptsList').innerHTML = 
                        '<span style="opacity:0.7">هنوز مفهومی استخراج نشده</span>';
                    document.getElementById('questionsCount').textContent = '0';
                    document.getElementById('conceptsCount').textContent = '0';
                    document.getElementById('questionType').textContent = '--';
                }
            }
            
            function testSystemCapabilities() {
                const tests = [
                    "هوش مصنوعی چیست؟",
                    "چرا آسمان آبی است؟",
                    "اثبات کن زمین گرد است",
                    "تفاوت علت و معلول با همبستگی چیست؟",
                    "آیا اجماع علمی درباره تغییرات اقلیمی وجود دارد؟"
                ];
                
                tests.forEach((question, index) => {
                    setTimeout(() => {
                        document.getElementById('messageInput').value = question;
                        window.natiqApp.sendMessage();
                    }, index * 3000);
                });
            }
        </script>
    </head>
    <body>
        <div class="container">
            <!-- هدر -->
            <header class="header">
                <div class="header-content">
                    <div class="logo">
                        <div class="logo-icon">
                            <i class="fas fa-project-diagram"></i>
                        </div>
                        <div class="logo-text">
                            <h1>natiq-ultimate</h1>
                            <div class="subtitle">سیستم یکپارچه مبتنی بر گراف دانش</div>
                        </div>
                    </div>
                    
                    <div class="system-badge">
                        نسخه ۵.۰
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div style="width: 10px; height: 10px; background: #10b981; border-radius: 50%; animation: pulse 2s infinite;"></div>
                            <span id="systemStatus">در حال راه‌اندازی...</span>
                        </div>
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
                            <h2>🌐 معماری یکپارچه فعال شد</h2>
                            <p>این سیستم از یک گراف دانش یکپارچه استفاده می‌کند که همه مفاهیم، روابط، قواعد استنتاج و سطوح اجماع در یک ساختار منسجم قرار دارند.</p>
                            
                            <div class="feature-grid">
                                <div class="feature">
                                    <i class="fas fa-network-wired"></i>
                                    <div>گراف دانش یکپارچه</div>
                                    <small>همه مفاهیم مرتبط</small>
                                </div>
                                <div class="feature">
                                    <i class="fas fa-random"></i>
                                    <div>استنتاج یکپارچه</div>
                                    <small>از روابط مستقیم</small>
                                </div>
                                <div class="feature">
                                    <i class="fas fa-link"></i>
                                    <div>روابط علّی واقعی</div>
                                    <small>در خود گراف</small>
                                </div>
                                <div class="feature">
                                    <i class="fas fa-handshake"></i>
                                    <div>اجماع یکپارچه</div>
                                    <small>به عنوان ویژگی مفاهیم</small>
                                </div>
                            </div>
                            
                            <p style="margin-top: 15px; font-size: 0.9em; color: #cbd5e1;">
                                <strong>✨ تفاوت کلیدی:</strong> دیگر ماژول‌های جداگانه وجود ندارند. همه چیز در یک ساختار واحد و هماهنگ کار می‌کند.
                            </p>
                        </div>
                    </div>
                    
                    <!-- پنل ورودی -->
                    <div class="input-panel">
                        <div class="input-group">
                            <input 
                                type="text" 
                                id="messageInput" 
                                placeholder="هر نوع سوالی بپرسید (سیستم به صورت یکپارچه تحلیل می‌کند)..." 
                                autocomplete="off"
                                autofocus
                            >
                            <button id="sendButton">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        
                        <div class="sample-questions">
                            <button class="sample-btn" data-question="هوش مصنوعی چیست؟">
                                <i class="fas fa-brain"></i> سوال تعریفی
                            </button>
                            <button class="sample-btn" data-question="چرا آسمان آبی است؟">
                                <i class="fas fa-question-circle"></i> سوال علّی
                            </button>
                            <button class="sample-btn" data-question="اثبات کن زمین گرد است">
                                <i class="fas fa-calculator"></i> سوال اثباتی
                            </button>
                            <button class="sample-btn" data-question="تفاوت هوش مصنوعی و یادگیری ماشین چیست؟">
                                <i class="fas fa-balance-scale"></i> سوال مقایسه‌ای
                            </button>
                            <button class="sample-btn" onclick="testSystemCapabilities()">
                                <i class="fas fa-vial"></i> تست کامل سیستم
                            </button>
                            <button class="sample-btn" onclick="clearChat()">
                                <i class="fas fa-trash"></i> پاک کردن همه
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- پنل دانش -->
                <div class="knowledge-panel">
                    <div class="panel-section">
                        <h3><i class="fas fa-chart-bar section-icon"></i> آمار جلسه</h3>
                        <div class="stat-grid">
                            <div class="stat-item">
                                <div class="stat-value" id="questionsCount">0</div>
                                <div class="stat-label">سوالات</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value" id="conceptsCount">0</div>
                                <div class="stat-label">مفاهیم</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value" id="reasoningDepth">--</div>
                                <div class="stat-label">عمق استدلال</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">۵.۰</div>
                                <div class="stat-label">نسخه</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-lightbulb section-icon"></i> مفاهیم استخراج شده</h3>
                        <div id="conceptsList" style="min-height: 80px; padding: 10px; background: rgba(30,41,59,0.5); border-radius: 8px;">
                            <span style="opacity: 0.7; font-size: 0.9em;">هنوز مفهومی استخراج نشده</span>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-filter section-icon"></i> نوع سوال</h3>
                        <div style="padding: 15px; background: rgba(30,41,59,0.6); border-radius: 8px; text-align: center;">
                            <span style="font-size: 1.1em; color: #60a5fa;" id="questionType">--</span>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-sitemap section-icon"></i> ساختار دانش</h3>
                        <div class="knowledge-structure">
                            <p><strong>گراف دانش یکپارچه شامل:</strong></p>
                            <ul style="padding-right: 20px; margin-top: 10px;">
                                <li>مفاهیم با ویژگی‌های کامل</li>
                                <li>روابط مستقیم بین مفاهیم</li>
                                <li>زنجیره‌های علّی از پیش تعریف شده</li>
                                <li>سطوح اجماع به عنوان ویژگی</li>
                                <li>قواعد استنتاج یکپارچه</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-info-circle section-icon"></i> اطلاعات سیستم</h3>
                        <div class="knowledge-structure">
                            <p><strong>شناسه جلسه:</strong> <span id="sessionIdDisplay">...</span></p>
                            <p><strong>زمان کنونی:</strong> <span id="currentTime">--:--</span></p>
                            <p><strong>وضعیت:</strong> <span id="systemStatusText">فعال</span></p>
                            <p><strong>معماری:</strong> یکپارچه مبتنی بر گراف</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

# ==================== API Endpoints ====================

@app.get("/api/health")
async def health_check():
    return {
        "status": "unified_system_active",
        "system": "natiq-ultimate",
        "version": "5.0.0",
        "architecture": "unified_knowledge_graph",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "knowledge_graph": {
                "concepts_count": len(unified_system.knowledge_graph.concepts),
                "relations_count": sum(len(rels) for rels in unified_system.knowledge_graph.graph.values()),
                "rules_count": len(unified_system.knowledge_graph.rules)
            },
            "language_processor": "unified",
            "response_generator": "integrated"
        },
        "capabilities": [
            "تحلیل یکپارچه سوالات",
            "استنتاج از گراف دانش",
            "تحلیل روابط علّی مستقیم",
            "بررسی اجماع به عنوان ویژگی",
            "پاسخ‌دهی مبتنی بر روابط واقعی"
        ]
    }

@app.post("/api/unified/{session_id}")
async def unified_endpoint(session_id: str, request: dict):
    """اندپوینت یکپارچه اصلی"""
    try:
        question = request.get("message", "")
        
        if not question or question.strip() == "":
            raise HTTPException(status_code=400, detail="سوال نمی‌تواند خالی باشد")
        
        # پردازش با سیستم یکپارچه
        result = unified_system.process(question)
        
        return {
            "session_id": session_id,
            "question": question,
            "response": result["response"],
            "analysis": result["analysis"],
            "stats": result["stats"],
            "system_info": result["system_info"],
            "timestamp": datetime.now().isoformat(),
            "version": "5.0.0"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "خطا در پردازش یکپارچه",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/knowledge/stats")
async def knowledge_stats():
    """آمار گراف دانش"""
    kg = unified_system.knowledge_graph
    
    return {
        "concepts_total": len(kg.concepts),
        "graph_relations": sum(len(rels) for rels in kg.graph.values()),
        "causal_chains": len(kg.causal_chains),
        "inference_rules": len(kg.rules),
        "consensus_levels": len(kg.consensus_levels),
        "sample_concepts": list(kg.concepts.keys())[:10]
    }

@app.get("/api/debug/unified")
async def debug_unified():
    """اطلاعات دیباگ سیستم یکپارچه"""
    return {
        "system": "natiq-ultimate-unified",
        "version": "5.0.0",
        "session_stats": unified_system.session_stats,
        "knowledge_graph": {
            "size": len(unified_system.knowledge_graph.concepts),
            "sample_concept": next(iter(unified_system.knowledge_graph.concepts.items()), ("none", {}))[0]
        },
        "architecture": "fully_unified_knowledge_graph",
        "integration_level": "complete"
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
