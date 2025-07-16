"""
Quickstart example for GitHub Models GCT integration
Demonstrates basic usage of the GCT analysis tools with Grok 3
"""

import os
import sys
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.github_models_client import GCTAnalyzer
from utils.coherence_calculator import CoherenceCalculator


def example_coherence_analysis():
    """Example: Analyze coherence from behavioral data"""
    print("=== Coherence Analysis Example ===\n")
    
    # Initialize calculator
    calculator = CoherenceCalculator()
    
    # Example behavioral data
    # Simulating belief-action measurements over time
    belief_action_pairs = [
        {"beliefs": [0.9, 0.8, 0.85, 0.7, 0.9], "actions": [0.85, 0.75, 0.8, 0.6, 0.88]},
        {"beliefs": [0.85, 0.9, 0.8, 0.75, 0.85], "actions": [0.8, 0.88, 0.82, 0.7, 0.83]},
        {"beliefs": [0.9, 0.85, 0.88, 0.8, 0.9], "actions": [0.88, 0.86, 0.9, 0.82, 0.91]}
    ]
    
    # Network data (example neighbor coherences)
    network_data = [
        {"neighbors": [0.7, 0.75, 0.8], "tie_strengths": [0.8, 0.6, 0.9]},
        {"neighbors": [0.75, 0.8, 0.82], "tie_strengths": [0.7, 0.8, 0.85]},
        {"neighbors": [0.8, 0.85, 0.88], "tie_strengths": [0.75, 0.85, 0.9]}
    ]
    
    # Calculate coherence over time
    timestamps = []
    for i, (ba_data, net_data) in enumerate(zip(belief_action_pairs, network_data)):
        # Calculate Ψ (internal consistency)
        psi = calculator.calculate_psi_from_beliefs_actions(
            ba_data["beliefs"], 
            ba_data["actions"]
        )
        
        # Calculate ρ (network influence)
        current_coherence = 0.7 + i * 0.05  # Simulated improvement
        rho = calculator.calculate_rho_from_network(
            current_coherence,
            net_data["neighbors"],
            net_data["tie_strengths"]
        )
        
        # Calculate feedback strength
        coherence_history = [0.6, 0.65, 0.7, 0.72, 0.75 + i * 0.05]
        f = calculator.calculate_feedback_strength(coherence_history)
        
        # Raw behavioral efficiency (example)
        q = 0.6 + i * 0.1
        
        # Add measurement
        timestamp = time.time() + i * 86400  # Daily measurements
        measurement = calculator.add_measurement(
            timestamp=timestamp,
            psi=psi,
            rho=rho,
            q=q,
            f=f,
            metadata={"day": i+1, "context": "leadership_training"}
        )
        
        print(f"Day {i+1} Measurement:")
        print(f"  Ψ (Internal Consistency): {psi:.3f}")
        print(f"  ρ (Network Influence): {rho:.3f}")
        print(f"  q* (Biological Optimization): {measurement.q_optimal:.3f}")
        print(f"  f (Feedback Strength): {f:.3f}")
        print(f"  C (Total Coherence): {measurement.coherence:.3f}\n")
    
    # Calculate statistics
    stats = calculator.get_statistics()
    print("Summary Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value:.3f}")
    
    # Identify breakthroughs
    breakthroughs = calculator.identify_breakthrough_moments(
        calculator.measurements, 
        threshold=0.3
    )
    if breakthroughs:
        print("\nBreakthrough Moments:")
        for idx, velocity in breakthroughs:
            print(f"  Day {idx}: Velocity = {velocity:.3f}")
    
    # Export data
    calculator.export_measurements("coherence_data.json")
    print("\nData exported to coherence_data.json")


