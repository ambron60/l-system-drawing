import sys
import math
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LSystemConfig:
    """Configuration class for L-System parameters."""
    axiom: str
    rules: Dict[str, str]
    iterations: int
    segment_length: float
    initial_heading: float
    angle_increment: float
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.iterations < 0:
            raise ValueError("Iterations must be non-negative")
        if self.segment_length <= 0:
            raise ValueError("Segment length must be positive")
        if not self.axiom:
            raise ValueError("Axiom cannot be empty")


class LSystemError(Exception):
    """Custom exception for L-System related errors."""
    pass


def parse_rules_from_string(rules_string: str) -> Dict[str, str]:
    """
    Parse L-System rules from a string format.
    
    Args:
        rules_string: String containing rules in format "symbol -> replacement"
        
    Returns:
        Dictionary mapping symbols to their replacements
        
    Raises:
        LSystemError: If rule format is invalid
    """
    rules = {}
    for line_num, line in enumerate(rules_string.splitlines(), 1):
        line = line.strip()
        if not line or '#' in line:  # Skip empty lines and comments
            continue
            
        if "->" not in line:
            raise LSystemError(f"Invalid rule format on line {line_num}: '{line}'. Use 'symbol -> replacement' format.")
            
        try:
            key, value = map(str.strip, line.split("->", 1))
            if not key:
                raise LSystemError(f"Empty symbol on line {line_num}")
            rules[key] = value
        except ValueError as e:
            raise LSystemError(f"Error parsing rule on line {line_num}: {e}")
    
    return rules


def get_system_rules() -> Dict[str, str]:
    """
    Collects user input rules for the L-System.
    
    Returns:
        Dictionary containing the L-System rules
        
    Raises:
        LSystemError: If input format is invalid
    """
    rules = {}
    rule_num = 1
    
    print("Enter L-System rules in format 'symbol -> replacement' (enter '0' when done):")
    
    while True:
        try:
            rule = input(f"Enter rule[{rule_num}]: ")
            if rule == '0':
                break
                
            parsed_rules = parse_rules_from_string(rule)
            rules.update(parsed_rules)
            rule_num += 1
            
        except LSystemError as e:
            print(f"Error: {e}")
            continue
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)
    
    return rules


def derivation(axiom: str, steps: int, rules: Dict[str, str]) -> str:
    """
    Generates an L-System sequence for a given axiom and number of steps.
    
    Args:
        axiom: The starting sequence
        steps: Number of derivation steps to perform
        rules: Dictionary mapping symbols to their replacements
        
    Returns:
        The derived sequence after applying rules
        
    Raises:
        LSystemError: If derivation fails
    """
    if steps < 0:
        raise LSystemError("Number of steps must be non-negative")
    
    if not axiom:
        raise LSystemError("Axiom cannot be empty")
    
    try:
        derived = axiom
        for _ in range(steps):
            derived = ''.join(rules.get(char, char) for char in derived)
            
            # Safety check to prevent excessive memory usage
            if len(derived) > 1_000_000:
                logger.warning(f"Sequence length exceeded 1M characters after {_ + 1} steps")
                break
                
        return derived
    except Exception as e:
        raise LSystemError(f"Derivation failed: {e}")


def generate_coordinates(sequence: str, seg_length: float, initial_heading: float, 
                        angle_increment: float) -> List[Tuple[float, float]]:
    """
    Generates a list of coordinates based on the L-System sequence.

    Args:
        sequence: The L-System sequence to interpret
        seg_length: The length of each forward step
        initial_heading: The initial direction of drawing in degrees
        angle_increment: The angle increment for each rotation command

    Returns:
        List of (x, y) coordinate tuples for plotting
        
    Raises:
        LSystemError: If coordinate generation fails
    """
    if seg_length <= 0:
        raise LSystemError("Segment length must be positive")
    
    try:
        x, y = 0.0, 0.0  # Starting position
        heading = initial_heading  # Start with the initial heading
        coordinates = [(x, y)]
        stack = []

        for i, command in enumerate(sequence):
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
                if not stack:
                    logger.warning(f"Unmatched ']' at position {i}")
                    continue
                x, y, heading = stack.pop()
                coordinates.append((x, y))
            # Ignore unrecognized commands (like 'G' which might be used in some systems)
        
        if stack:
            logger.warning(f"Unmatched '[' found. Stack size: {len(stack)}")
            
        return coordinates
    except Exception as e:
        raise LSystemError(f"Coordinate generation failed: {e}")


