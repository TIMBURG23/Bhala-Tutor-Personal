import streamlit as st
import ollama
import json
import os
import re

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bhala-Smart",
    page_icon="🇿🇦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE MEMORY (DATABASE) ---
class StatsManager:
    def __init__(self):
        self.filename = "bhala_stats.json"
        
    def load_stats(self):
        if not os.path.exists(self.filename):
            return {"essays_marked": 0, "total_score": 0}
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except:
            return {"essays_marked": 0, "total_score": 0}

    def update_stats(self, score):
        data = self.load_stats()
        data["essays_marked"] += 1
        data["total_score"] += score
        with open(self.filename, "w") as f:
            json.dump(data, f)
        return data

    def get_average(self):
        data = self.load_stats()
        if data["essays_marked"] == 0:
            return 0
        return int(data["total_score"] / data["essays_marked"])

# --- 3. CUSTOM STYLING (FULL CSS RESTORED) ---
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #ff6b6b;
    }
    
    .grading-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4ecdc4;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .reference-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffe66d;
        margin-bottom: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ff8e53);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255,107,107,0.3);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        font-size: 16px;
        transition: border-color 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #4ecdc4;
        box-shadow: 0 0 0 2px rgba(78,205,196,0.2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4ecdc4 !important;
        color: white !important;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        background: #ffe66d;
        color: #333;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    
    /* Custom header */
    .header-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Grade indicator */
    .grade-indicator {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. THE BRAIN ---
class BhalaSmartGrader:
    def check_grammar(self, text):
        prompt = """
        TASK: Identify ONLY spelling, punctuation, and strict grammar errors in this South African English text.
        CONTEXT: South African English (Grade 12).
        - IGNORE THESE WORDS (Do not mark as errors): braai, ubuntu, bakkie, gogo, eish, mzansi, lekker, laaitie, bru, ja, nee.
        - MARK THESE ERRORS: "Borrow me" (should be Lend me), "I'm coming" (when going), "Can able to".
        OUTPUT: A bulleted list of errors. If none, say "✅ No mechanical errors found."
        """
        response = ollama.chat(model='llama3.2', messages=[{'role': 'system', 'content': prompt}, {'role': 'user', 'content': text}])
        return response['message']['content']

    def check_feedback(self, text):
        prompt = """
        ROLE: South African English FAL Teacher.
        TASK: Critique Tone, Structure, and Content based on CAPS Rubric.
        GOLDEN RULE:
        - "Bra" = Friend. "Robot" = Traffic Light. "Just now" = Later.
        
        REQUIRED OUTPUT FORMAT:
        1. Give a bulleted critique of the essay structure and tone.
        2. Be encouraging.
        3. On the very last line, write the score exactly like this: SCORE: 80
        """
        response = ollama.chat(model='llama3.2', messages=[{'role': 'system', 'content': prompt}, {'role': 'user', 'content': text}])
        return response['message']['content']

    def extract_score(self, feedback_text):
        try:
            match = re.search(r"SCORE:\s*(\d+)", feedback_text)
            if match:
                return int(match.group(1))
            return 75
        except:
            return 75

# --- 5. INITIALIZATION & CALLBACKS ---
db = StatsManager()
stats = db.load_stats()
avg_score = db.get_average()

if 'essay_input' not in st.session_state:
    st.session_state.essay_input = ""
if 'results_ready' not in st.session_state:
    st.session_state.results_ready = False
if 'saved_grammar' not in st.session_state:
    st.session_state.saved_grammar = ""
if 'saved_feedback' not in st.session_state:
    st.session_state.saved_feedback = ""
if 'saved_score' not in st.session_state:
    st.session_state.saved_score = 0

# --- CALLBACK FUNCTION (Fixes the Crash) ---
def load_template_callback():
    st.session_state.essay_input = "Title: [Enter Title]\n\nIntroduction:\n[State your thesis clearly...]\n\nBody Paragraph 1:\n[Your first point...]\n\nConclusion:\n[Summarize your argument...]"

# --- 6. HEADER ---
st.markdown("""
<div class="header-container">
    <div>
        <h1 style="margin:0; color:#333;">📚 Bhala-Smart</h1>
        <p style="margin:5px 0 0 0; color:#666;">Offline AI Assistant • SA CAPS Aligned</p>
    </div>
    <div class="grade-indicator">
        <span>🇿🇦</span>
        <span>Grade 12 FAL</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 7. MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    # Writing Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ✏️ Your Essay")
    
    student_text = st.text_area(
        " ", 
        height=350,
        key="essay_input",
        placeholder="Start writing your essay here...",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mark Button
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🎯 **Submit for Marking**", use_container_width=True):
            if not st.session_state.essay_input:
                st.warning("Please write your essay first!")
            else:
                grader = BhalaSmartGrader()
                
                with st.spinner("Teacher is reviewing your work..."):
                    # Process Grammar
                    grammar_res = grader.check_grammar(st.session_state.essay_input)
                    
                    # Process Feedback
                    feedback_res = grader.check_feedback(st.session_state.essay_input)
                    score = grader.extract_score(feedback_res)
                    
                    # Save Data
                    db.update_stats(score)
                    
                    st.session_state.saved_grammar = grammar_res
                    st.session_state.saved_feedback = feedback_res
                    st.session_state.saved_score = score
                    st.session_state.results_ready = True
                    
                    st.balloons()

    # Results Section
    if st.session_state.results_ready:
        st.markdown("### 📊 Assessment Results")
        tab1, tab2 = st.tabs(["🔍 **Grammar Check**", "👩‍🏫 **Teacher's Feedback**"])
        
        with tab1:
            st.markdown('<div class="grading-card">', unsafe_allow_html=True)
            st.markdown("#### Grammar & Mechanics")
            st.markdown(st.session_state.saved_grammar)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="grading-card">', unsafe_allow_html=True)
            st.markdown("#### Content & Structure")
            st.markdown(st.session_state.saved_feedback)
            st.divider()
            st.metric("Final Score", f"{st.session_state.saved_score}/100")
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Stats Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📈 Your Progress")
    
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.metric("Essays", stats["essays_marked"])
    with c_m2:
        st.metric("Avg Score", f"{avg_score}%")
    
    st.progress(avg_score)
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    # --- BUTTON WITH CALLBACK (The Fix) ---
    st.button("📝 Load Template", on_click=load_template_callback, use_container_width=True)
        
    if st.button("🔄 Refresh Stats", use_container_width=True):
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Reference Card
    st.markdown('<div class="reference-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Quick Tips")
    
    with st.expander("🚫 **Avoid These**", expanded=True):
        st.markdown("""
        <span class="badge">Gonna</span>
        <span class="badge">Coz</span>
        <span class="badge">Wanna</span>
        <span class="badge">Ain't</span>
        <span class="badge">U</span>
        """, unsafe_allow_html=True)
    
    with st.expander("💎 **Formal Connectors**"):
        st.write("Furthermore, However, Therefore, Consequently, In conclusion")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("**Powered by**\n\n🎯 Llama 3.2 AI")
with f2:
    st.markdown("**Features**\n\n✓ Offline Mode\n✓ SA Context")
with f3:
    st.markdown("**Support**\n\n📧 help@bhalasmart.co.za")

st.markdown("<br><br>", unsafe_allow_html=True)