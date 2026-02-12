import streamlit as st
import ollama
import sympy
from sympy import symbols, solve, diff, integrate, simplify, Eq
# CRITICAL IMPORT: This allows Python to understand "2x" as "2*x"
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ukufunda-Sci",
    page_icon="🔬",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp { 
        background-color: #0e1117; 
        color: white; 
    }
    
    /* Input Box Styling */
    .stTextInput input { 
        background-color: #262730; 
        color: #fff; 
        border: 1px solid #4e4e4e; 
        border-radius: 8px; 
        padding: 12px;
    }
    
    /* Result Cards */
    .result-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        font-family: 'Times New Roman', Times, serif; /* Math Font */
        font-size: 1.1em;
        line-height: 1.6;
        color: #e0e0e0;
        border-left: 5px solid #00D4FF;
    }
    
    /* Success/Error Boxes */
    .success-box {
        background-color: #153820;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #28a745;
        margin-bottom: 15px;
        color: #fff;
    }
    
    .error-box {
        background-color: #381515;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #a72828;
        margin-bottom: 15px;
        color: #fff;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #00D4FF, #0099CC);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.2em;
        transition: all 0.3s;
        width: 100%;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. THE PERFECT MATH ENGINE (SymPy) ---
def solve_with_sympy(query):
    x = symbols('x')
    
    # PRE-PROCESSING: Clean the input for Python
    # 1. Replace powers: "x^2" -> "x**2"
    # 2. Replace "=" with "-" so "2x = 6" becomes "2x - 6" (Expression equals 0)
    clean_query = query.lower().replace("^", "**").replace("=", "-")
    
    # DEFINING RULES: Allow "2x" to be read as "2*x"
    transformations = (standard_transformations + (implicit_multiplication_application,))
    
    try:
        # A. CALCULUS: "Derive 2x^2"
        if "derive" in clean_query or "differentiate" in clean_query:
            # Remove keywords to isolate the math
            clean_query = clean_query.replace("derive", "").replace("differentiate", "")
            
            # Parse and Calculate
            expr = parse_expr(clean_query, transformations=transformations)
            result = diff(expr, x)
            return f"Calculated Derivative: {result}"
            
        elif "integrate" in clean_query:
            clean_query = clean_query.replace("integrate", "")
            expr = parse_expr(clean_query, transformations=transformations)
            result = integrate(expr, x)
            return f"Calculated Integral: {result} + C"
            
        # B. ALGEBRA: "Solve 2x^3 - ... = 0"
        elif "solve" in clean_query:
            clean_query = clean_query.replace("solve", "")
            
            # Parse using the "Human" rules
            expr = parse_expr(clean_query, transformations=transformations)
            
            # Solve for x (Roots)
            result = solve(expr, x)
            return f"Exact Roots: {result}"

        # Default Fallback: Try to solve whatever is typed as an equation = 0
        else:
            expr = parse_expr(clean_query, transformations=transformations)
            result = solve(expr, x)
            return f"Exact Answer: {result}"

    except Exception as e:
        return f"ERROR: {str(e)}"

# --- 2. THE AI SOLVER (PHOTOMATH STYLE) ---
def ask_tutor_stream(subject, topic, math_context=None):
    
    # LOGIC: If we have a verified answer, force "Marking Memo" mode
    if math_context and "ERROR" not in math_context:
        system_prompt = f"""
        ROLE: Automated Math Solver (Photomath Style).
        TASK: Show the vertical calculation steps to reach the answer: {math_context}
        
        STRICT VISUAL RULES:
        1. NO paragraphs or conversational filler (e.g., "Let's assume...").
        2. Output ONLY the math steps in vertical order.
        3. Use LaTeX display mode ($$ ... $$) for EVERY line.
        4. Format it exactly like a student's exam paper.
        
        EXAMPLE FORMAT:
        $$ 2x^2 + 5x - 3 = 0 $$
        $$ (2x - 1)(x + 3) = 0 $$
        $$ 2x - 1 = 0 \\quad \\text{{or}} \\quad x + 3 = 0 $$
        $$ x = \\frac{{1}}{{2}} \\quad \\text{{or}} \\quad x = -3 $$
        """
    else:
        # Fallback for Physics/Theory (Still kept structured)
        system_prompt = f"""
        ROLE: Science Marking Memo Generator.
        SUBJECT: {subject}
        
        INSTRUCTIONS:
        1. Provide the solution in clear, vertical steps.
        2. State the Formula first.
        3. Show Substitution.
        4. Show Final Answer.
        5. Use LaTeX ($$) for all math.
        """
    
    try:
        # Check if model exists
        try:
            ollama.show('qwen2.5:1.5b')
        except:
            return "⚠️ Error: The model 'qwen2.5:1.5b' is not found. Please run `ollama pull qwen2.5:1.5b`."

        stream = ollama.chat(
            model='qwen2.5:1.5b', 
            messages=[{'role': 'system', 'content': system_prompt}, 
                      {'role': 'user', 'content': f"Solve this: {topic}"}],
            stream=True
        )
        return stream
    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. UI LAYOUT ---
st.markdown('<h1 style="text-align: center; color: #00D4FF;">🔬 Ukufunda-Sci</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #aaa;">Engine: SymPy (Math) + Qwen (Steps)</p>', unsafe_allow_html=True)

# Input Container
with st.container():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        subject = st.selectbox(
            "Select Subject:",
            ["Pure Mathematics", "Physical Sciences", "Chemistry"]
        )
    
    with col2:
        topic = st.text_input("Enter Problem:", placeholder="e.g. Solve 2x^3 - 3x^2 - 11x + 6 = 0")

# Action Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 **Show Calculation**", type="primary"):
    if not topic.strip():
        st.warning("⚠️ Please enter a problem first!")
    else:
        st.markdown("---")
        
        # 1. RUN THE MATH ENGINE (SymPy)
        math_result = solve_with_sympy(topic)
        
        # Display Engine Status
        if math_result:
            if "ERROR" in math_result:
                # If SymPy fails, show red error
                st.markdown(f'<div class="error-box">⚠️ <b>Math Engine Warning:</b> {math_result}</div>', unsafe_allow_html=True)
            else:
                # If SymPy succeeds, show green success box
                st.markdown(f'<div class="success-box">✅ <b>Verified Result:</b> {math_result}</div>', unsafe_allow_html=True)
        
        # 2. RUN THE AI SOLVER
        st.markdown(f"### 📝 **Step-by-Step Solution**")
        response_placeholder = st.empty()
        full_text = ""
        
        try:
            stream = ask_tutor_stream(subject, topic, math_context=math_result)
            
            if isinstance(stream, str):
                st.error(stream) 
            else:
                for chunk in stream:
                    content = chunk['message']['content']
                    full_text += content
                    response_placeholder.markdown(f'<div class="result-card">{full_text}▌</div>', unsafe_allow_html=True)
                
                response_placeholder.markdown(f'<div class="result-card">{full_text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")