import streamlit as st
import json
import time
from utils.run_main import run_main_script

# Initialize session state
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
    st.session_state.user_data = {}
    st.session_state.model_deployed = False
    st.session_state.logs = ""
    st.session_state.output_data = None

# List of input fields
fields = [
    ("name", "Enter your name"),
    ("phone", "Enter your phone number"),
    ("paytm_link", "Enter your Paytm link"),
    ("country", "Enter your country"),
    ("age", "Enter your age"),
    ("email", "Enter your email"),
    ("num_permutations", "Enter number of permutations you want")
]

st.title("📦 AML Permutation Generator")

# Phase 1: Deploy Model Button
if not st.session_state.model_deployed:
    st.subheader("Start the system")
    if st.button("🚀 Deploy Model"):
        st.session_state.model_deployed = True
        st.rerun()

# Phase 2: Dynamic Input Form
elif st.session_state.current_step < len(fields):
    key, prompt = fields[st.session_state.current_step]
    user_input = st.text_input(prompt, key=key)
    if user_input:
        st.session_state.user_data[key] = user_input
        st.session_state.current_step += 1
        st.rerun()

# Phase 3: Run `main.py` and display logs/output
else:
    st.sidebar.header("📝 Inputs")
    st.sidebar.json(st.session_state.user_data)

    with st.spinner("Running model and generating output..."):
        logs, output_data = run_main_script(st.session_state.user_data)
        st.session_state.logs = logs
        st.session_state.output_data = output_data

    # Right side: Logs
    st.subheader("🔧 Process Logs")
    st.text(st.session_state.logs)

    # Center: Output file
    st.subheader("📤 Output File")
    if st.session_state.output_data:
        st.json(st.session_state.output_data)
    else:
        st.error("No output generated.")
