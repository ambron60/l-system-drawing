import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, generate_coordinates, SYSTEM_RULES

# Title and Description
st.title("L-System Fractal Generator")
st.write(
    "Create fractal patterns using Lindenmayer Systems (L-Systems). Adjust the parameters in the sidebar and generate your custom fractal pattern.")

# Sidebar Inputs for L-System Parameters
st.sidebar.header("L-System Parameters")
axiom = st.sidebar.text_input("Axiom (Starting Sequence)", "F-F-F-F")
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


# Plotting function
def plot_l_system(coordinates):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))  # Standard size; scaling is managed by Streamlit width control
    ax.plot(*zip(*coordinates), lw=0.3, color="gray")
    ax.axis("equal")
    ax.axis("off")
    return fig


# Generate and display the L-System fractal
if st.sidebar.button("Generate L-System"):
    l_system_sequence = derivation(axiom, iterations)
    coordinates = generate_coordinates(l_system_sequence, 1, initial_heading, angle_increment)
    fig = plot_l_system(coordinates)
    st.pyplot(fig, use_container_width=False)

# Footer in Sidebar with smaller GitHub link
st.sidebar.markdown("""
---
#### See my original Python code on GitHub:  
[ambron60/l-system-drawing](https://github.com/ambron60/l-system-drawing)
""", unsafe_allow_html=True)
