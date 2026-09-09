import math
import re

# Restricted namespace untuk evaluasi ekspresi yang aman
SAFE_MATH_NAMESPACE = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'log': math.log10,    # Log basis 10
    'ln': math.log,       # Natural log
    'sqrt': math.sqrt,
    'pi': math.pi,
    'e': math.e,
    'abs': abs,
    'pow': math.pow
}

def evaluate_expression(expression):
    """
    Mengevaluasi ekspresi matematika dari string dengan aman.
    """
    try:
        # Pre-processing ekspresi:
        # Ganti ^ dengan ** untuk pangkat
        expr = expression.replace('^', '**')
        # Ganti 'x' atau 'X' dengan '*' untuk perkalian jika pengguna mengetiknya secara manual
        expr = expr.replace('x', '*').replace('X', '*')
        
        # Tambahkan otomatis tanda kurung tutup jika kurang
        open_brackets = expr.count('(')
        close_brackets = expr.count(')')
        if open_brackets > close_brackets:
            expr += ')' * (open_brackets - close_brackets)
            
        # Evaluasi dengan namespace terbatas (tidak ada __builtins__)
        result = eval(expr, {"__builtins__": None}, SAFE_MATH_NAMESPACE)
        
        # Format hasil agar rapi jika bilangan bulat
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(round(result, 8)) # Pembulatan untuk mencegah floating point error (e.g. 0.1 + 0.2)
        
    except ZeroDivisionError:
        return "Error: Dibagi nol"
    except Exception as e:
        # Untuk error penulisan rumus matematika
        return "Error: Sintaks"

