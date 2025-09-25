import streamlit as st
import matplotlib.pyplot as plt
from lsystem import (
    derivation, 
    generate_coordinates, 
    parse_rules_from_string,
    LSystemConfig,
    create_l_system,
    list_presets,
    get_preset_config,
    LSystemError
)
import concurrent.futures

# Title and Description
st.title("2D L-System Fractal Generator")
st.write(
    "Create fractal patterns using Lindenmayer Systems (L-Systems). Adjust the parameters in the sidebar to generate your custom fractal pattern."
)

# Sidebar Inputs for L-System Parameters
st.sidebar.header("L-System Parameters")

# Preset selection
presets = list_presets()
use_preset = st.sidebar.selectbox("Choose preset or custom", ["Custom"] + presets)

if use_preset != "Custom":
    try:
        preset_config = get_preset_config(use_preset)
        axiom_input = preset_config.axiom
        rules_input = "\n".join([f"{k} -> {v}" for k, v in preset_config.rules.items()])
        iterations = preset_config.iterations
        initial_heading = preset_config.initial_heading
        angle_increment = preset_config.angle_increment
        segment_length = preset_config.segment_length
        
        # Show preset info
        st.sidebar.info(f"Using preset: {use_preset}")
        
        # Allow users to override preset values
        if st.sidebar.checkbox("Override preset values"):
            axiom_input = st.sidebar.text_input("Axiom (Starting Sequence)", axiom_input)
            rules_input = st.sidebar.text_area("Rules", rules_input)
            iterations = st.sidebar.slider("Iterations", min_value=1, max_value=10, value=iterations)
            initial_heading = st.sidebar.number_input("Initial Heading (degrees)", min_value=0, max_value=360, value=initial_heading)
            angle_increment = st.sidebar.number_input("Angle Increment", min_value=0, max_value=360, value=angle_increment)
            segment_length = st.sidebar.number_input("Segment Length", min_value=0.1, max_value=10.0, value=segment_length)
    except LSystemError as e:
        st.sidebar.error(f"Error loading preset: {e}")
        use_preset = "Custom"

if use_preset == "Custom":
    axiom_input = st.sidebar.text_input("Axiom (Starting Sequence)", "F-F-F-F")
    rules_input = st.sidebar.text_area("Rules (e.g., F -> F+F-F-F+F)", "F -> F-G+F+G-F\nG -> GG")
    iterations = st.sidebar.slider("Iterations", min_value=1, max_value=10, value=5)
    initial_heading = st.sidebar.number_input("Initial Heading (degrees)", min_value=0, max_value=360, value=0)
    angle_increment = st.sidebar.number_input("Angle Increment", min_value=0, max_value=360, value=120)
    segment_length = st.sidebar.number_input("Segment Length", min_value=0.1, max_value=10.0, value=1.0)

# Process rules input
try:
    system_rules = parse_rules_from_string(rules_input)
    if not system_rules:
        st.sidebar.warning("No valid rules found. Please enter rules in format 'symbol -> replacement'")
except LSystemError as e:
    st.sidebar.error(f"Error parsing rules: {e}")
    system_rules = {}


def calculate_rule_complexity(rules_data, num_iterations=1, angle_measure=0):
    """
    Calculate complexity metrics for L-system rules, including angle_increment.
    """
    def single_rule_complexity(rule_text):
        length = len(rule_text)
        unique_symbols = len(set(rule_text))
        rotations = rule_text.count('+') + rule_text.count('-')
        branches = rule_text.count('[') + rule_text.count(']')
        variables = sum(1 for c in rule_text if c.isalpha())

        weights = {
            'length': 0.5,
            'unique': 1.0,
            'rotation': 1.5,
            'branch': 2.0,
            'variable': 1.0,
            'angle': 0.02
        }

        base_complexity = (
            length * weights['length'] +
            unique_symbols * weights['unique'] +
            rotations * weights['rotation'] +
            branches * weights['branch'] +
            variables * weights['variable'] +
            angle_measure * weights['angle']
        )

        iteration_factor = 1 + (num_iterations * 0.5)
        return base_complexity * iteration_factor

    individual_complexity_scores = {var: single_rule_complexity(rule) for var, rule in rules_data.items()}
    total_complexity_score = sum(individual_complexity_scores.values())
    average_complexity = total_complexity_score / len(rules_data) if rules_data else 0

    return total_complexity_score, average_complexity, individual_complexity_scores


# Display rule complexity in real-time
if system_rules:
    total_complexity, avg_complexity, individual_complexities = calculate_rule_complexity(
        system_rules, iterations, angle_increment
    )
    st.sidebar.subheader("Rule Complexity Metrics")
    st.sidebar.markdown(f"""
    Total Complexity: {total_complexity:.2f}  
    Average Complexity: {avg_complexity:.2f}  
    Individual Rule Complexities:  
    {chr(10).join(f'{var}: {comp:.2f}' for var, comp in individual_complexities.items())}
    """)
else:
    st.sidebar.subheader("Rule Complexity Metrics")
    st.sidebar.warning("No rules defined")


# Function to safely create L-System with timeout
def safe_create_l_system(config, timeout=10):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(create_l_system, config)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            st.warning("Generation took too long and was stopped. Try reducing iterations or simplifying the rules.")
            return None
        except LSystemError as e:
            st.error(f"L-System error: {e}")
            return None


# Plotting function
def plot_l_system(plt_coordinates):
    figure, axis = plt.subplots(figsize=(3.5, 3.5))
    axis.plot(*zip(*plt_coordinates), lw=0.3, color="forestgreen")
    axis.axis("equal")
    axis.axis("off")
    return figure


# Generate and display the L-System fractal
if st.sidebar.button("Generate L-System"):
    if not system_rules:
        st.error("Please define at least one rule before generating.")
    else:
        try:
            config = LSystemConfig(
                axiom=axiom_input,
                rules=system_rules,
                iterations=iterations,
                segment_length=segment_length,
                initial_heading=initial_heading,
                angle_increment=angle_increment
            )
            
            result = safe_create_l_system(config)
            if result:
                l_system_sequence, plot_coordinates = result
                l_system_figure = plot_l_system(plot_coordinates)
                st.pyplot(l_system_figure, use_container_width=False)
                
                # Display statistics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Sequence Length", len(l_system_sequence))
                with col2:
                    st.metric("Coordinate Points", len(plot_coordinates))
        except Exception as e:
            st.error(f"Error creating L-System: {e}")

# Footer in Sidebar with smaller GitHub link
st.sidebar.markdown("""
---
#### See my original Python code on GitHub:  
[ambron60/l-system-drawing](https://github.com/ambron60/l-system-drawing)
""", unsafe_allow_html=True)