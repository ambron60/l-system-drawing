import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, generate_coordinates, SYSTEM_RULES
import concurrent.futures

# Title and Description
st.title("L-System Fractal Generator")
st.write(
    "Create fractal patterns using Lindenmayer Systems (L-Systems). Adjust the parameters in the sidebar and generate your custom fractal pattern.")

# Sidebar Inputs for L-System Parameters
st.sidebar.header("L-System Parameters")
axiom_input = st.sidebar.text_input("Axiom (Starting Sequence)", "F-F-F-F")
rules_input = st.sidebar.text_area("Rules (e.g., F -> F+F-F-F+F)", "F -> F-G+F+G-F\nG -> GG")
iterations = st.sidebar.slider("Iterations", min_value=1, max_value=10, value=5)
initial_heading = st.sidebar.number_input("Initial Heading (degrees)", min_value=0, max_value=360, value=0)
angle_increment = st.sidebar.number_input("Angle Increment", min_value=0, max_value=360, value=120)

# Process rules input into SYSTEM_RULES
SYSTEM_RULES.clear()
for line in rules_input.splitlines():
    if "->" in line:
        key, value = map(str.strip, line.split("->"))
        SYSTEM_RULES[key] = value

# Function to safely run derivation with timeout
def safe_derivation(start_axiom, steps, timeout=10):
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
    plot_axis.plot(*zip(*plot_coordinates), lw=0.3, color="blue")
    plot_axis.axis("equal")
    plot_axis.axis("off")
    return plot_figure

# Conditional confirmation button for high iterations
generate_confirm = True if iterations <= 5 else st.sidebar.button("Confirm High Iteration Count")
if generate_confirm and st.sidebar.button("Generate L-System"):
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