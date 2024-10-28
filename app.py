import streamlit as st
import matplotlib.pyplot as plt
from lsystem import derivation, generate_coordinates, SYSTEM_RULES
import concurrent.futures


# Function to calculate rule complexity
def calculate_rule_complexity(rules):
    def single_rule_complexity(rule):
        # Basic metrics
        length = len(rule)
        unique_symbols = len(set(rule))
        rotations = rule.count('+') + rule.count('-')
        branches = rule.count('[') + rule.count(']')
        variables = sum(1 for c in rule if c.isalpha())

        # Weighted complexity score
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

        return {
            'length': length,
            'unique_symbols': unique_symbols,
            'rotations': rotations,
            'branches': branches,
            'variables': variables,
            'complexity_score': complexity_score
        }

    # Calculate complexity for each rule
    rule_complexities = {
        variable: single_rule_complexity(production)
        for variable, production in rules.items()
    }

    total_complexity = sum(rc['complexity_score'] for rc in rule_complexities.values())
    avg_complexity = total_complexity / len(rules) if rules else 0

    return {
        'rule_complexities': rule_complexities,
        'total_complexity': total_complexity,
        'average_complexity': avg_complexity,
        'num_rules': len(rules)
    }


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

# Display rule complexity
complexity_metrics = calculate_rule_complexity(SYSTEM_RULES)
st.sidebar.subheader("Rule Complexity Metrics")
st.sidebar.write(f"Total Complexity: {complexity_metrics['total_complexity']:.2f}")
st.sidebar.write(f"Average Complexity: {complexity_metrics['average_complexity']:.2f}")
st.sidebar.write(f"Number of Rules: {complexity_metrics['num_rules']}")

st.sidebar.write("Individual Rule Complexities:")
for var, metrics in complexity_metrics['rule_complexities'].items():
    st.sidebar.write(f"{var}: {metrics['complexity_score']:.2f}")


# Function to safely run derivation with timeout
def safe_derivation(start_axiom, steps, timeout=5):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(derivation, start_axiom, steps)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            st.warning("Generation took too long and was stopped. Try reducing iterations or simplifying the rules.")
            return None


# Plotting function with unique variable names
def plot_l_system(plot_coordinates):
    plot_figure, plot_axis = plt.subplots(
        figsize=(3.5, 3.5))  # Standard size; scaling is managed by Streamlit width control
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