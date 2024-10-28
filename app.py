import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from lsystem import derivation, generate_coordinates, SYSTEM_RULES
import concurrent.futures


def calculate_rule_complexity(rules_data):
    """
    Enhanced complexity calculator with visualization metrics
    """

    def single_rule_complexity(rule_text):
        # Basic metrics
        metrics = {
            'length': len(rule_text),
            'unique_symbols': len(set(rule_text)),
            'rotations': rule_text.count('+') + rule_text.count('-'),
            'branches': rule_text.count('[') + rule_text.count(']'),
            'variables': sum(1 for c in rule_text if c.isalpha())
        }

        # Weights for different complexity factors
        weights = {
            'length': 1.0,
            'unique': 1.5,
            'rotation': 2.0,
            'branch': 3.0,
            'variable': 1.5
        }

        # Calculate weighted complexity score
        complexity_score = (
                metrics['length'] * weights['length'] +
                metrics['unique_symbols'] * weights['unique'] +
                metrics['rotations'] * weights['rotation'] +
                metrics['branches'] * weights['branch'] +
                metrics['variables'] * weights['variable']
        )

        return complexity_score, metrics

    # Calculate complexity for each rule
    rule_details = {}
    for var_name, prod_rule in rules_data.items():
        score, metrics = single_rule_complexity(prod_rule)
        rule_details[var_name] = {
            'score': score,
            'metrics': metrics
        }

    total_complexity = sum(details['score'] for details in rule_details.values())
    avg_complexity = total_complexity / len(rules_data) if rules_data else 0

    return total_complexity, avg_complexity, rule_details


def display_complexity_metrics(rules):
    """
    Display enhanced complexity metrics with Streamlit components
    """
    total_complexity, avg_complexity, rule_details = calculate_rule_complexity(rules)

    # Create an expander for complexity metrics
    with st.sidebar.expander("Rule Complexity Analysis", expanded=True):
        # Overall complexity metrics
        col1, col2 = st.columns(2)
        col1.metric("Total Complexity", f"{total_complexity:.1f}")
        col2.metric("Avg Complexity", f"{avg_complexity:.1f}")

        # Individual rule analysis
        st.write("---")
        st.write("Individual Rule Analysis:")

        for var_name, details in rule_details.items():
            with st.container():
                st.write(f"**Rule: {var_name}**")

                # Create a horizontal bar chart for rule metrics
                metrics = details['metrics']
                metric_names = list(metrics.keys())
                metric_values = list(metrics.values())

                # Generate bar chart
                fig, ax = plt.subplots(figsize=(6, 2))
                y_pos = np.arange(len(metric_names))
                ax.barh(y_pos, metric_values)
                ax.set_yticks(y_pos)
                ax.set_yticklabels([name.replace('_', ' ').title() for name in metric_names])
                ax.set_xlabel('Count')
                plt.tight_layout()

                # Display the chart
                st.pyplot(fig)

                # Show complexity score
                st.metric("Rule Complexity", f"{details['score']:.1f}")
                st.write("---")


# Update the main Streamlit app code to use the new display function
def main():
    st.title("L-System Fractal Generator")
    st.write("Create fractal patterns using Lindenmayer Systems (L-Systems).")

    # Sidebar inputs
    st.sidebar.header("L-System Parameters")
    axiom_input = st.sidebar.text_input("Axiom", "F-F-F-F")
    rules_input = st.sidebar.text_area("Rules", "F -> F-G+F+G-F\nG -> GG")

    # Process rules and update SYSTEM_RULES
    SYSTEM_RULES.clear()
    for line in rules_input.splitlines():
        if "->" in line:
            key, value = map(str.strip, line.split("->"))
            SYSTEM_RULES[key] = value

    # Display complexity metrics in real-time
    display_complexity_metrics(SYSTEM_RULES)

    # Rest of your existing code for L-System generation and visualization...


if __name__ == "__main__":
    main()