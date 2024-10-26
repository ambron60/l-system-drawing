import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, generate_coordinates, SYSTEM_RULES

# Title and Description
st.title("L-System Fractal Generator")
st.write(
    "Create fractal patterns using Lindenmayer Systems (L-Systems). Adjust the parameters in the sidebar and generate your custom fractal pattern.")

# Sidebar Inputs for L-System Parameters
st.sidebar.header("L-System Parameters")
axiom = st.sidebar.text_input("Axiom (Starting Sequence)", "F+XF+F+XF")
rules_input = st.sidebar.text_area("Rules (e.g., F -> F+F-F-F+F)", "X -> XF-F+F-XF+F+XF-F+F-X")
iterations = st.sidebar.slider("Iterations", min_value=1, max_value=10, value=4)
initial_heading = st.sidebar.number_input("Initial Heading (degrees)", min_value=0, max_value=360, value=0)
angle_increment = st.sidebar.number_input("Angle Increment", min_value=0, max_value=360, value=90)

# Process rules input into SYSTEM_RULES
SYSTEM_RULES.clear()
for line in rules_input.splitlines():
    if "->" in line:
        key, value = map(str.strip, line.split("->"))
        SYSTEM_RULES[key] = value

# Plotting function with unique variable names
def plot_l_system(plot_coordinates):
    plot_figure, plot_axis = plt.subplots(figsize=(3.5, 3.5))  # Standard size; scaling is managed by Streamlit width control
    plot_axis.plot(*zip(*plot_coordinates), lw=0.4, color="black")
    plot_axis.axis("equal")
    plot_axis.axis("off")
    return plot_figure

# Generate and display the L-System fractal
if st.sidebar.button("Generate L-System"):
    generated_sequence = derivation(axiom, iterations)
    generated_coordinates = generate_coordinates(generated_sequence, 1, initial_heading, angle_increment)
    fractal_figure = plot_l_system(generated_coordinates)
    st.pyplot(fractal_figure, use_container_width=False)

# Footer in Sidebar with smaller GitHub link
st.sidebar.markdown("""
---
#### See my original Python code on GitHub:  
[ambron60/l-system-drawing](https://github.com/ambron60/l-system-drawing)
""", unsafe_allow_html=True)