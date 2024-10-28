import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, generate_coordinates, SYSTEM_RULES
import concurrent.futures

# Title and Description
st.title("L-System Fractal Generator")
st.write(
    "Create fractal patterns using Lindenmayer Systems (L-Systems). Adjust the parameters in the sidebar to generate your custom fractal pattern.")

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

def calculate_rule_complexity(rules_data):
    """
    Calculate complexity metrics for L-system rules
    """
    def single_rule_complexity(rule_text):
        length = len(rule_text)
        unique_symbols = len(set(rule_text))
        rotations = rule_text.count('+') + rule_text.count('-')
        branches = rule_text.count('[') + rule_text.count(']')
        variables = sum(1 for c in rule_text if c.isalpha())

        weights = {
            'length': 1.0,
            'unique': 1.5,
            'rotation': 2.0,
            'branch': 3.0,
            'variable': 1.5
        }

        complexity_score = (
            length * weights['length'] +
            unique_symbols * weights['unique'] +
            rotations * weights['rotation'] +
            branches * weights['branch'] +
            variables * weights['variable']
        )

        return complexity_score

    # Calculate individual rule complexities
    individual_complexities = {var: single_rule_complexity(rule) for var, rule in rules_data.items()}
    total_complexity = sum(individual_complexities.values())
    avg_complexity = total_complexity / len(rules_data) if rules_data else 0

    return total_complexity, avg_complexity, individual_complexities

# Display rule complexity in real-time
total_complexity, avg_complexity, individual_complexities = calculate_rule_complexity(SYSTEM_RULES)
st.sidebar.subheader("Rule Complexity Metrics")
st.sidebar.write(f"Total Complexity: {total_complexity:.2f}")
st.sidebar.write(f"Average Complexity: {avg_complexity:.2f}")
st.sidebar.write("Individual Rule Complexities:")
for var, complexity in individual_complexities.items():
    st.sidebar.write(f"{var}: {complexity:.2f}")

# Function to safely run derivation with timeout
def safe_derivation(start_axiom, steps, timeout=5):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(derivation, start_axiom, steps)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            st.warning("Generation took too long and was stopped. Try reducing iterations or simplifying the rules.")
            return None

# Plotting function
def plot_l_system(plot_coordinates):
    figure, axis = plt.subplots(figsize=(3.5, 3.5))
    axis.plot(*zip(*plot_coordinates), lw=0.3, color="forestgreen")
    axis.axis("equal")
    axis.axis("off")
    return figure

# Generate and display the L-System fractal
if st.sidebar.button("Generate L-System"):
    l_system_sequence = safe_derivation(axiom_input, iterations)
    if l_system_sequence:
        plot_coordinates = generate_coordinates(l_system_sequence, 1, initial_heading, angle_increment)
        l_system_figure = plot_l_system(plot_coordinates)
        st.pyplot(l_system_figure, use_container_width=False)

# Footer in Sidebar with smaller GitHub link
st.sidebar.markdown("""
---
#### See my original Python code on GitHub:  
[ambron60/l-system-drawing](https://github.com/ambron60/l-system-drawing)
""", unsafe_allow_html=True)