"""
GitHub Models API Client for Grounded Coherence Theory
Integrates with Grok 3 for GCT assessment and analysis
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time


@dataclass
class ModelResponse:
    """Response from GitHub Models API"""
    content: str
    model: str
    usage: Dict[str, int]
    created: int
    choices: List[Dict[str, Any]]


class GitHubModelsClient:
    """Client for interacting with GitHub Models API"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub Models client
        
        Args:
            token: GitHub PAT token. If not provided, will look for GITHUB_TOKEN env var
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN env var or pass token parameter")
        
        self.base_url = "https://models.github.com/v1"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-3",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ModelResponse:
        """
        Send chat completion request to GitHub Models
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (default: grok-3)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            ModelResponse object
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            return ModelResponse(
                content=data['choices'][0]['message']['content'],
                model=data['model'],
                usage=data.get('usage', {}),
                created=data['created'],
                choices=data['choices']
            )
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def query_grok3(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Simplified method to query Grok 3
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response content as string
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.chat_completion(
            messages=messages,
            model="grok-3",
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.content
    
    def batch_analyze(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        delay_seconds: float = 0.5
    ) -> List[str]:
        """
        Analyze multiple prompts with rate limiting
        
        Args:
            prompts: List of prompts to analyze
            system_prompt: Optional system prompt
            delay_seconds: Delay between requests
            
        Returns:
            List of response contents
        """
        results = []
        
        for prompt in prompts:
            result = self.query_grok3(prompt, system_prompt)
            results.append(result)
            
            # Rate limiting
            if delay_seconds > 0:
                time.sleep(delay_seconds)
        
        return results


class GCTAnalyzer(GitHubModelsClient):
    """Specialized client for GCT-specific analysis"""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__(token)
        self.gct_system_prompt = """You are an expert in Grounded Coherence Theory (GCT), 
        a mathematical framework for measuring belief-action alignment. You understand:
        - Internal consistency (Ψ): Correlation between stated beliefs and actions
        - Network influence (ρ): Social contagion effects
        - Biological optimization (q*): Energy-optimized action patterns
        - Feedback loops (f): Self-reinforcing coherence mechanisms
        
        The core equation is: C = Ψ + (ρ × Ψ) + q^optimal + (f × Ψ)
        Where q^optimal = (q_max × q) / (K_m + q + q²/K_i)
        With biological parameters: K_m = 0.2, K_i = 0.8
        """
    
    def analyze_coherence(
        self,
        data: Dict[str, Any],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze coherence metrics from behavioral data
        
        Args:
            data: Dictionary containing behavioral measurements
            context: Optional context about the measurement
            
        Returns:
            Dictionary with coherence analysis
        """
        prompt = f"""Analyze the following behavioral data for coherence metrics:

Data: {json.dumps(data, indent=2)}
Context: {context or 'General assessment'}

Calculate and provide:
1. Internal consistency (Ψ) score (0-1)
2. Network influence (ρ) estimate
3. Biological optimization (q*) using the given parameters
4. Feedback strength (f)
5. Total coherence (C) score
6. Coherence velocity (dC/dt) if historical data available
7. Key insights and recommendations

Provide calculations and reasoning for each component."""

        result = self.query_grok3(prompt, self.gct_system_prompt)
        
        # Parse the response to extract numerical values
        # In production, use more sophisticated parsing
        return {
            "raw_analysis": result,
            "timestamp": time.time(),
            "context": context,
            "data": data
        }
    
    def generate_assessment_scenarios(
        self,
        cultural_context: str,
        target_population: str,
        num_scenarios: int = 5
    ) -> List[Dict[str, str]]:
        """
        Generate culturally appropriate assessment scenarios
        
        Args:
            cultural_context: Cultural setting for scenarios
            target_population: Description of target population
            num_scenarios: Number of scenarios to generate
            
        Returns:
            List of scenario dictionaries
        """
        prompt = f"""Generate {num_scenarios} moral decision scenarios for measuring 
internal consistency (Ψ) in Grounded Coherence Theory.

Cultural Context: {cultural_context}
Target Population: {target_population}

Each scenario should:
1. Present a clear moral choice between stated values and expedient action
2. Allow measurement of belief-behavior correlation
3. Be culturally appropriate and realistic
4. Include measurable outcomes
5. Vary in domain (personal, professional, social)

Format each scenario as:
- Title: Brief descriptive title
- Setup: Context and background
- Dilemma: The moral choice to be made
- Belief Indicator: What belief would be measured
- Action Options: 2-3 possible actions with coherence implications
- Measurement: How to assess the choice made"""

        result = self.query_grok3(prompt, self.gct_system_prompt)
        
        # In production, parse this into structured scenario objects
        return [{"scenario": result, "generated_at": time.time()}]
    
    def validate_mathematical_model(
        self,
        equation: str,
        parameters: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Validate GCT mathematical formulations
        
        Args:
            equation: Mathematical equation to validate
            parameters: Parameter values
            
        Returns:
            Validation results
        """
        prompt = f"""Validate the following GCT mathematical formulation:

Equation: {equation}
Parameters: {json.dumps(parameters, indent=2)}

Perform:
1. Dimensional analysis
2. Boundary condition testing
3. Stability analysis
4. Parameter sensitivity analysis
5. Biological plausibility check

Provide detailed mathematical reasoning and any concerns."""

        result = self.query_grok3(prompt, self.gct_system_prompt)
        
        return {
            "validation": result,
            "equation": equation,
            "parameters": parameters,
            "timestamp": time.time()
        }