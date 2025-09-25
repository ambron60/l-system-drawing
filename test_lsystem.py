#!/usr/bin/env python3
"""
Unit tests for the L-System module.
Run with: python test_lsystem.py
"""

import unittest
from lsystem import (
    derivation,
    generate_coordinates,
    parse_rules_from_string,
    LSystemConfig,
    create_l_system,
    get_preset_config,
    list_presets,
    LSystemError,
    PRESET_L_SYSTEMS
)


class TestLSystemCore(unittest.TestCase):
    """Test core L-System functionality."""
    
    def test_derivation_basic(self):
        """Test basic derivation functionality."""
        rules = {"F": "F+F", "G": "GG"}
        result = derivation("F", 2, rules)
        self.assertEqual(result, "F+F+F+F")
    
    def test_derivation_empty_axiom(self):
        """Test derivation with empty axiom."""
        rules = {"F": "F+F"}
        with self.assertRaises(LSystemError):
            derivation("", 2, rules)
    
    def test_derivation_negative_steps(self):
        """Test derivation with negative steps."""
        rules = {"F": "F+F"}
        with self.assertRaises(LSystemError):
            derivation("F", -1, rules)
    
    def test_derivation_no_rules(self):
        """Test derivation without rules."""
        result = derivation("F", 2, {})
        self.assertEqual(result, "F")
    
    def test_generate_coordinates_basic(self):
        """Test basic coordinate generation."""
        sequence = "F+F-F"
        coords = generate_coordinates(sequence, 1, 0, 90)
        self.assertGreater(len(coords), 1)
        self.assertEqual(coords[0], (0, 0))  # Starting point
    
    def test_generate_coordinates_empty_sequence(self):
        """Test coordinate generation with empty sequence."""
        coords = generate_coordinates("", 1, 0, 90)
        self.assertEqual(len(coords), 1)
        self.assertEqual(coords[0], (0, 0))
    
    def test_generate_coordinates_invalid_segment_length(self):
        """Test coordinate generation with invalid segment length."""
        with self.assertRaises(LSystemError):
            generate_coordinates("F", 0, 0, 90)
    
    def test_generate_coordinates_brackets(self):
        """Test coordinate generation with bracket commands."""
        sequence = "F[+F]F"
        coords = generate_coordinates(sequence, 1, 0, 90)
        self.assertGreater(len(coords), 2)


class TestRuleParsing(unittest.TestCase):
    """Test rule parsing functionality."""
    
    def test_parse_rules_valid(self):
        """Test parsing valid rules."""
        rules_str = "F -> F+F\nG -> GG\n"
        rules = parse_rules_from_string(rules_str)
        expected = {"F": "F+F", "G": "GG"}
        self.assertEqual(rules, expected)
    
    def test_parse_rules_empty_lines(self):
        """Test parsing rules with empty lines."""
        rules_str = "F -> F+F\n\nG -> GG\n"
        rules = parse_rules_from_string(rules_str)
        expected = {"F": "F+F", "G": "GG"}
        self.assertEqual(rules, expected)
    
    def test_parse_rules_comments(self):
        """Test parsing rules with comments."""
        rules_str = "# This is a comment\nF -> F+F\nG -> GG"
        rules = parse_rules_from_string(rules_str)
        expected = {"F": "F+F", "G": "GG"}
        self.assertEqual(rules, expected)
    
    def test_parse_rules_invalid_format(self):
        """Test parsing invalid rule format."""
        rules_str = "F -> F+F\nInvalid rule\nG -> GG"
        with self.assertRaises(LSystemError):
            parse_rules_from_string(rules_str)
    
    def test_parse_rules_empty_symbol(self):
        """Test parsing rules with empty symbol."""
        rules_str = " -> F+F"
        with self.assertRaises(LSystemError):
            parse_rules_from_string(rules_str)


