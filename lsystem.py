import keyboard
import sys
import math
import threading
import matplotlib.pyplot as plt

SYSTEM_RULES = {}


def get_system_rules():
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
    derived = axiom
    for _ in range(steps):
        derived = ''.join(SYSTEM_RULES.get(char, char) for char in derived)
    return derived


def generate_coordinates(sequence, seg_length, initial_heading, angle_increment):
    x, y = 0, 0
    heading = initial_heading
    coordinates = [(x, y)]
    stack = []

    for command in sequence:
        if command in "FGRL":
            x += seg_length * math.cos(math.radians(heading))
            y += seg_length * math.sin(math.radians(heading))
            coordinates.append((x, y))
        elif command == "+":
            heading -= angle_increment
        elif command == "-":
            heading += angle_increment
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


def plot_in_thread(coordinates):
    """Plots in a separate thread and listens for 'q' to quit."""
    # Start the plotting in a separate thread
    plotting_thread = threading.Thread(target=plot_l_system, args=(coordinates,))
    plotting_thread.start()

    # Check for 'q' keypress to quit
    while plotting_thread.is_alive():
        if keyboard.is_pressed('q'):
            print("Quitting drawing...")
            plt.close('all')  # Closes all matplotlib figures
            break


def main():
    get_system_rules()
    axiom = input("Enter axiom (starting sequence): ")
    iterations = int(input("Enter number of iterations: "))
    segment_length = int(input("Enter segment length: "))
    initial_heading = float(input("Enter initial heading (alpha-0): "))
    angle_increment = float(input("Enter angle increment: "))

    # Generate L-System sequence
    final_sequence = derivation(axiom, iterations)
    coordinates = generate_coordinates(final_sequence, segment_length, initial_heading, angle_increment)

    # Start plotting with 'q' to quit functionality
    plot_in_thread(coordinates)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        sys.exit(0)
