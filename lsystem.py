import sys
import math
import matplotlib.pyplot as plt

# Global dictionary to store L-System rules
SYSTEM_RULES = {}


def get_system_rules():
    """Collects user input rules for the L-System."""
    rule_num = 1
    while True:
        rule = input(f"Enter rule[{rule_num}]: rewrite term (0 when done): ")
        if rule == '0':
            break
        try:
            key, value = map(str.strip, rule.split("->"))
            SYSTEM_RULES[key] = value
            rule_num += 1
        except ValueError:
            print("Invalid format. Use `symbol->replacement` format.")
    return SYSTEM_RULES


def derivation(axiom, steps):
    """Generates an L-System sequence for a given axiom and number of steps."""
    derived = axiom
    for _ in range(steps):
        derived = ''.join(SYSTEM_RULES.get(char, char) for char in derived)
    return derived


def generate_coordinates(sequence, seg_length, initial_heading, angle_increment):
    """
    Generates a list of coordinates based on the L-System sequence.

    Parameters:
        sequence (str): The L-System sequence to interpret.
        seg_length (float): The length of each forward step.
        initial_heading (float): The initial direction of drawing in degrees.
        angle_increment (float): The angle increment for each rotation command.

    Returns:
        list of tuples: Each tuple contains (x, y) coordinates for plotting.
    """
    x, y = 0, 0  # Starting position
    heading = initial_heading  # Start with the initial heading
    coordinates = [(x, y)]
    stack = []

    for command in sequence:
        if command in "FGRL":
            # Move forward in the current direction
            x += seg_length * math.cos(math.radians(heading))
            y += seg_length * math.sin(math.radians(heading))
            coordinates.append((x, y))
        elif command == "+":
            heading -= angle_increment  # Rotate clockwise
        elif command == "-":
            heading += angle_increment  # Rotate counterclockwise
        elif command == "[":
            stack.append((x, y, heading))
        elif command == "]":
            x, y, heading = stack.pop()
            coordinates.append((x, y))

    return coordinates


def plot_l_system(coordinates):
    """Plots the L-System based on generated coordinates."""
    plt.figure(figsize=(8, 8))
    plt.plot(*zip(*coordinates), lw=0.5)
    plt.axis("equal")
    plt.axis("off")
    plt.show()


def main():
    # Collect system rules and parameters
    get_system_rules()
    axiom = input("Enter axiom (starting sequence): ")
    iterations = int(input("Enter number of iterations: "))
    segment_length = int(input("Enter segment length: "))
    initial_heading = float(input("Enter initial heading (alpha-0): "))
    angle_increment = float(input("Enter angle increment: "))

    # Generate L-System sequence
    final_sequence = derivation(axiom, iterations)

    # Generate coordinates for plotting with both heading and angle
    coordinates = generate_coordinates(final_sequence, segment_length, initial_heading, angle_increment)

    # Plot the L-System
    plot_l_system(coordinates)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        sys.exit(0)
