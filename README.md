Bhala-Smart: CAPS Essay Assistant
Bhala-Smart is a local AI writing tutor designed specifically for the South African educational context. Built using Ollama and the llama3.2 model, it serves as a specialized critique tool for Grade 12 English First Additional Language (FAL) students.

Unlike standard AI tools that simply rewrite text, Bhala-Smart is engineered to act as a strict South African educator. It provides critical feedback based on the CAPS curriculum guidelines, ensuring students improve their own writing skills rather than relying on automated generation.

Key Features
CAPS Alignment: Evaluates structure, tone, and language according to Grade 12 standards.

South Africanism Detection: Automatically flags informal local slang (e.g., eish, bra, yebo, sharp-sharp) that is inappropriate for formal academic essays.

Grammar Focus: Deep-scans for common mechanical errors like comma splices and run-on sentences.

No-Rewrite Policy: Follows a strict rule to critique only, forcing the student to perform the actual edits.

Privacy-First: Runs locally via Ollama; no student data is sent to external cloud APIs.

Prerequisites
Ollama: Download and install Ollama

Model: Pull the Llama 3.2 model:

Bash
ollama pull llama3.2
Python: Version 3.8 or higher.

Installation
Clone the repository:

Bash
git clone https://github.com/timburg23/bhala-tutor-personal.git
cd bhala-smart
Install dependencies:

Bash
pip install ollama
Complete Source Code (bhala_tutor.py)
Python
import ollama
import sys

def bhala_tutor(essay_text):
    """
    Bhala-Smart: CAPS ESSAY ASSISTANT (v1)
    Provides critical feedback for Grade 12 English FAL essays.
    """
    
    system_prompt = (
        "You are a strict South African Grade 12 English FAL teacher. "
        "Your goal is to critique the student's essay based on CAPS standards. "
        "Rules:\n"
        "1. Do NOT rewrite the essay for the student.\n"
        "2. Identify informal South Africanisms (e.g., 'eish', 'bra', 'yebo', 'sharp-sharp', 'mzansi') "
        "and mark them as inappropriate for formal writing.\n"
        "3. Check for comma splices and run-on sentences.\n"
        "4. Provide bulleted feedback on Structure, Language, and Tone.\n"
        "5. Keep the tone professional, firm, but encouraging."
    )

    try:
        # Ensure the ollama server is running before calling this
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Please critique my essay:\n\n{essay_text}"}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def main():
    print("==========================================")
    print("   BHALA-SMART: CAPS ESSAY ASSISTANT v1   ")
    print("==========================================\n")
    
    print("Enter/Paste your essay below. Press Ctrl-D (or Ctrl-Z on Windows) and Enter to save:\n")
    
    try:
        user_essay = sys.stdin.read()
    except EOFError:
        pass

    if user_essay.strip():
        print("\n--- Teacher is marking... Please wait ---\n")
        feedback = bhala_tutor(user_essay)
        print("--- TEACHER FEEDBACK ---\n")
        print(feedback)
    else:
        print("Error: No essay content detected.")

if __name__ == "__main__":
    main()
Usage
Run the script:

Bash
python bhala_tutor.py
Paste your essay text into the terminal.

Receive structured feedback categorized by Structure, Language, and Tone.
