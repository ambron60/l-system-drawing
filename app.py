import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, generate_coordinates, SYSTEM_RULES
import concurrent.futures

# Title and Description
st.title("L-System Fractal Generator")
st.write(
    "Create fractal patterns using Lindenmayer Systems (L-Systems). Adjust the parameters in the sidebar and generate your custom fractal pattern.")

# Sidebar Inputs for L-System Parameters

# Initialize session state for each input field if not already set
if 'axiom' not in st.session_state:
    st.session_state['axiom'] = "F-F-F-F"
if 'rules' not in st.session_state:
    st.session_state['rules'] = "F -> F-G+F+G-F\nG -> GG"
if 'iterations' not in st.session_state:
    st.session_state['iterations'] = 5
if 'initial_heading' not in st.session_state:
    st.session_state['initial_heading'] = 0
if 'angle_increment' not in st.session_state:
    st.session_state['angle_increment'] = 120

# Sidebar inputs, linked to session state for reset capability
axiom_input = st.sidebar.text_input("Axiom (Starting Sequence)", st.session_state['axiom'], key='axiom')
rules_input = st.sidebar.text_area("Rules (e.g., F -> F+F-F-F+F)", st.session_state['rules'], key='rules')
iterations = st.sidebar.slider("Iterations", min_value=1, max_value=10, value=st.session_state['iterations'], key='iterations')
initial_heading = st.sidebar.number_input("Initial Heading (degrees)", min_value=0, max_value=360, value=st.session_state['initial_heading'], key='initial_heading')
angle_increment = st.sidebar.number_input("Angle Increment", min_value=0, max_value=360, value=st.session_state['angle_increment'], key='angle_increment')

# Clear All button sets fields to neutral values
if st.sidebar.button("Clear All Fields"):
    st.session_state['axiom'] = ""  # Empty string for text fields
    st.session_state['rules'] = ""
    st.session_state['iterations'] = 1  # Minimum slider value for stability
    st.session_state['initial_heading'] = 0  # Neutral direction for heading
    st.session_state['angle_increment'] = 0  # Neutral angle increment

# Process rules input into SYSTEM_RULES
SYSTEM_RULES.clear()
for line in rules_input.splitlines():
    if "->" in line:
        key, value = map(str.strip, line.split("->"))
        SYSTEM_RULES[key] = value

# Function to safely run derivation with timeout
def safe_derivation(start_axiom, steps, timeout=5):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(derivation, start_axiom, steps)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            st.warning("Generation took too long and was stopped. Try reducing iterations or simplifying the rules.")
            return None

# Function to estimate complexity based on initial iterations
def estimate_complexity(start_axiom, rules, estimate_iters=3):
    derived = start_axiom
    for _ in range(estimate_iters):
        derived = ''.join(rules.get(char, char) for char in derived)
    return len(derived)

# Display complexity estimation warning if necessary
complexity = estimate_complexity(axiom_input, SYSTEM_RULES, 3)
if complexity > 500:
    st.warning("High complexity detected. Consider reducing iterations or simplifying the axiom/rules.")

# Plotting function with unique variable names
def plot_l_system(plot_coordinates):
    plot_figure, plot_axis = plt.subplots(figsize=(3.5, 3.5))  # Standard size; scaling is managed by Streamlit width control
    plot_axis.plot(*zip(*plot_coordinates), lw=0.3, color="forestgreen")
    plot_axis.axis("equal")
    plot_axis.axis("off")
    return plot_figure

# Generate and display the L-System fractal
if st.sidebar.button("Generate L-System"):
    l_system_sequence = safe_derivation(axiom_input, iterations)
    if l_system_sequence:
        coordinates = generate_coordinates(l_system_sequence, 1, initial_heading, angle_increment)
        fig = plot_l_system(coordinates)
        st.pyplot(fig, use_container_width=False)

# Footer in Sidebar with smaller GitHub link
st.sidebar.markdown("""
---
#### See my original Python code on GitHub:  
[ambron60/l-system-drawing](https://github.com/ambron60/l-system-drawing)
""", unsafe_allow_html=True)