def example_scenario_generation():
    """Example: Generate assessment scenarios using Grok 3"""
    print("\n\n=== Scenario Generation Example ===\n")
    
    # Check for GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Note: Set GITHUB_TOKEN environment variable to use Grok 3 features")
        print("Example scenarios would be generated here...")
        return
    
    try:
        # Initialize GCT Analyzer
        analyzer = GCTAnalyzer(token)
        
        # Generate scenarios for different contexts
        contexts = [
            {
                "cultural_context": "Silicon Valley startup culture",
                "target_population": "Software engineers and product managers"
            },
            {
                "cultural_context": "Japanese corporate environment",
                "target_population": "Middle management in traditional companies"
            }
        ]
        
        for context in contexts:
            print(f"\nGenerating scenarios for: {context['cultural_context']}")
            print(f"Target: {context['target_population']}")
            
            scenarios = analyzer.generate_assessment_scenarios(
                cultural_context=context["cultural_context"],
                target_population=context["target_population"],
                num_scenarios=3
            )
            
            # In real implementation, this would return structured scenarios
            print("Scenarios generated successfully!")
            
    except Exception as e:
        print(f"API call skipped: {str(e)}")
        print("This is expected if running without API access")


def example_mathematical_validation():
    """Example: Validate GCT mathematical models"""
    print("\n\n=== Mathematical Validation Example ===\n")
    
    # Example equation validation
    equation = "C = Ψ + (ρ × Ψ) + q^optimal + (f × Ψ)"
    parameters = {
        "K_m": 0.2,
        "K_i": 0.8,
        "q_max": 1.0,
        "typical_psi_range": [0.0, 1.0],
        "typical_rho_range": [0.0, 0.5],
        "typical_f_range": [0.0, 0.3]
    }
    
    print(f"Validating equation: {equation}")
    print(f"Parameters: {parameters}")
    
    # Local validation (without API)
    calculator = CoherenceCalculator()
    
    # Test boundary conditions
    print("\nBoundary Condition Tests:")
    
    test_cases = [
        {"psi": 0, "rho": 0, "q": 0, "f": 0, "label": "All zeros"},
        {"psi": 1, "rho": 0.5, "q": 1, "f": 0.3, "label": "Maximum values"},
        {"psi": 0.5, "rho": 0.25, "q": 0.5, "f": 0.1, "label": "Typical values"}
    ]
    
    for test in test_cases:
        coherence = calculator.calculate_coherence(
            test["psi"], test["rho"], test["q"], test["f"]
        )
        print(f"  {test['label']}: C = {coherence:.3f}")
    
    # Test biological optimization curve
    print("\nBiological Optimization Curve:")
    q_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    for q in q_values:
        q_optimal = calculator.calculate_q_optimal(q)
        print(f"  q = {q:.1f} → q* = {q_optimal:.3f}")


def example_real_time_monitoring():
    """Example: Real-time coherence monitoring simulation"""
    print("\n\n=== Real-Time Monitoring Example ===\n")
    
    calculator = CoherenceCalculator()
    
    print("Simulating real-time coherence monitoring...")
    print("Press Ctrl+C to stop\n")
    
    # Simulate 10 time steps
    for t in range(10):
        # Simulate varying measurements
        import random
        
        psi = 0.7 + random.uniform(-0.1, 0.1)
        rho = 0.3 + random.uniform(-0.05, 0.05)
        q = 0.6 + t * 0.03 + random.uniform(-0.05, 0.05)
        f = 0.1 + t * 0.02
        
        measurement = calculator.add_measurement(
            timestamp=time.time(),
            psi=psi,
            rho=rho,
            q=q,
            f=f,
            metadata={"iteration": t}
        )
        
        print(f"Time {t}: C = {measurement.coherence:.3f} "
              f"(Ψ={psi:.2f}, ρ={rho:.2f}, q*={measurement.q_optimal:.2f}, f={f:.2f})")
        
        # Check for breakthroughs
        if len(calculator.measurements) > 1:
            velocities = calculator.calculate_coherence_velocity(
                calculator.measurements[-2:]
            )
            if velocities and velocities[0] > 0.5:
                print("  ⚡ Breakthrough detected!")
        
        time.sleep(0.5)  # Simulate real-time delay


if __name__ == "__main__":
    print("GitHub Models + Grok 3 for Grounded Coherence Theory")
    print("=" * 50)
    
    # Run examples
    example_coherence_analysis()
    example_scenario_generation()
    example_mathematical_validation()
    example_real_time_monitoring()
    
    print("\n\nQuickstart complete!")
    print("\nNext steps:")
    print("1. Set GITHUB_TOKEN environment variable for API access")
    print("2. Customize assessment scenarios in prompts/assessment_prompts.yaml")
    print("3. Integrate with your data collection systems")
    print("4. Deploy real-time monitoring for your use case")