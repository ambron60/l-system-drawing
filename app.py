import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, draw_l_system, initialize_turtle, SYSTEM_RULES

# Streamlit app configuration
st.title("L-System Fractal Generator")
st.write("Create fractal patterns using Lindenmayer Systems (L-Systems).")

# User inputs for the L-System parameters
axiom = st.text_input("Axiom", "F")
rules_input = st.text_area("Rules (e.g., F -> F+F-F-F+F)", "F -> F+F-F-F+F")
angle = st.number_input("Angle (degrees)", min_value=0, max_value=360, value=90)
iterations = st.slider("Iterations", min_value=1, max_value=10, value=4)
segment_length = st.number_input("Segment Length", min_value=1, max_value=20, value=5)
initial_heading = st.number_input("Initial Heading", min_value=0, max_value=360, value=90)


# Process the rules input into a dictionary
SYSTEM_RULES.clear()  # Clear any existing rules
for line in rules_input.splitlines():
    if "->" in line:
        key, value = line.split("->")
        SYSTEM_RULES[key.strip()] = value.strip()

# Generate the L-System sequence based on user inputs
if st.button("Generate L-System"):
    # Generate the sequence with the given axiom and rules
    l_system_sequence = derivation(axiom, iterations)

    # Set up Matplotlib figure for plotting the L-System
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.axis("equal")
    ax.axis("off")
    ax.set_title("L-System Fractal Pattern")

    # Initialize turtle for drawing the L-System
    turtle_instance = initialize_turtle(initial_heading)
    draw_l_system(turtle_instance, l_system_sequence, segment_length, angle)

    # Display the Matplotlib figure in Streamlit
    st.pyplot(fig)