def plot_l_system(coordinates: List[Tuple[float, float]], 
                  figsize: Tuple[int, int] = (8, 8), 
                  line_width: float = 0.5,
                  color: str = "black",
                  title: Optional[str] = None) -> plt.Figure:
    """
    Plots the L-System based on generated coordinates.
    
    Args:
        coordinates: List of (x, y) coordinate tuples
        figsize: Figure size as (width, height)
        line_width: Width of the plot line
        color: Color of the plot line
        title: Optional title for the plot
        
    Returns:
        The matplotlib figure object
    """
    if not coordinates:
        raise LSystemError("Cannot plot empty coordinates")
    
    try:
        fig, ax = plt.subplots(figsize=figsize)
        
        # Extract x and y coordinates
        x_coords, y_coords = zip(*coordinates)
        
        ax.plot(x_coords, y_coords, lw=line_width, color=color)
        ax.set_aspect('equal')
        ax.axis('off')
        
        if title:
            ax.set_title(title, fontsize=14, pad=20)
            
        plt.tight_layout()
        return fig
    except Exception as e:
        raise LSystemError(f"Plotting failed: {e}")


# Preset L-Systems
PRESET_L_SYSTEMS = {
    "dragon_curve": LSystemConfig(
        axiom="FX",
        rules={"X": "X+YF+", "Y": "-FX-Y"},
        iterations=13,
        segment_length=1,
        initial_heading=0,
        angle_increment=90
    ),
    "sierpinski_triangle": LSystemConfig(
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        iterations=6,
        segment_length=1,
        initial_heading=0,
        angle_increment=120
    ),
    "koch_curve": LSystemConfig(
        axiom="F",
        rules={"F": "F+F-F-F+F"},
        iterations=5,
        segment_length=4,
        initial_heading=180,
        angle_increment=90
    ),
    "hilbert_curve": LSystemConfig(
        axiom="A",
        rules={"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
        iterations=6,
        segment_length=1,
        initial_heading=0,
        angle_increment=90
    ),
    "axial_tree": LSystemConfig(
        axiom="X",
        rules={"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        iterations=6,
        segment_length=1,
        initial_heading=90,
        angle_increment=22.5
    ),
}


def get_preset_config(preset_name: str) -> LSystemConfig:
    """
    Get a preset L-System configuration.
    
    Args:
        preset_name: Name of the preset system
        
    Returns:
        LSystemConfig object for the preset
        
    Raises:
        LSystemError: If preset name is not found
    """
    if preset_name not in PRESET_L_SYSTEMS:
        available = ", ".join(PRESET_L_SYSTEMS.keys())
        raise LSystemError(f"Unknown preset '{preset_name}'. Available: {available}")
    
    return PRESET_L_SYSTEMS[preset_name]


def list_presets() -> List[str]:
    """Return a list of available preset L-System names."""
    return list(PRESET_L_SYSTEMS.keys())


def create_l_system(config: LSystemConfig) -> Tuple[str, List[Tuple[float, float]]]:
    """
    Create a complete L-System from configuration.
    
    Args:
        config: LSystemConfig object containing all parameters
        
    Returns:
        Tuple of (final_sequence, coordinates)
        
    Raises:
        LSystemError: If generation fails
    """
    try:
        # Generate L-System sequence
        final_sequence = derivation(config.axiom, config.iterations, config.rules)
        logger.info(f"Generated sequence of length {len(final_sequence)}")
        
        # Generate coordinates for plotting
        coordinates = generate_coordinates(
            final_sequence, 
            config.segment_length, 
            config.initial_heading, 
            config.angle_increment
        )
        logger.info(f"Generated {len(coordinates)} coordinate points")
        
        return final_sequence, coordinates
    except Exception as e:
        raise LSystemError(f"L-System creation failed: {e}")


def main():
    print()
    print("L-System Fractal Generator")
    print("=" * 30)
    
    # Ask user if they want to use a preset
    use_preset = input("Use preset L-System? (y/n): ").lower().strip()
    
    if use_preset == 'y':
        presets = list_presets()
        
        # Display numbered presets
        print("\nAvailable presets:")
        for i, preset in enumerate(presets, 1):
            print(f"  {i}. {preset}")
        
        # Get preset selection with validation
        while True:
            selection = input(f"\nEnter preset number (1-{len(presets)}) or name: ").strip()
            if selection:
                # Try to parse as number first
                try:
                    preset_num = int(selection)
                    if 1 <= preset_num <= len(presets):
                        preset_name = presets[preset_num - 1]
                        config = get_preset_config(preset_name)
                        print(f"Using preset: {preset_name}")
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(presets)}.")
                        continue
                except ValueError:
                    # Not a number, try as preset name
                    try:
                        config = get_preset_config(selection)
                        print(f"Using preset: {selection}")
                        break
                    except LSystemError as e:
                        print(f"Error: {e}")
                        continue
            else:
                print("Please enter a preset number or name, or press Ctrl+C to exit.")
                continue
    else:
        # Collect custom system rules and parameters
        try:
            rules = get_system_rules()
            axiom = input("Enter axiom (starting sequence): ").strip()
            
            # Get iterations with validation
            while True:
                iterations_input = input("Enter number of iterations: ").strip()
                if iterations_input:
                    try:
                        iterations = int(iterations_input)
                        if iterations < 0:
                            print("Iterations must be non-negative. Please try again.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid integer. Try again.")
                        continue
                else:
                    print("Please enter a number of iterations.")
                    continue
            
            # Get segment length with validation
            while True:
                segment_input = input("Enter segment length: ").strip()
                if segment_input:
                    try:
                        segment_length = float(segment_input)
                        if segment_length <= 0:
                            print("Segment length must be positive. Please try again.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number. Try again.")
                        continue
                else:
                    print("Please enter a segment length.")
                    continue
            
            # Get initial heading with validation
            while True:
                heading_input = input("Enter initial heading (degrees): ").strip()
                if heading_input:
                    try:
                        initial_heading = float(heading_input)
                        break
                    except ValueError:
                        print("Please enter a valid number. Try again.")
                        continue
                else:
                    print("Please enter an initial heading.")
                    continue
            
            # Get angle increment with validation
            while True:
                angle_input = input("Enter angle increment (degrees): ").strip()
                if angle_input:
                    try:
                        angle_increment = float(angle_input)
                        break
                    except ValueError:
                        print("Please enter a valid number. Try again.")
                        continue
                else:
                    print("Please enter an angle increment.")
                    continue
            
            config = LSystemConfig(
                axiom=axiom,
                rules=rules,
                iterations=iterations,
                segment_length=segment_length,
                initial_heading=initial_heading,
                angle_increment=angle_increment
            )
        except LSystemError as e:
            print(f"Error: {e}")
            return

    # Generate and plot the L-System
    try:
        final_sequence, coordinates = create_l_system(config)
        
        # Plot the L-System
        title = f"L-System: {config.axiom} ({config.iterations} iterations)"
        fig = plot_l_system(coordinates, title=title)
        plt.show()
        
        print(f"\nGenerated sequence length: {len(final_sequence)}")
        print(f"Number of coordinate points: {len(coordinates)}")
        
    except LSystemError as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
