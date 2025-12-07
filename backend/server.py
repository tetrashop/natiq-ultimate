#!/usr/bin/env python3
"""
natiq-ultimate - سیستم یکپارچه عصبی-نمادین
نسخه 6.0: ترکیب یادگیری عمیق، کتابخانه‌ای و گراف دانش
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import json
import re
import numpy as np
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
import hashlib
import pickle
import random

app = FastAPI(
    title="natiq-ultimate",
    description="سیستم عصبی-نمادین یکپارچه با یادگیری عمیق و کتابخانه‌ای",
    version="6.0.0"
)

# CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== سیستم یادگیری عمیق (شبیه‌سازی) ====================

class DeepLearningNLP:
    """سیستم پردازش زبان طبیعی مبتنی بر یادگیری عمیق"""
    
    def __init__(self):
        self.word_vectors = {}  # بردارهای کلمات (شبیه‌سازی)
        self.model_state = "trained"
        self.initialize_embeddings()
    
    def initialize_embeddings(self):
        """شبیه‌سازی embeddingهای اولیه"""
        # کلمات فارسی متداول
        common_words = [
            "هوش", "مصنوعی", "یادگیری", "ماشین", "داده", "الگوریتم",
            "علت", "معلول", "اجماع", "تحلیل", "استنتاج", "منطق",
            "برنامه", "نویسی", "پایتون", "شبکه", "عصبی", "مدل"
        ]
        
        for i, word in enumerate(common_words):
            # ایجاد بردار 50 بعدی شبیه‌سازی شده
            vector = np.random.randn(50)
            # نرمال‌سازی
            vector = vector / np.linalg.norm(vector)
            self.word_vectors[word] = vector
    
    def get_sentence_embedding(self, text: str) -> np.ndarray:
        """ایجاد embedding برای جمله"""
        words = text.split()
        vectors = []
        
        for word in words:
            if word in self.word_vectors:
                vectors.append(self.word_vectors[word])
            else:
                # بردار تصادفی برای کلمات ناشناخته
                vec = np.random.randn(50)
                vec = vec / np.linalg.norm(vec)
                vectors.append(vec)
        
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(50)
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """محاسبه شباهت معنایی"""
        vec1 = self.get_sentence_embedding(text1)
        vec2 = self.get_sentence_embedding(text2)
        
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(similarity)
    
    def classify_intent(self, text: str) -> Dict:
        """طبقه‌بندی هدف سوال با شبکه عصبی شبیه‌سازی شده"""
        # شبیه‌سازی یک شبکه عصبی ساده
        text_lower = text.lower()
        
        intents = {
            "definition": ["چیست", "چیه", "تعریف", "منظور"],
            "causal": ["چرا", "علت", "دلیل", "چرایی"],
            "comparison": ["تفاوت", "فرق", "مقایسه"],
            "proof": ["اثبات", "ثابت", "نشان"],
            "howto": ["چگونه", "چطور", "روش"],
            "consensus": ["اجماع", "نظر", "توافق"]
        }
        
        scores = {}
        for intent, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[intent] = score / max(len(keywords), 1)
        
        # افزودن نویز شبیه‌سازی شده
        for intent in scores:
            scores[intent] += np.random.uniform(-0.1, 0.1)
            scores[intent] = max(0, min(1, scores[intent]))
        
        primary_intent = max(scores.items(), key=lambda x: x[1])
        
        return {
            "primary": primary_intent[0],
            "confidence": primary_intent[1],
            "all_scores": scores
        }
    
    def extract_entities_deep(self, text: str) -> List[Dict]:
        """استخراج موجودیت‌ها با یادگیری عمیق شبیه‌سازی شده"""
        entities = []
        words = text.split()
        
        # الگوهای شبیه‌سازی شده از مدل NER
        patterns = {
            "CONCEPT": ["هوش", "یادگیری", "الگوریتم", "مدل", "شبکه"],
            "TECH": ["پایتون", "تنسورفلو", "پایتورچ", "آی‌آی"],
            "PERSON": ["علی", "مریم", "انیشتین", "تورینگ"],
            "ORG": ["دانشگاه", "شرکت", "آزمایشگاه", "مرکز"],
            "ACTION": ["یادگیری", "آموزش", "تحلیل", "پردازش"]
        }
        
        for i, word in enumerate(words):
            for entity_type, keywords in patterns.items():
                if word in keywords:
                    entities.append({
                        "entity": word,
                        "type": entity_type,
                        "start": i,
                        "end": i + 1,
                        "confidence": np.random.uniform(0.7, 0.95)
                    })
        
        return entities

# ==================== سیستم یادگیری کتابخانه‌ای ====================

class LibraryLearning:
    """سیستم یادگیری از کتابخانه‌ها و منابع خارجی"""
    
    def __init__(self):
        self.knowledge_sources = self.initialize_sources()
        self.cache = {}
    
    def initialize_sources(self):
        """شبیه‌سازی منابع دانش"""
        return {
            "wikipedia": {
                "name": "ویکی‌پدیا فارسی",
                "coverage": "عمومی",
                "access": "simulated"
            },
            "conceptnet": {
                "name": "ConceptNet",
                "coverage": "روابط مفهومی",
                "access": "simulated"
            },
            "arxiv": {
                "name": "arXiv مقالات علمی",
                "coverage": "علمی",
                "access": "simulated"
            },
            "persian_corpus": {
                "name": "پیکره متون فارسی",
                "coverage": "زبان فارسی",
                "access": "simulated"
            }
        }
    
    def search_wikipedia(self, query: str) -> Dict:
        """جستجوی شبیه‌سازی شده در ویکی‌پدیا"""
        cache_key = f"wikipedia_{hashlib.md5(query.encode()).hexdigest()}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # شبیه‌سازی داده‌های ویکی‌پدیا
        simulated_data = {
            "query": query,
            "results": [],
            "source": "wikipedia_fa_simulated"
        }
        
        topics = {
            "هوش مصنوعی": "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است که به ایجاد ماشین‌های هوشمند می‌پردازد.",
            "یادگیری ماشین": "یادگیری ماشین زیرشاخه‌ای از هوش مصنوعی است که به سیستم‌ها توانایی یادگیری از داده می‌دهد.",
            "پایتون": "پایتون یک زبان برنامه‌نویسی سطح بالا، مفسری و همه‌منظوره است.",
            "شبکه عصبی": "شبکه عصبی مصنوعی مدلی محاسباتی است که از شبکه عصبی بیولوژیکی الهام گرفته شده است."
        }
        
        for topic, content in topics.items():
            if topic in query or query in topic:
                simulated_data["results"].append({
                    "title": topic,
                    "summary": content,
                    "url": f"https://fa.wikipedia.org/wiki/{topic.replace(' ', '_')}",
                    "confidence": np.random.uniform(0.8, 0.95)
                })
        
        self.cache[cache_key] = simulated_data
        return simulated_data
    
    def query_conceptnet(self, concept: str) -> Dict:
        """پرس‌وجوی شبیه‌سازی شده از ConceptNet"""
        cache_key = f"conceptnet_{hashlib.md5(concept.encode()).hexdigest()}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # روابط شبیه‌سازی شده
        relations = {
            "هوش_مصنوعی": [
                {"relation": "IsA", "target": "رشته_علمی", "weight": 0.9},
                {"relation": "UsedFor", "target": "حل_مسئله", "weight": 0.8},
                {"relation": "RelatedTo", "target": "کامپیوتر", "weight": 0.95}
            ],
            "یادگیری_ماشین": [
                {"relation": "PartOf", "target": "هوش_مصنوعی", "weight": 0.85},
                {"relation": "UsedFor", "target": "پیش‌بینی", "weight": 0.9},
                {"relation": "RelatedTo", "target": "داده", "weight": 0.95}
            ]
        }
        
        concept_key = concept.replace(" ", "_")
        result = {
            "concept": concept,
            "relations": relations.get(concept_key, []),
            "source": "conceptnet_simulated"
        }
        
        self.cache[cache_key] = result
        return result
    
    def fetch_academic_paper(self, topic: str) -> Dict:
        """دریافت شبیه‌سازی شده مقاله علمی"""
        papers = {
            "یادگیری عمیق": {
                "title": "یادگیری عمیق: مروری بر معماری‌ها و کاربردها",
                "authors": ["LeCun", "Bengio", "Hinton"],
                "abstract": "یادگیری عمیق زیرشاخه‌ای از یادگیری ماشین است که از شبکه‌های عصبی با لایه‌های متعدد استفاده می‌کند.",
                "year": 2015,
                "citations": 100000
            },
            "شبکه عصبی کانولوشن": {
                "title": "شبکه‌های عصبی کانولوشن برای تشخیص تصویر",
                "authors": ["Krizhevsky", "Sutskever", "Hinton"],
                "abstract": "معماری CNN برای پردازش داده‌های با ساختار شبکه‌ای مانند تصاویر بهینه شده است.",
                "year": 2012,
                "citations": 80000
            }
        }
        
        for paper_topic, paper_data in papers.items():
            if paper_topic in topic or topic in paper_topic:
                return {
                    "topic": topic,
                    "found": True,
                    "paper": paper_data,
                    "source": "arxiv_simulated"
                }
        
        return {
            "topic": topic,
            "found": False,
            "source": "arxiv_simulated"
        }
    
    def learn_from_library(self, query: str) -> Dict:
        """یادگیری ترکیبی از همه کتابخانه‌ها"""
        results = {
            "query": query,
            "wikipedia": self.search_wikipedia(query),
            "conceptnet": self.query_conceptnet(query),
            "academic": self.fetch_academic_paper(query),
            "timestamp": datetime.now().isoformat()
        }
        
        # استخراج دانش ترکیبی
        combined_knowledge = self.extract_combined_knowledge(results)
        results["combined_knowledge"] = combined_knowledge
        
        return results
    
    def extract_combined_knowledge(self, library_results: Dict) -> Dict:
        """استخراج دانش یکپارچه از نتایج کتابخانه‌ای"""
        concepts = set()
        relations = []
        definitions = []
        
        # از ویکی‌پدیا
        if "results" in library_results["wikipedia"]:
            for result in library_results["wikipedia"]["results"]:
                concepts.add(result["title"])
                definitions.append({
                    "concept": result["title"],
                    "definition": result["summary"],
                    "source": "wikipedia"
                })
        
        # از ConceptNet
        if "relations" in library_results["conceptnet"]:
            for relation in library_results["conceptnet"]["relations"]:
                relations.append(relation)
                concepts.add(library_results["conceptnet"]["concept"])
                concepts.add(relation["target"])
        
        # از مقالات علمی
        if library_results["academic"]["found"]:
            paper = library_results["academic"]["paper"]
            concepts.add(library_results["academic"]["topic"])
            definitions.append({
                "concept": paper["title"],
                "definition": paper["abstract"],
                "source": "academic"
            })
        
        return {
            "concepts": list(concepts),
            "relations": relations,
            "definitions": definitions,
            "source_count": len([k for k, v in library_results.items() if isinstance(v, dict) and v])
        }

# ==================== سیستم یکپارچه عصبی-نمادین ====================

class NeuralSymbolicGraph:
    """گراف دانش یکپارچه عصبی-نمادین"""
    
    def __init__(self):
        self.deep_nlp = DeepLearningNLP()
        self.library = LibraryLearning()
        
        # گراف نمادین
        self.symbolic_graph = defaultdict(dict)
        
        # حافظه عصبی (embeddings)
        self.neural_embeddings = {}
        
        # پایگاه دانش یکپارچه
        self.unified_knowledge = self.initialize_unified_knowledge()
        
        # تاریخچه یادگیری
        self.learning_history = []
    
    def initialize_unified_knowledge(self):
        """ایجاد پایگاه دانش یکپارچه اولیه"""
        return {
            "هوش_مصنوعی": {
                "type": "مفهوم_علمی",
                "neural_embedding": self.deep_nlp.get_sentence_embedding("هوش مصنوعی"),
                "symbolic_properties": ["یادگیری", "استدلال", "حل مسئله"],
                "library_sources": ["wikipedia", "conceptnet", "arxiv"],
                "consensus_score": 0.95,
                "last_updated": datetime.now().isoformat()
            },
            "یادگیری_ماشین": {
                "type": "زیرشاخه",
                "neural_embedding": self.deep_nlp.get_sentence_embedding("یادگیری ماشین"),
                "symbolic_properties": ["پیش‌بینی", "طبقه‌بندی", "خوشه‌بندی"],
                "library_sources": ["wikipedia", "conceptnet"],
                "consensus_score": 0.98,
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def process_question(self, question: str) -> Dict:
        """پردازش یکپارچه سوال"""
        # تحلیل عصبی
        neural_analysis = self.deep_nlp.classify_intent(question)
        entities_deep = self.deep_nlp.extract_entities_deep(question)
        question_embedding = self.deep_nlp.get_sentence_embedding(question)
        
        # یادگیری کتابخانه‌ای
        library_knowledge = self.library.learn_from_library(question)
        
        # تحلیل نمادین
        symbolic_analysis = self.analyze_symbolically(question)
        
        # یکپارچه‌سازی نتایج
        unified_analysis = self.integrate_analyses(
            neural_analysis,
            library_knowledge,
            symbolic_analysis,
            question_embedding
        )
        
        # یادگیری و به‌روزرسانی
        self.learn_from_interaction(question, unified_analysis)
        
        return unified_analysis
    
    def analyze_symbolically(self, text: str) -> Dict:
        """تحلیل نمادین متن"""
        words = text.split()
        
        # استخراج روابط ساده
        relations = []
        for i in range(len(words) - 1):
            if words[i] in ["علت", "دلیل"] and words[i+1] not in ["است", "می‌باشد"]:
                relations.append({
                    "type": "causal",
                    "source": words[i+1],
                    "relation": "علت"
                })
            elif words[i] in ["تفاوت", "فرق"] and "و" in text:
                relations.append({
                    "type": "comparison",
                    "relation": "مقایسه"
                })
        
        return {
            "word_count": len(words),
            "relations_found": relations,
            "has_question_mark": "؟" in text,
            "symbolic_pattern": self.detect_symbolic_pattern(text)
        }
    
    def detect_symbolic_pattern(self, text: str) -> str:
        """تشخیص الگوی نمادین"""
        patterns = {
            "definition": r"(چیست|چیه|تعریف)",
            "causal": r"(چرا|علت|دلیل)",
            "comparison": r"(تفاوت|فرق|مقایسه)",
            "proof": r"(اثبات|ثابت|نشان)",
            "howto": r"(چگونه|چطور|روش)"
        }
        
        for pattern_name, pattern in patterns.items():
            if re.search(pattern, text):
                return pattern_name
        
        return "general"
    
    def integrate_analyses(self, neural: Dict, library: Dict, symbolic: Dict, embedding: np.ndarray) -> Dict:
        """یکپارچه‌سازی تحلیل‌های مختلف"""
        # محاسبه اطمینان کلی
        neural_confidence = neural.get("confidence", 0.5)
        library_confidence = library.get("combined_knowledge", {}).get("source_count", 0) / 4
        symbolic_confidence = len(symbolic.get("relations_found", [])) * 0.2
        
        overall_confidence = (neural_confidence + library_confidence + symbolic_confidence) / 3
        
        # استخراج مفاهیم یکپارچه
        all_concepts = set()
        
        # از تحلیل عصبی
        for entity in neural.get("entities", []):
            all_concepts.add(entity.get("entity", ""))
        
        # از کتابخانه
        if "combined_knowledge" in library:
            for concept in library["combined_knowledge"].get("concepts", []):
                all_concepts.add(concept)
        
        # از تحلیل نمادین
        for relation in symbolic.get("relations_found", []):
            if "source" in relation:
                all_concepts.add(relation["source"])
        
        return {
            "question_embedding": embedding.tolist(),
            "neural_intent": neural,
            "library_knowledge": library["combined_knowledge"],
            "symbolic_analysis": symbolic,
            "unified_concepts": list(all_concepts),
            "confidence": overall_confidence,
            "integration_method": "neural_symbolic_fusion",
            "timestamp": datetime.now().isoformat()
        }
    
    def learn_from_interaction(self, question: str, analysis: Dict):
        """یادگیری از تعامل و به‌روزرسانی دانش"""
        learning_entry = {
            "question": question,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        self.learning_history.append(learning_entry)
        
        # به‌روزرسانی گراف با مفاهیم جدید
        for concept in analysis.get("unified_concepts", []):
            concept_key = concept.replace(" ", "_")
            
            if concept_key not in self.unified_knowledge:
                # ایجاد ورودی جدید
                self.unified_knowledge[concept_key] = {
                    "type": "new_concept",
                    "neural_embedding": self.deep_nlp.get_sentence_embedding(concept),
                    "symbolic_properties": [],
                    "library_sources": [],
                    "consensus_score": 0.5,
                    "learned_from": "interaction",
                    "first_seen": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            else:
                # به‌روزرسانی ورودی موجود
                self.unified_knowledge[concept_key]["last_updated"] = datetime.now().isoformat()
                if "learned_from" not in self.unified_knowledge[concept_key]:
                    self.unified_knowledge[concept_key]["learned_from"] = "interaction"
        
        # محدود کردن تاریخچه یادگیری
        if len(self.learning_history) > 100:
            self.learning_history = self.learning_history[-100:]
    
    def generate_response(self, analysis: Dict) -> str:
        """تولید پاسخ بر اساس تحلیل یکپارچه"""
        primary_intent = analysis["neural_intent"]["primary"]
        confidence = analysis["confidence"]
        
        # تولید پاسخ بر اساس هدف
        if primary_intent == "definition":
            return self._generate_definition_response(analysis)
        elif primary_intent == "causal":
            return self._generate_causal_response(analysis)
        elif primary_intent == "comparison":
            return self._generate_comparison_response(analysis)
        elif primary_intent == "proof":
            return self._generate_proof_response(analysis)
        elif primary_intent == "howto":
            return self._generate_howto_response(analysis)
        else:
            return self._generate_general_response(analysis)
    
    def _generate_definition_response(self, analysis: Dict) -> str:
        """پاسخ به سوالات تعریفی"""
        concepts = analysis.get("unified_concepts", [])
        
        if not concepts:
            return "🤔 **تعریف**:\n\nمفهوم مورد نظر را مشخص‌تر بیان کنید."
        
        main_concept = concepts[0]
        
        # جستجو در دانش یکپارچه
        if main_concept.replace(" ", "_") in self.unified_knowledge:
            concept_data = self.unified_knowledge[main_concept.replace(" ", "_")]
            
            response = f"🧠 **تعریف یکپارچه عصبی-نمادین**:\n\n"
            response += f"**{main_concept}**\n\n"
            
            # اطلاعات از کتابخانه
            if "library_knowledge" in analysis:
                for definition in analysis["library_knowledge"].get("definitions", []):
                    if definition["concept"] == main_concept:
                        response += f"📚 **از {definition['source']}**:\n{definition['definition']}\n\n"
            
            # اطلاعات عصبی
            response += f"🔬 **تحلیل عصبی**:\n"
            response += f"• شباهت مفهومی: {analysis['neural_intent']['confidence']:.2f}\n"
            response += f"• اطمینان کلی: {analysis['confidence']:.2f}\n\n"
            
            # یادگیری سیستم
            response += f"💡 **سیستم من**:\n"
            response += "این پاسخ با ترکیب تحلیل عمیق عصبی و دانش کتابخانه‌ای تولید شده است."
            
            return response
        
        return "🔍 **تحلیل**:\n\nاین مفهوم را در سیستم یکپارچه خود می‌آموزم. لطفاً کمی بیشتر توضیح دهید."
    
    def _generate_causal_response(self, analysis: Dict) -> str:
        """پاسخ به سوالات علّی"""
        symbolic_relations = analysis["symbolic_analysis"].get("relations_found", [])
        
        response = "🔗 **تحلیل علّی یکپارچه**:\n\n"
        
        if symbolic_relations:
            for rel in symbolic_relations:
                if rel["type"] == "causal":
                    response += f"**{rel['source']}** → علت احتمالی\n\n"
        
        # افزودن تحلیل عصبی
        response += f"🧠 **تحلیل عصبی**:\n"
        response += f"• هدف شناسایی شده: {analysis['neural_intent']['primary']}\n"
        response += f"• اطمینان: {analysis['neural_intent']['confidence']:.2f}\n\n"
        
        # افزودن یادگیری کتابخانه‌ای
        if analysis["library_knowledge"].get("relations"):
            response += "📚 **روابط از منابع خارجی**:\n"
            for rel in analysis["library_knowledge"]["relations"][:3]:
                response += f"• {rel['relation']}: {rel['target']} (اطمینان: {rel['weight']:.2f})\n"
        
        response += "\n💡 **نکته**: این تحلیل از ترکیب سیستم عصبی و دانش نمادین تولید شده است."
        
        return response
    
    def _generate_comparison_response(self, analysis: Dict) -> str:
        """پاسخ به سوالات مقایسه‌ای"""
        concepts = analysis.get("unified_concepts", [])
        
        response = "⚖️ **مقایسه یکپارچه**:\n\n"
        
        if len(concepts) >= 2:
            response += f"مقایسه **{concepts[0]}** و **{concepts[1]}**:\n\n"
            
            # محاسبه شباهت عصبی
            if len(concepts) >= 2:
                sim = self.deep_nlp.semantic_similarity(concepts[0], concepts[1])
                response += f"🧠 **شباهت عصبی**: {sim:.2f}\n\n"
        
        # افزودن تحلیل ترکیبی
        response += "🔬 **روش تحلیل**:\n"
        response += "1. استخراج embeddingهای عصبی\n"
        response += "2. جستجو در منابع کتابخانه‌ای\n"
        response += "3. تحلیل روابط نمادین\n"
        response += "4. ترکیب نتایج\n\n"
        
        response += "📊 **اطمینان سیستم**: "
        response += f"{analysis['confidence']:.2f}"
        
        return response
    
    def _generate_proof_response(self, analysis: Dict) -> str:
        """پاسخ به سوالات اثباتی"""
        response = "🔍 **روش اثبات یکپارچه**:\n\n"
        
        response += "🧠 **رویکرد عصبی-نمادین**:\n"
        response += "1. تحلیل معنایی با شبکه عصبی\n"
        response += "2. بررسی روابط در گراف دانش\n"
        response += "3. استخراج از منابع معتبر\n"
        response += "4. ترکیب و استنتاج\n\n"
        
        # اطلاعات کتابخانه‌ای
        if analysis["library_knowledge"].get("definitions"):
            response += "📚 **منابع استفاده شده**:\n"
            sources = set(d["source"] for d in analysis["library_knowledge"]["definitions"])
            for source in list(sources)[:3]:
                response += f"• {source}\n"
        
        response += f"\n🎯 **اعتماد به سیستم**: {analysis['confidence']:.2f}"
        
        return response
    
    def _generate_howto_response(self, analysis: Dict) -> str:
        """پاسخ به سوالات روشی"""
        response = "🛠️ **راهنمای یکپارچه**:\n\n"
        
        response += "**مراحل پیشنهادی**:\n"
        response += "1. تحلیل مسئله با سیستم عصبی\n"
        response += "2. جستجو در دانش کتابخانه‌ای\n"
        response += "3. استخراج الگوهای نمادین\n"
        response += "4. تولید راه‌حل ترکیبی\n\n"
        
        response += "🔬 **مزایای رویکرد ترکیبی**:\n"
        response += "• درک عمیق‌تر با شبکه عصبی\n"
        response += "• دقت بیشتر با دانش نمادین\n"
        response += "• جامعیت با منابع خارجی\n"
        response += "• سازگاری با مفاهیم جدید\n"
        
        return response
    
    def _generate_general_response(self, analysis: Dict) -> str:
        """پاسخ عمومی"""
        concepts = analysis.get("unified_concepts", [])
        
        response = "🧠 **تحلیل یکپارچه عصبی-نمادین**:\n\n"
        
        if concepts:
            response += f"**مفاهیم شناسایی شده**: {', '.join(concepts[:5])}\n\n"
        
        response += "**سیستم من**:\n"
        response += "• 🤖 پردازش عصبی (یادگیری عمیق)\n"
        response += "• 📚 یادگیری کتابخانه‌ای\n"
        response += "• 🔗 گراف دانش نمادین\n"
        response += "• ⚡ یکپارچه‌سازی هوشمند\n\n"
        
        response += f"**اطمینان تحلیل**: {analysis['confidence']:.2f}\n"
        response += f"**هدف شناسایی شده**: {analysis['neural_intent']['primary']}"
        
        return response

# ==================== سیستم اصلی ====================

class IntegratedNatiqSystem:
    """سیستم اصلی یکپارچه عصبی-نمادین"""
    
    def __init__(self):
        self.neural_symbolic_graph = NeuralSymbolicGraph()
        self.session_stats = {
            "total_questions": 0,
            "neural_analyses": 0,
            "library_searches": 0,
            "concepts_learned": 0
        }
    
    def process(self, question: str) -> Dict:
        """پردازش کامل سوال"""
        self.session_stats["total_questions"] += 1
        
        # پردازش یکپارچه
        start_time = datetime.now()
        
        analysis = self.neural_symbolic_graph.process_question(question)
        response = self.neural_symbolic_graph.generate_response(analysis)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # به‌روزرسانی آمار
        self.session_stats["neural_analyses"] += 1
        self.session_stats["library_searches"] += 1
        self.session_stats["concepts_learned"] = len(self.neural_symbolic_graph.unified_knowledge)
        
        return {
            "question": question,
            "response": response,
            "analysis": {
                "neural": analysis["neural_intent"],
                "library_summary": {
                    "concepts_found": len(analysis["library_knowledge"].get("concepts", [])),
                    "relations_found": len(analysis["library_knowledge"].get("relations", []))
                },
                "symbolic": analysis["symbolic_analysis"],
                "unified_concepts": analysis["unified_concepts"],
                "confidence": analysis["confidence"]
            },
            "system_info": {
                "version": "6.0.0",
                "architecture": "neural_symbolic_integration",
                "processing_time": processing_time,
                "knowledge_base_size": len(self.neural_symbolic_graph.unified_knowledge)
            },
            "stats": self.session_stats
        }

# ایجاد سیستم اصلی
integrated_system = IntegratedNatiqSystem()

# ==================== API Endpoints ====================

@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 natiq-ultimate v6.0 | سیستم یکپارچه عصبی-نمادین</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Vazirmatn', system-ui, sans-serif;
                background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
                color: #e0e0e0;
                min-height: 100vh;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1600px;
                margin: 0 auto;
                background: rgba(20, 20, 30, 0.95);
                min-height: 100vh;
                box-shadow: 0 0 60px rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(100, 100, 255, 0.1);
                backdrop-filter: blur(20px);
            }
            
            /* هدر */
            .header {
                background: linear-gradient(90deg, #1a237e, #0d47a1);
                padding: 30px 50px;
                border-bottom: 4px solid #2962ff;
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
                background: 
                    radial-gradient(circle at 20% 50%, rgba(41, 98, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(156, 39, 176, 0.1) 0%, transparent 50%);
            }
            
            .header-content {
                position: relative;
                z-index: 1;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 30px;
            }
            
            .logo {
                display: flex;
                align-items: center;
                gap: 25px;
            }
            
            .logo-icon {
                font-size: 4em;
                color: #82b1ff;
                filter: drop-shadow(0 0 20px rgba(130, 177, 255, 0.5));
                animation: neural-pulse 3s ease-in-out infinite;
            }
            
            @keyframes neural-pulse {
                0%, 100% { 
                    filter: drop-shadow(0 0 20px rgba(130, 177, 255, 0.5));
                    transform: scale(1);
                }
                50% { 
                    filter: drop-shadow(0 0 40px rgba(130, 177, 255, 0.8));
                    transform: scale(1.05);
                }
            }
            
            .logo-text h1 {
                font-size: 2.8em;
                font-weight: 900;
                background: linear-gradient(45deg, #82b1ff, #bb86fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 5px 30px rgba(130, 177, 255, 0.3);
            }
            
            .logo-text .subtitle {
                font-size: 1.1em;
                opacity: 0.9;
                margin-top: 8px;
                color: #bb86fc;
                font-weight: 300;
            }
            
            .architecture-badge {
                background: rgba(41, 98, 255, 0.2);
                border: 2px solid #2962ff;
                padding: 12px 30px;
                border-radius: 35px;
                font-weight: bold;
                font-size: 1.2em;
                backdrop-filter: blur(10px);
                box-shadow: 
                    0 10px 30px rgba(41, 98, 255, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }
            
            /* محتوای اصلی */
            .main-content {
                display: grid;
                grid-template-columns: 1.5fr 1fr;
                gap: 0;
                min-height: 85vh;
            }
            
            /* پنل چت */
            .chat-panel {
                background: rgba(10, 15, 30, 0.8);
                border-right: 1px solid rgba(100, 100, 255, 0.2);
                display: flex;
                flex-direction: column;
            }
            
            .messages-container {
                flex: 1;
                overflow-y: auto;
                padding: 40px;
                background: 
                    linear-gradient(180deg, 
                        rgba(15, 20, 40, 0.9) 0%,
                        rgba(10, 15, 30, 0.7) 100%),
                    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="1" fill="rgba(130,177,255,0.05)"/></svg>');
            }
            
            .message {
                margin: 25px 0;
                padding: 30px;
                border-radius: 25px;
                max-width: 92%;
                position: relative;
                animation: neural-slide 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(130, 177, 255, 0.2);
                box-shadow: 
                    0 15px 40px rgba(0, 0, 0, 0.3),
                    0 0 0 1px rgba(130, 177, 255, 0.1);
            }
            
            @keyframes neural-slide {
                from { 
                    opacity: 0;
                    transform: translateY(40px) scale(0.92);
                }
                to { 
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .user-message {
                background: linear-gradient(135deg, 
                    rgba(41, 98, 255, 0.25), 
                    rgba(30, 70, 180, 0.25));
                margin-left: auto;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                border-right: 5px solid #2962ff;
            }
            
            .bot-message {
                background: linear-gradient(135deg,
                    rgba(25, 30, 50, 0.9),
                    rgba(15, 20, 40, 0.95));
                margin-right: auto;
                border-top-left-radius: 8px;
                border-bottom-left-radius: 8px;
                border-left: 5px solid #bb86fc;
            }
            
            .message-header {
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid rgba(130, 177, 255, 0.2);
            }
            
            .message-icon {
                font-size: 2em;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: rgba(130, 177, 255, 0.15);
                box-shadow: 0 5px 15px rgba(130, 177, 255, 0.2);
            }
            
            .message-type {
                font-weight: bold;
                font-size: 1.1em;
                color: #82b1ff;
                text-shadow: 0 0 10px rgba(130, 177, 255, 0.3);
            }
            
            .message-content {
                white-space: pre-wrap;
                line-height: 1.8;
                font-size: 1.1em;
                color: #e0e0e0;
            }
            
            .message-time {
                font-size: 0.85em;
                opacity: 0.7;
                margin-top: 20px;
                text-align: left;
                color: #bb86fc;
                font-family: monospace;
            }
            
            /* ورودی */
            .input-panel {
                background: rgba(15, 20, 40, 0.95);
                padding: 30px;
                border-top: 1px solid rgba(130, 177, 255, 0.2);
            }
            
            .input-group {
                display: flex;
                gap: 20px;
                margin-bottom: 25px;
            }
            
            #messageInput {
                flex: 1;
                padding: 22px 30px;
                background: rgba(25, 30, 50, 0.8);
                border: 2px solid rgba(130, 177, 255, 0.4);
                border-radius: 20px;
                font-size: 1.2em;
                font-family: inherit;
                color: #ffffff;
                transition: all 0.3s;
            }
            
            #messageInput:focus {
                outline: none;
                border-color: #82b1ff;
                background: rgba(25, 30, 50, 0.9);
                box-shadow: 
                    0 0 0 4px rgba(130, 177, 255, 0.1),
                    0 0 30px rgba(130, 177, 255, 0.2);
            }
            
            #sendButton {
                width: 70px;
                background: linear-gradient(45deg, #2962ff, #6200ea);
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-size: 1.4em;
                transition: all 0.3s;
                box-shadow: 0 10px 25px rgba(41, 98, 255, 0.3);
            }
            
            #sendButton:hover {
                transform: translateY(-3px);
                box-shadow: 
                    0 15px 35px rgba(41, 98, 255, 0.4),
                    0 0 20px rgba(130, 177, 255, 0.3);
            }
            
            /* پنل سیستم */
            .system-panel {
                background: rgba(15, 20, 40, 0.95);
                padding: 35px;
                overflow-y: auto;
                border-left: 1px solid rgba(187, 134, 252, 0.2);
            }
            
            .panel-section {
                margin-bottom: 35px;
                padding-bottom: 25px;
                border-bottom: 1px solid rgba(130, 177, 255, 0.2);
            }
            
            .panel-section h3 {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 25px;
                color: #bb86fc;
                font-size: 1.3em;
            }
            
            .section-icon {
                font-size: 1.4em;
                color: #82b1ff;
            }
            
            /* آمار سیستم */
            .system-stats {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: rgba(25, 30, 50, 0.7);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 1px solid rgba(130, 177, 255, 0.2);
                transition: all 0.3s;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                border-color: #82b1ff;
                box-shadow: 0 10px 25px rgba(130, 177, 255, 0.2);
            }
            
            .stat-value {
                font-size: 2.2em;
                font-weight: bold;
                color: #82b1ff;
                margin-bottom: 8px;
                text-shadow: 0 0 15px rgba(130, 177, 255, 0.5);
            }
            
            .stat-label {
                font-size: 0.95em;
                opacity: 0.9;
                color: #bb86fc;
            }
            
            /* کامپوننت‌های سیستم */
            .components-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-top: 15px;
            }
            
            .component {
                background: rgba(30, 35, 60, 0.7);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid rgba(187, 134, 252, 0.2);
                transition: all 0.3s;
            }
            
            .component:hover {
                transform: translateY(-3px);
                border-color: #bb86fc;
                box-shadow: 0 8px 20px rgba(187, 134, 252, 0.2);
            }
            
            .component-icon {
                font-size: 2em;
                color: #bb86fc;
                margin-bottom: 10px;
            }
            
            /* نمونه‌ها */
            .examples-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .example-btn {
                padding: 18px;
                background: rgba(25, 30, 50, 0.7);
                border: 1px solid rgba(130, 177, 255, 0.3);
                border-radius: 15px;
                color: #e0e0e0;
                cursor: pointer;
                transition: all 0.3s;
                text-align: center;
                font-size: 1em;
            }
            
            .example-btn:hover {
                background: rgba(41, 98, 255, 0.2);
                border-color: #2962ff;
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(41, 98, 255, 0.2);
            }
            
            /* پیام خوش‌آمدگویی */
            .welcome-message {
                background: linear-gradient(135deg, 
                    rgba(41, 98, 255, 0.25), 
                    rgba(187, 134, 252, 0.25));
                padding: 35px;
                border-radius: 25px;
                margin-bottom: 35px;
                border: 1px solid rgba(130, 177, 255, 0.3);
                backdrop-filter: blur(20px);
                box-shadow: 
                    0 20px 50px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }
            
            .welcome-message h2 {
                color: #82b1ff;
                margin-bottom: 20px;
                font-size: 1.8em;
            }
            
            .architecture-diagram {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin: 25px 0;
            }
            
            .layer {
                background: rgba(25, 30, 50, 0.7);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                border: 1px solid rgba(130, 177, 255, 0.2);
            }
            
            .layer-icon {
                font-size: 2.5em;
                color: #82b1ff;
                margin-bottom: 15px;
            }
            
            .layer.neural {
                border-color: #2962ff;
                background: rgba(41, 98, 255, 0.1);
            }
            
            .layer.symbolic {
                border-color: #bb86fc;
                background: rgba(187, 134, 252, 0.1);
            }
            
            /* اسکرول بار */
            ::-webkit-scrollbar {
                width: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(25, 30, 50, 0.5);
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #2962ff, #bb86fc);
                border-radius: 6px;
                border: 3px solid rgba(25, 30, 50, 0.5);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(180deg, #2979ff, #d500f9);
            }
            
            /* responsive */
            @media (max-width: 1200px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
                
                .system-panel {
                    border-left: none;
                    border-top: 1px solid rgba(187, 134, 252, 0.2);
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
                    max-width: 96%;
                    padding: 25px;
                }
                
                .architecture-diagram {
                    grid-template-columns: 1fr;
                }
                
                .components-grid,
                .system-stats {
                    grid-template-columns: 1fr;
                }
                
                .examples-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            /* انیمیشن‌های ویژه */
            .neural-connection {
                position: relative;
            }
            
            .neural-connection::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, 
                    transparent, 
                    #82b1ff, 
                    #bb86fc, 
                    transparent);
                animation: neural-flow 3s linear infinite;
            }
            
            @keyframes neural-flow {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
        </style>
        
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <!-- Google Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        
        <script>
            class NeuralSymbolicApp {
                constructor() {
                    this.sessionId = 'neural_' + Date.now();
                    this.baseUrl = window.location.origin;
                    this.messageCount = 0;
                    this.neuralAnalyses = 0;
                    this.knowledgeSize = 0;
                    this.init();
                }
                
                init() {
                    console.log('🧠 natiq-ultimate v6.0 - سیستم عصبی-نمادین یکپارچه');
                    this.setupEventListeners();
                    this.updateSystemStatus('⚡ سیستم عصبی فعال');
                    this.updateNeuralStats();
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
                    document.querySelectorAll('.example-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            const question = e.target.getAttribute('data-question');
                            if (question) {
                                document.getElementById('messageInput').value = question;
                                this.sendMessage();
                            }
                        });
                    });
                }
                
                updateSystemStatus(message) {
                    const statusElement = document.getElementById('systemStatus');
                    if (statusElement) {
                        statusElement.textContent = message;
                    }
                }
                
                updateNeuralStats() {
                    // به‌روزرسانی آمار سیستم عصبی
                    const now = new Date();
                    document.getElementById('currentTime').textContent = 
                        now.toLocaleTimeString('fa-IR', { 
                            hour: '2-digit', 
                            minute: '2-digit',
                            second: '2-digit'
                        });
                    
                    document.getElementById('sessionId').textContent = 
                        this.sessionId.substring(0, 10) + '...';
                }
                
                async sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (!message) return;
                    
                    // نمایش پیام کاربر
                    this.addMessage(message, 'user', 'پرسش کاربر');
                    messageInput.value = '';
                    this.messageCount++;
                    
                    // نمایش پردازش عصبی
                    this.showNeuralProcessing();
                    
                    try {
                        const response = await fetch(this.baseUrl + '/api/neural/' + this.sessionId, {
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
                        
                        this.hideNeuralProcessing();
                        
                        // نمایش پاسخ
                        this.addMessage(data.response, 'bot', 'تحلیل عصبی-نمادین');
                        
                        // به‌روزرسانی پنل سیستم
                        this.updateSystemPanel(data.analysis, data.system_info);
                        
                        this.updateSystemStatus('✅ تحلیل کامل شد');
                        this.neuralAnalyses++;
                        
                    } catch (error) {
                        this.hideNeuralProcessing();
                        console.error('❌ خطا:', error);
                        
                        this.addMessage('⚠️ خطا در پردازش عصبی-نمادین. لطفاً دوباره تلاش کنید.', 'error', 'خطای سیستم');
                        this.updateSystemStatus('❌ خطا در پردازش');
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
                                 type === 'error' ? '⚠️' : '🧬';
                    
                    const headerText = header || (type === 'user' ? 'پرسش کاربر' : 'تحلیل عصبی-نمادین');
                    
                    messageDiv.innerHTML = `
                        <div class="message-header">
                            <div class="message-icon">${icon}</div>
                            <div class="message-type">${headerText}</div>
                        </div>
                        <div class="message-content">${this.escapeHtml(text)}</div>
                        <div class="message-time">${time} | پردازش عصبی</div>
                    `;
                    
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                showNeuralProcessing() {
                    const messagesDiv = document.getElementById('messages');
                    
                    const processingDiv = document.createElement('div');
                    processingDiv.className = 'message bot-message';
                    processingDiv.id = 'neuralProcessingIndicator';
                    processingDiv.innerHTML = `
                        <div class="message-header">
                            <div class="message-icon">⚡</div>
                            <div class="message-type">پردازش عصبی-نمادین</div>
                        </div>
                        <div class="message-content">
                            <div style="display: flex; align-items: center; gap: 20px; padding: 15px 0;">
                                <div style="display: flex; gap: 10px;">
                                    <span style="animation: pulse 1s infinite; color: #82b1ff; font-size: 1.5em;">●</span>
                                    <span style="animation: pulse 1s infinite 0.2s; color: #2962ff; font-size: 1.5em;">●</span>
                                    <span style="animation: pulse 1s infinite 0.4s; color: #bb86fc; font-size: 1.5em;">●</span>
                                </div>
                                <div style="flex: 1;">
                                    <div>🧠 در حال پردازش با شبکه عصبی...</div>
                                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">
                                        ترکیب یادگیری عمیق و دانش نمادین
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(processingDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                hideNeuralProcessing() {
                    const processing = document.getElementById('neuralProcessingIndicator');
                    if (processing) {
                        processing.remove();
                    }
                }
                
                updateSystemPanel(analysis, systemInfo) {
                    // به‌روزرسانی آمار
                    document.getElementById('questionsCount').textContent = this.messageCount;
                    document.getElementById('neuralCount').textContent = this.neuralAnalyses;
                    document.getElementById('knowledgeSize').textContent = systemInfo.knowledge_base_size || 0;
                    document.getElementById('processingTime').textContent = systemInfo.processing_time 
                        ? `${systemInfo.processing_time.toFixed(2)}s` 
                        : '--';
                    
                    // به‌روزرسانی هدف عصبی
                    const neuralIntent = document.getElementById('neuralIntent');
                    if (neuralIntent && analysis.neural) {
                        neuralIntent.textContent = analysis.neural.primary || '--';
                    }
                    
                    // به‌روزرسانی اطمینان
                    const confidence = document.getElementById('confidenceScore');
                    if (confidence && analysis.confidence) {
                        confidence.textContent = analysis.confidence.toFixed(2);
                        // تغییر رنگ بر اساس اطمینان
                        if (analysis.confidence > 0.8) {
                            confidence.style.color = '#4caf50';
                        } else if (analysis.confidence > 0.6) {
                            confidence.style.color = '#ff9800';
                        } else {
                            confidence.style.color = '#f44336';
                        }
                    }
                    
                    // به‌روزرسانی مفاهیم
                    const conceptsDiv = document.getElementById('conceptsList');
                    if (conceptsDiv && analysis.unified_concepts) {
                        conceptsDiv.innerHTML = '';
                        analysis.unified_concepts.slice(0, 6).forEach(concept => {
                            const span = document.createElement('span');
                            span.className = 'concept-tag';
                            span.textContent = concept;
                            conceptsDiv.appendChild(span);
                        });
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
                window.natiqApp = new NeuralSymbolicApp();
                document.getElementById('messageInput').focus();
                
                // نمایش پیام خوش‌آمدگویی
                setTimeout(() => {
                    const welcomeMsg = `🧬 **به natiq-ultimate نسخه ۶.۰ خوش آمدید!**\n\nاین سیستم از **معماری عصبی-نمادین یکپارچه** استفاده می‌کند:\n\n🤖 **لایه عصبی**: یادگیری عمیق برای درک زبان\n📚 **لایه کتابخانه‌ای**: یادگیری از منابع خارجی\n🔗 **لایه نمادین**: گراف دانش و استنتاج منطقی\n⚡ **یکپارچه‌ساز**: ترکیب هوشمند همه لایه‌ها\n\n💡 **ویژگی منحصربه‌فرد**: سیستم می‌تواند هم‌زمان از شبکه عصبی و دانش نمادین استفاده کند!`;
                    window.natiqApp.addMessage(welcomeMsg, 'bot', 'سیستم عصبی-نمادین');
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
                    window.natiqApp.neuralAnalyses = 0;
                    window.natiqApp.updateSystemStatus('🗑️ گفتگو پاک شد');
                    
                    // بازنشانی پنل سیستم
                    document.getElementById('questionsCount').textContent = '0';
                    document.getElementById('neuralCount').textContent = '0';
                    document.getElementById('neuralIntent').textContent = '--';
                    document.getElementById('confidenceScore').textContent = '--';
                    document.getElementById('conceptsList').innerHTML = 
                        '<span style="opacity:0.7">هنوز مفهومی یافت نشد</span>';
                }
            }
            
            function testNeuralCapabilities() {
                const tests = [
                    "یادگیری عمیق چیست؟",
                    "تفاوت شبکه عصبی و یادگیری ماشین",
                    "چگونه هوش مصنوعی کار می‌کند؟",
                    "علت اهمیت داده در هوش مصنوعی",
                    "اثبات اهمیت یادگیری عمیق"
                ];
                
                tests.forEach((question, index) => {
                    setTimeout(() => {
                        document.getElementById('messageInput').value = question;
                        window.natiqApp.sendMessage();
                    }, index * 3500);
                });
            }
            
            function showArchitecture() {
                const msg = `🏗️ **معماری سیستم عصبی-نمادین**:\n\n` +
                          `**۱. لایه عصبی (Deep Learning)**:\n` +
                          `   • پردازش زبان طبیعی\n` +
                          `   • استخراج embedding\n` +
                          `   • طبقه‌بندی هدف\n\n` +
                          `**۲. لایه کتابخانه‌ای (Library Learning)**:\n` +
                          `   • جستجوی ویکی‌پدیا\n` +
                          `   • پرس‌وجوی ConceptNet\n` +
                          `   • دریافت مقالات علمی\n\n` +
                          `**۳. لایه نمادین (Symbolic)**:\n` +
                          `   • گراف دانش\n` +
                          `   • استنتاج منطقی\n` +
                          `   • روابط علّی\n\n` +
                          `**۴. یکپارچه‌ساز (Integrator)**:\n` +
                          `   • ترکیب نتایج\n` +
                          `   • محاسبه اطمینان\n` +
                          `   • تولید پاسخ نهایی`;
                
                window.natiqApp.addMessage(msg, 'bot', 'معماری سیستم');
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
                            <i class="fas fa-brain"></i>
                        </div>
                        <div class="logo-text">
                            <h1>natiq-ultimate</h1>
                            <div class="subtitle">سیستم عصبی-نمادین یکپارچه</div>
                        </div>
                    </div>
                    
                    <div class="architecture-badge">
                        نسخه ۶.۰ - Neural-Symbolic
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 12px; height: 12px; background: #4caf50; border-radius: 50%; 
                                      box-shadow: 0 0 20px #4caf50; animation: pulse 2s infinite;"></div>
                            <span id="systemStatus" style="font-weight: bold;">در حال راه‌اندازی...</span>
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
                            <h2>🧬 معماری عصبی-نمادین فعال شد</h2>
                            <p>این سیستم ترکیبی از یادگیری عمیق، دانش کتابخانه‌ای و منطق نمادین است که همگی به صورت یکپارچه کار می‌کنند.</p>
                            
                            <div class="architecture-diagram">
                                <div class="layer neural">
                                    <div class="layer-icon">
                                        <i class="fas fa-network-wired"></i>
                                    </div>
                                    <div>لایه عصبی</div>
                                    <small>یادگیری عمیق</small>
                                </div>
                                <div class="layer symbolic">
                                    <div class="layer-icon">
                                        <i class="fas fa-project-diagram"></i>
                                    </div>
                                    <div>لایه نمادین</div>
                                    <small>گراف دانش</small>
                                </div>
                                <div class="layer">
                                    <div class="layer-icon">
                                        <i class="fas fa-book"></i>
                                    </div>
                                    <div>لایه کتابخانه‌ای</div>
                                    <small>منابع خارجی</small>
                                </div>
                                <div class="layer" style="grid-column: span 2;">
                                    <div class="layer-icon">
                                        <i class="fas fa-sync-alt"></i>
                                    </div>
                                    <div>یکپارچه‌ساز</div>
                                    <small>ترکیب هوشمند</small>
                                </div>
                            </div>
                            
                            <p style="margin-top: 20px; font-size: 0.95em; color: #bb86fc;">
                                <strong>✨ نوآوری:</strong> سیستم می‌تواند هم‌زمان از قدرت شبکه عصبی و دقت دانش نمادین استفاده کند.
                            </p>
                        </div>
                    </div>
                    
                    <!-- پنل ورودی -->
                    <div class="input-panel">
                        <div class="input-group">
                            <input 
                                type="text" 
                                id="messageInput" 
                                placeholder="سوال خود را بپرسید (سیستم عصبی-نمادین تحلیل می‌کند)..." 
                                autocomplete="off"
                                autofocus
                            >
                            <button id="sendButton">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        
                        <div class="examples-grid">
                            <button class="example-btn" data-question="یادگیری عمیق چیست؟">
                                <i class="fas fa-graduation-cap"></i> سوال تعریفی
                            </button>
                            <button class="example-btn" data-question="تفاوت شبکه عصبی و یادگیری ماشین">
                                <i class="fas fa-balance-scale"></i> سوال مقایسه‌ای
                            </button>
                            <button class="example-btn" data-question="چگونه هوش مصنوعی کار می‌کند؟">
                                <i class="fas fa-cogs"></i> سوال روشی
                            </button>
                            <button class="example-btn" onclick="testNeuralCapabilities()">
                                <i class="fas fa-vial"></i> تست کامل سیستم
                            </button>
                            <button class="example-btn" onclick="showArchitecture()">
                                <i class="fas fa-sitemap"></i> نمایش معماری
                            </button>
                            <button class="example-btn" onclick="clearChat()">
                                <i class="fas fa-trash"></i> پاک کردن همه
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- پنل سیستم -->
                <div class="system-panel">
                    <div class="panel-section">
                        <h3><i class="fas fa-chart-line section-icon"></i> آمار سیستم</h3>
                        <div class="system-stats">
                            <div class="stat-card">
                                <div class="stat-value" id="questionsCount">0</div>
                                <div class="stat-label">سوالات</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value" id="neuralCount">0</div>
                                <div class="stat-label">تحلیل عصبی</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value" id="knowledgeSize">0</div>
                                <div class="stat-label">مفاهیم دانش</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value" id="processingTime">--</div>
                                <div class="stat-label">زمان پردازش</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-microchip section-icon"></i> کامپوننت‌های سیستم</h3>
                        <div class="components-grid">
                            <div class="component">
                                <div class="component-icon">
                                    <i class="fas fa-brain"></i>
                                </div>
                                <div>شبکه عصبی</div>
                                <small>یادگیری عمیق</small>
                            </div>
                            <div class="component">
                                <div class="component-icon">
                                    <i class="fas fa-book"></i>
                                </div>
                                <div>کتابخانه‌ای</div>
                                <small>منابع خارجی</small>
                            </div>
                            <div class="component">
                                <div class="component-icon">
                                    <i class="fas fa-project-diagram"></i>
                                </div>
                                <div>گراف دانش</div>
                                <small>نمادین</small>
                            </div>
                            <div class="component">
                                <div class="component-icon">
                                    <i class="fas fa-sync-alt"></i>
                                </div>
                                <div>یکپارچه‌ساز</div>
                                <small>ترکیب کننده</small>
                            </div>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-bullseye section-icon"></i> تحلیل جاری</h3>
                        <div style="background: rgba(25,30,50,0.7); padding: 20px; border-radius: 12px;">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                                <div>
                                    <div style="font-size: 0.9em; opacity: 0.8;">هدف عصبی:</div>
                                    <div style="font-size: 1.2em; color: #82b1ff;" id="neuralIntent">--</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.9em; opacity: 0.8;">اطمینان:</div>
                                    <div style="font-size: 1.2em; color: #4caf50;" id="confidenceScore">--</div>
                                </div>
                            </div>
                            <div>
                                <div style="font-size: 0.9em; opacity: 0.8; margin-bottom: 10px;">مفاهیم یافت شده:</div>
                                <div id="conceptsList" style="display: flex; flex-wrap: wrap; gap: 8px; min-height: 40px;">
                                    <span style="opacity: 0.7;">هنوز مفهومی یافت نشد</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="panel-section">
                        <h3><i class="fas fa-info-circle section-icon"></i> اطلاعات جلسه</h3>
                        <div style="background: rgba(25,30,50,0.7); padding: 20px; border-radius: 12px; font-size: 0.95em;">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                <div>
                                    <div style="opacity: 0.8;">شناسه جلسه:</div>
                                    <div style="color: #bb86fc; font-family: monospace;" id="sessionId">...</div>
                                </div>
                                <div>
                                    <div style="opacity: 0.8;">زمان کنونی:</div>
                                    <div style="color: #82b1ff;" id="currentTime">--:--:--</div>
                                </div>
                            </div>
                            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(130,177,255,0.2);">
                                <div style="opacity: 0.8;">معماری:</div>
                                <div style="color: #82b1ff;">عصبی-نمادین یکپارچه</div>
                            </div>
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
        "status": "neural_symbolic_active",
        "system": "natiq-ultimate",
        "version": "6.0.0",
        "architecture": "neural_symbolic_integration",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "deep_learning": {
                "status": "simulated",
                "embeddings": len(integrated_system.neural_symbolic_graph.deep_nlp.word_vectors),
                "capabilities": ["semantic_similarity", "intent_classification", "entity_extraction"]
            },
            "library_learning": {
                "status": "simulated",
                "sources": list(integrated_system.neural_symbolic_graph.library.knowledge_sources.keys()),
                "cache_size": len(integrated_system.neural_symbolic_graph.library.cache)
            },
            "symbolic_graph": {
                "status": "active",
                "concepts": len(integrated_system.neural_symbolic_graph.unified_knowledge),
                "learning_history": len(integrated_system.neural_symbolic_graph.learning_history)
            }
        },
        "integration": {
            "method": "neural_symbolic_fusion",
            "status": "fully_integrated",
            "learning_capability": "continuous"
        }
    }

@app.post("/api/neural/{session_id}")
async def neural_endpoint(session_id: str, request: dict):
    """اندپوینت سیستم عصبی-نمادین"""
    try:
        question = request.get("message", "")
        
        if not question or question.strip() == "":
            raise HTTPException(status_code=400, detail="سوال نمی‌تواند خالی باشد")
        
        # پردازش با سیستم عصبی-نمادین
        result = integrated_system.process(question)
        
        return {
            "session_id": session_id,
            "question": question,
            "response": result["response"],
            "analysis": result["analysis"],
            "system_info": result["system_info"],
            "stats": result["stats"],
            "timestamp": datetime.now().isoformat(),
            "version": "6.0.0"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "خطا در پردازش عصبی-نمادین",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/system/status")
async def system_status():
    """وضعیت سیستم عصبی-نمادین"""
    return {
        "neural_system": {
            "embeddings_loaded": len(integrated_system.neural_symbolic_graph.deep_nlp.word_vectors),
            "model_state": integrated_system.neural_symbolic_graph.deep_nlp.model_state
        },
        "library_system": {
            "sources_available": len(integrated_system.neural_symbolic_graph.library.knowledge_sources),
            "cache_entries": len(integrated_system.neural_symbolic_graph.library.cache)
        },
        "knowledge_base": {
            "total_concepts": len(integrated_system.neural_symbolic_graph.unified_knowledge),
            "learning_entries": len(integrated_system.neural_symbolic_graph.learning_history),
            "recent_learning": integrated_system.neural_symbolic_graph.learning_history[-1] 
                if integrated_system.neural_symbolic_graph.learning_history else None
        },
        "session_stats": integrated_system.session_stats
    }

@app.get("/api/debug/neural")
async def debug_neural():
    """دیباگ سیستم عصبی"""
    return {
        "system": "natiq-ultimate-neural-symbolic",
        "version": "6.0.0",
        "integration_level": "full_neural_symbolic",
        "deep_learning": {
            "simulation": True,
            "embedding_dim": 50,
            "word_vectors_count": len(integrated_system.neural_symbolic_graph.deep_nlp.word_vectors),
            "sample_embedding": integrated_system.neural_symbolic_graph.deep_nlp.get_sentence_embedding("هوش مصنوعی").tolist()[:5]
        },
        "library_learning": {
            "simulation": True,
            "sources": list(integrated_system.neural_symbolic_graph.library.knowledge_sources.keys()),
            "cache_hits": len(integrated_system.neural_symbolic_graph.library.cache)
        },
        "symbolic_integration": {
            "method": "neural_symbolic_fusion",
            "knowledge_fusion": "real_time",
            "learning": "continuous"
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
