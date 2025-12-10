import sympy as sp
import numpy as np
from typing import Dict, Any, List
import re
import json

class NatiqMathEngine:
    """موتور ریاضی ناطق"""
    
    def __init__(self):
        self.supported_operations = {
            'جبر': ['معادله', 'ساده‌سازی', 'عامل‌گیری'],
            'حسابان': ['مشتق', 'انتگرال', 'حد'],
            'منطق': ['گزاره', 'استلزام', 'برهان'],
            'آمار': ['میانگین', 'انحراف معیار', 'رگرسیون']
        }
    
    def parse_persian_math(self, text: str) -> str:
        """تبدیل ریاضی فارسی به نماد استاندارد"""
        replacements = {
            'مشتق': 'diff',
            'انتگرال': 'integrate',
            'حد': 'limit',
            'جذر': 'sqrt',
            'سیگما': 'Sum',
            'بینهایت': 'oo',
            'پی': 'pi',
            'ای': 'E',
            'قدر مطلق': 'abs'
        }
        
        for fa, en in replacements.items():
            text = text.replace(fa, en)
        
        return text
    
    def solve_equation(self, equation: str, variable: str = 'x'):
        """حل معادله"""
        try:
            # تبدیل به فرمت sympy
            eq = sp.sympify(equation)
            sol = sp.solve(eq, sp.Symbol(variable))
            
            return {
                'equation': equation,
                'solutions': [str(s) for s in sol],
                'steps': self._show_steps(eq, variable),
                'type': 'algebraic'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_derivative(self, expression: str, variable: str = 'x'):
        """محاسبه مشتق"""
        try:
            expr = sp.sympify(expression)
            deriv = sp.diff(expr, sp.Symbol(variable))
            
            return {
                'function': expression,
                'derivative': str(deriv),
                'latex': sp.latex(deriv),
                'steps': f'مشتق {expression} نسبت به {variable}'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def evaluate_logic(self, proposition: str):
        """ارزیابی گزاره منطقی"""
        try:
            # تبدیل گزاره فارسی به منطق
            logic_map = {
                'و': '&',
                'یا': '|',
                'نباشد': '~',
                'اگر': '>>',
                'آنگاه': '>>'
            }
            
            return {
                'proposition': proposition,
                'evaluation': 'در حال توسعه',
                'type': 'logical'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _show_steps(self, equation, variable):
        """نمایش مراحل حل"""
        steps = []
        x = sp.Symbol(variable)
        
        try:
            # مرحله 1: ساده‌سازی
            simplified = sp.simplify(equation)
            steps.append(f"ساده‌سازی: {simplified}")
            
            # مرحله 2: حل
            solutions = sp.solve(equation, x)
            steps.append(f"حل برای {variable}: {solutions}")
            
        except Exception as e:
            steps.append(f"خطا در نمایش مراحل: {str(e)}")
        
        return steps

# نمونه شیء جهانی
math_engine = NatiqMathEngine()
