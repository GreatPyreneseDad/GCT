# GitHub Models + Grok 3 for Grounded Coherence Theory

This integration leverages GitHub Models with Grok 3 to accelerate the implementation and validation of Grounded Coherence Theory (GCT).

## Overview

Grounded Coherence Theory provides a mathematical framework for measuring belief-action alignment:

```
C = Ψ + (ρ × Ψ) + q^optimal + (f × Ψ)
```

Where:
- **Ψ** (Psi): Internal consistency - correlation between stated beliefs and actions
- **ρ** (Rho): Network influence coefficient
- **q^optimal**: Biologically optimized action patterns
- **f**: Feedback loop strength
- **C**: Total coherence score

## Features

### 1. **GitHub Models Client** (`client/github_models_client.py`)
- Direct integration with Grok 3 via GitHub Models API
- Specialized GCT analysis methods
- Batch processing with rate limiting
- Coherence analysis from behavioral data

### 2. **Assessment Prompts** (`prompts/assessment_prompts.yaml`)
- Pre-configured prompts for all GCT components
- Cultural adaptation templates
- Scenario generation for different contexts
- Mathematical validation prompts

### 3. **Coherence Calculator** (`utils/coherence_calculator.py`)
- Implementation of GCT mathematical framework
- Biological optimization calculations (K_m=0.2, K_i=0.8)
- Coherence velocity (dC/dt) calculations
- Breakthrough moment identification
- Statistical analysis tools

### 4. **Examples** (`examples/quickstart.py`)
- Complete working examples
- Real-time monitoring simulation
- Scenario generation demonstrations
- Mathematical validation tests

## Quick Start

### 1. Set up your environment

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_github_pat_token"

# Install dependencies
pip install requests numpy pyyaml
```

### 2. Run the quickstart example

```bash
cd github_models_gct
python examples/quickstart.py
```

### 3. Basic usage

```python
from client.github_models_client import GCTAnalyzer
from utils.coherence_calculator import CoherenceCalculator

# Initialize analyzer
analyzer = GCTAnalyzer()

# Generate assessment scenarios
scenarios = analyzer.generate_assessment_scenarios(
    cultural_context="Western corporate environment",
    target_population="Senior executives",
    num_scenarios=5
)

# Calculate coherence
calculator = CoherenceCalculator()
coherence = calculator.calculate_coherence(
    psi=0.8,    # Internal consistency
    rho=0.3,    # Network influence
    q=0.7,      # Behavioral efficiency
    f=0.2       # Feedback strength
)
```

## Application Phases

### Phase 1-2: Foundation & Testing
- Generate culturally adapted assessment tools
- Validate mathematical models
- Test biological optimization parameters

### Phase 3: Application Development
- Leadership coherence assessment
- Team dynamics analysis
- Organizational coherence mapping

### Phase 4-5: Scale & Implementation
- Multi-site validation studies
- Real-time coherence monitoring
- Intervention effectiveness tracking

## API Integration

### Authentication

```python
# Option 1: Environment variable
export GITHUB_TOKEN="github_pat_..."

# Option 2: Direct initialization
analyzer = GCTAnalyzer(token="github_pat_...")
```

### Example API Call

```python
# Analyze coherence from behavioral data
result = analyzer.analyze_coherence(
    data={
        "beliefs": [0.9, 0.8, 0.85],
        "actions": [0.85, 0.75, 0.8],
        "network_ties": [0.7, 0.8, 0.75]
    },
    context="Leadership team assessment"
)
```

## Mathematical Framework

### Biological Optimization

The biological optimization curve models energy-efficient behavior:

```
q^optimal = (q_max × q) / (K_m + q + q²/K_i)
```

Where:
- K_m = 0.2 (cooperation threshold)
- K_i = 0.8 (competition threshold)

### Coherence Velocity

Track the rate of coherence change:

```
dC/dt = Ψ̇(1 + ρ + f) + ρ̇Ψ + dq*/dt + ḟΨ
```

## Best Practices

1. **Prompt Engineering**: Customize prompts in `assessment_prompts.yaml` for your specific context
2. **Rate Limiting**: Use batch processing with delays for large-scale analysis
3. **Data Export**: Save measurements for longitudinal analysis
4. **Cultural Validation**: Always validate assessments for cultural appropriateness

## Next Steps

1. Obtain GitHub token and configure environment
2. Customize assessment scenarios for your use case
3. Integrate with existing data collection systems
4. Deploy real-time monitoring infrastructure
5. Validate results against existing psychological scales

## Resources

- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- [Grok 3 on GitHub Models](https://github.com/marketplace/models/azureml-xai/grok-3)
- [Grounded Coherence Theory Paper](link-to-paper)

## License

This integration is designed for research and assessment purposes in accordance with GCT principles.