class TestLSystemConfig(unittest.TestCase):
    """Test LSystemConfig functionality."""
    
    def test_config_valid(self):
        """Test creating valid config."""
        config = LSystemConfig(
            axiom="F",
            rules={"F": "F+F"},
            iterations=2,
            segment_length=1.0,
            initial_heading=0.0,
            angle_increment=90.0
        )
        self.assertEqual(config.axiom, "F")
        self.assertEqual(config.iterations, 2)
    
    def test_config_invalid_iterations(self):
        """Test config with invalid iterations."""
        with self.assertRaises(ValueError):
            LSystemConfig(
                axiom="F",
                rules={"F": "F+F"},
                iterations=-1,
                segment_length=1.0,
                initial_heading=0.0,
                angle_increment=90.0
            )
    
    def test_config_invalid_segment_length(self):
        """Test config with invalid segment length."""
        with self.assertRaises(ValueError):
            LSystemConfig(
                axiom="F",
                rules={"F": "F+F"},
                iterations=2,
                segment_length=0,
                initial_heading=0.0,
                angle_increment=90.0
            )
    
    def test_config_empty_axiom(self):
        """Test config with empty axiom."""
        with self.assertRaises(ValueError):
            LSystemConfig(
                axiom="",
                rules={"F": "F+F"},
                iterations=2,
                segment_length=1.0,
                initial_heading=0.0,
                angle_increment=90.0
            )


class TestPresetSystems(unittest.TestCase):
    """Test preset L-System functionality."""
    
    def test_list_presets(self):
        """Test listing available presets."""
        presets = list_presets()
        self.assertIsInstance(presets, list)
        self.assertGreater(len(presets), 0)
        self.assertIn("koch_curve", presets)
    
    def test_get_preset_valid(self):
        """Test getting valid preset."""
        config = get_preset_config("koch_curve")
        self.assertIsInstance(config, LSystemConfig)
        self.assertEqual(config.axiom, "F")
    
    def test_get_preset_invalid(self):
        """Test getting invalid preset."""
        with self.assertRaises(LSystemError):
            get_preset_config("nonexistent_preset")


class TestCreateLSystem(unittest.TestCase):
    """Test complete L-System creation."""
    
    def test_create_l_system_basic(self):
        """Test creating a basic L-System."""
        config = LSystemConfig(
            axiom="F",
            rules={"F": "F+F"},
            iterations=2,
            segment_length=1.0,
            initial_heading=0.0,
            angle_increment=90.0
        )
        
        sequence, coords = create_l_system(config)
        self.assertIsInstance(sequence, str)
        self.assertIsInstance(coords, list)
        self.assertGreater(len(sequence), 0)
        self.assertGreater(len(coords), 0)
    
    def test_create_l_system_complex(self):
        """Test creating a complex L-System using preset."""
        config = get_preset_config("koch_curve")
        sequence, coords = create_l_system(config)
        
        self.assertGreater(len(sequence), len(config.axiom))
        self.assertGreater(len(coords), 1)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_derivation_large_sequence(self):
        """Test derivation with potentially large sequence."""
        # This should not crash but might truncate
        rules = {"F": "F+F"}
        result = derivation("F", 20, rules)
        self.assertIsInstance(result, str)
    
    def test_coordinate_generation_unmatched_brackets(self):
        """Test coordinate generation with unmatched brackets."""
        sequence = "F[+F"  # Missing closing bracket
        coords = generate_coordinates(sequence, 1, 0, 90)
        self.assertGreater(len(coords), 0)  # Should still work
    
    def test_coordinate_generation_extra_closing_brackets(self):
        """Test coordinate generation with extra closing brackets."""
        sequence = "F+F]"  # Extra closing bracket
        coords = generate_coordinates(sequence, 1, 0, 90)
        self.assertGreater(len(coords), 0)  # Should still work


def run_tests():
    """Run all tests and display results."""
    print("Running L-System Tests...")
    print("=" * 40)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestLSystemCore,
        TestRuleParsing,
        TestLSystemConfig,
        TestPresetSystems,
        TestCreateLSystem,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Summary
    print("\n" + "=" * 40)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
