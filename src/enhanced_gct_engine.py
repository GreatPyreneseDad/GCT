"""
Enhanced GCT Engine with Token-Based Derivatives
===============================================

Extends the core GCT engine with information-theoretic derivatives
based on the insight: Time = Token Flow Rate

This enhanced engine tracks coherence changes per unit of information
exchange, providing more meaningful dynamics for conversational AI.

Author: Christopher MacGregor bin Joseph
Date: October 2025
"""

import numpy as np
from typing import Dict, Tuple, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import time


@dataclass
class TokenAwareGCTVariables:
    """Extended GCT variables with token information"""
    psi: float  # Clarity/precision of narrative
    rho: float  # Reflective depth/nuance
    q_raw: float  # Emotional charge (raw)
    f: float  # Social belonging signal
    timestamp: datetime
    token_count: int  # Number of tokens in the text
    message_text: str  # Original text for reference
    speaker: str  # 'user' or 'system'


@dataclass
class EnhancedGCTResult:
    """Extended GCT results with token derivatives"""
    coherence: float
    q_opt: float  # Optimized emotional charge
    dc_dt: float  # Traditional time derivative
    d2c_dt2: float  # Traditional second derivative
    dc_dtokens: float  # Token-based derivative
    d2c_dtokens2: float  # Token-based second derivative
    flow_rate: float  # Tokens per second
    sentiment: str  # bullish/bearish/neutral
    dynamics_interpretation: str  # Semantic interpretation
    components: Dict[str, float]


class EnhancedGCTEngine:
    """Extended GCT engine with token-based analysis"""
    
    def __init__(self, km: float = 0.3, ki: float = 0.1, coupling_strength: float = 0.15):
        """
        Initialize enhanced GCT engine
        
        Args:
            km: Saturation constant for wisdom
            ki: Inhibition constant for wisdom
            coupling_strength: Coupling between components
        """
        self.km = km
        self.ki = ki
        self.coupling_strength = coupling_strength
        
        # Extended history tracking
        self.coherence_history: List[float] = []
        self.token_history: List[int] = []  # Cumulative tokens
        self.timestamp_history: List[float] = []
        self.message_history: List[TokenAwareGCTVariables] = []
        
        # Flow rate thresholds
        self.flow_thresholds = {
            'crisis': 100,      # tokens/second
            'high': 80,
            'standard': 40,
            'contemplative': 30,
            'slow': 15
        }
        
        # Derivative thresholds for interpretation
        self.derivative_thresholds = {
            'positive_surge': 0.001,
            'positive': 0.0005,
            'neutral': 0.0001,
            'negative': -0.0005,
            'negative_plunge': -0.001
        }
    
    def compute_coherence(self, variables: TokenAwareGCTVariables) -> Tuple[float, float]:
        """
        Compute GCT coherence score (same as base engine)
        
        Returns:
            coherence: Overall coherence score
            q_opt: Optimized emotional charge
        """
        # Validate inputs
        if self.ki == 0:
            raise ValueError("ki parameter cannot be zero")
        if variables.q_raw < 0:
            raise ValueError("q_raw must be non-negative")
            
        # Optimize emotional charge with wisdom modulation
        denominator = self.km + variables.q_raw + (variables.q_raw**2) / self.ki
        if denominator == 0:
            raise ValueError("Denominator in q_opt calculation cannot be zero")
            
        q_opt = variables.q_raw / denominator
        
        # Component contributions
        base = variables.psi
        wisdom_amp = variables.rho * variables.psi
        social_amp = variables.f * variables.psi
        coupling = self.coupling_strength * variables.rho * q_opt
        
        # Total coherence
        coherence = base + wisdom_amp + q_opt + social_amp + coupling
        
        return coherence, q_opt
    
    def update_history(self, variables: TokenAwareGCTVariables, coherence: float):
        """Update all history tracking"""
        # Add to message history
        self.message_history.append(variables)
        
        # Update coherence history
        self.coherence_history.append(coherence)
        
        # Calculate cumulative tokens
        if self.token_history:
            cumulative_tokens = self.token_history[-1] + variables.token_count
        else:
            cumulative_tokens = variables.token_count
        self.token_history.append(cumulative_tokens)
        
        # Update timestamp history
        self.timestamp_history.append(variables.timestamp.timestamp())
        
        # Keep history manageable (last 100 points)
        if len(self.coherence_history) > 100:
            self.coherence_history.pop(0)
            self.token_history.pop(0)
            self.timestamp_history.pop(0)
            self.message_history.pop(0)
    
    def calculate_token_derivatives(self) -> Tuple[float, float]:
        """
        Calculate token-based derivatives
        
        Returns:
            dc_dtokens: First derivative wrt tokens
            d2c_dtokens2: Second derivative wrt tokens
        """
        if len(self.coherence_history) < 2:
            return 0.0, 0.0
        
        # First derivative
        dC = self.coherence_history[-1] - self.coherence_history[-2]
        d_tokens = self.token_history[-1] - self.token_history[-2]
        
        if d_tokens == 0:
            dc_dtokens = 0.0
        else:
            dc_dtokens = dC / d_tokens
        
        # Second derivative
        if len(self.coherence_history) < 3:
            d2c_dtokens2 = 0.0
        else:
            # Calculate two consecutive first derivatives
            dC1 = self.coherence_history[-2] - self.coherence_history[-3]
            d_tokens1 = self.token_history[-2] - self.token_history[-3]
            
            if d_tokens1 == 0:
                dc_dtokens1 = 0.0
            else:
                dc_dtokens1 = dC1 / d_tokens1
            
            # Second derivative
            if d_tokens == 0:
                d2c_dtokens2 = 0.0
            else:
                d2c_dtokens2 = (dc_dtokens - dc_dtokens1) / d_tokens
        
        return dc_dtokens, d2c_dtokens2
    
    def calculate_time_derivatives(self) -> Tuple[float, float]:
        """
        Calculate traditional time-based derivatives
        
        Returns:
            dc_dt: First time derivative
            d2c_dt2: Second time derivative
        """
        if len(self.timestamp_history) < 2:
            return 0.0, 0.0
        
        # Convert to numpy arrays for gradient calculation
        times = np.array(self.timestamp_history)
        values = np.array(self.coherence_history)
        
        # First derivative
        if len(times) >= 2:
            dc_dt = np.gradient(values, times)[-1]
        else:
            dc_dt = 0.0
        
        # Second derivative
        if len(times) >= 3:
            first_derivatives = np.gradient(values, times)
            d2c_dt2 = np.gradient(first_derivatives, times)[-1]
        else:
            d2c_dt2 = 0.0
        
        return dc_dt, d2c_dt2
    
    def calculate_flow_rate(self) -> float:
        """
        Calculate current token flow rate (tokens/second)
        
        Returns:
            Current flow rate
        """
        if len(self.timestamp_history) < 2:
            return 0.0
        
        # Use recent window for flow rate
        window_size = min(5, len(self.timestamp_history))
        window_start = len(self.timestamp_history) - window_size
        
        dt = self.timestamp_history[-1] - self.timestamp_history[window_start]
        d_tokens = self.token_history[-1] - self.token_history[window_start]
        
        if dt == 0:
            return float('inf')
        
        return d_tokens / dt
    
    def interpret_dynamics(self, 
                          dc_dtokens: float, 
                          flow_rate: float,
                          coherence: float) -> str:
        """
        Interpret the conversation dynamics based on derivatives and flow
        
        Args:
            dc_dtokens: Token-based derivative
            flow_rate: Current token flow rate
            coherence: Current coherence value
            
        Returns:
            Semantic interpretation
        """
        # Crisis patterns
        if coherence < 1.0 and flow_rate > self.flow_thresholds['crisis']:
            return "crisis_spiral_detected"
        
        # High flow patterns
        if flow_rate > self.flow_thresholds['high']:
            if dc_dtokens > self.derivative_thresholds['positive']:
                return "high_energy_convergence"
            elif dc_dtokens < self.derivative_thresholds['negative']:
                return "rapid_deterioration"
            else:
                return "high_energy_neutral"
        
        # Contemplative patterns
        elif flow_rate < self.flow_thresholds['contemplative']:
            if dc_dtokens > self.derivative_thresholds['positive']:
                return "contemplative_growth"
            elif dc_dtokens < self.derivative_thresholds['negative']:
                return "slow_disengagement"
            else:
                return "quiet_stability"
        
        # Standard flow patterns
        else:
            if dc_dtokens > self.derivative_thresholds['positive_surge']:
                return "breakthrough_moment"
            elif dc_dtokens > self.derivative_thresholds['positive']:
                return "steady_improvement"
            elif dc_dtokens < self.derivative_thresholds['negative_plunge']:
                return "coherence_collapse"
            elif dc_dtokens < self.derivative_thresholds['negative']:
                return "gradual_decline"
            else:
                return "stable_dialogue"
    
    def analyze_enhanced(self, variables: TokenAwareGCTVariables) -> EnhancedGCTResult:
        """
        Complete enhanced GCT analysis with token derivatives
        
        Args:
            variables: Token-aware GCT variables
            
        Returns:
            Enhanced GCT result with dual derivatives
        """
        # Compute base coherence
        coherence, q_opt = self.compute_coherence(variables)
        
        # Update history
        self.update_history(variables, coherence)
        
        # Calculate derivatives
        dc_dt, d2c_dt2 = self.calculate_time_derivatives()
        dc_dtokens, d2c_dtokens2 = self.calculate_token_derivatives()
        
        # Calculate flow rate
        flow_rate = self.calculate_flow_rate()
        
        # Interpret dynamics
        interpretation = self.interpret_dynamics(dc_dtokens, flow_rate, coherence)
        
        # Classify sentiment (using time derivative for compatibility)
        if dc_dt > 0.05:
            sentiment = "bullish"
        elif dc_dt < -0.05:
            sentiment = "bearish"
        else:
            sentiment = "neutral"
        
        # Component breakdown
        components = {
            "base": variables.psi,
            "wisdom_amp": variables.rho * variables.psi,
            "emotional": q_opt,
            "social_amp": variables.f * variables.psi,
            "coupling": self.coupling_strength * variables.rho * q_opt,
        }
        
        return EnhancedGCTResult(
            coherence=coherence,
            q_opt=q_opt,
            dc_dt=dc_dt,
            d2c_dt2=d2c_dt2,
            dc_dtokens=dc_dtokens,
            d2c_dtokens2=d2c_dtokens2,
            flow_rate=flow_rate,
            sentiment=sentiment,
            dynamics_interpretation=interpretation,
            components=components
        )
    
    def get_conversation_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive conversation metrics
        
        Returns:
            Dictionary of conversation analytics
        """
        if len(self.message_history) < 2:
            return {
                'message': 'Insufficient data for metrics',
                'message_count': len(self.message_history)
            }
        
        # Basic metrics
        total_tokens = self.token_history[-1] if self.token_history else 0
        duration = self.timestamp_history[-1] - self.timestamp_history[0]
        avg_flow_rate = total_tokens / duration if duration > 0 else 0
        
        # Speaker analysis
        user_messages = sum(1 for m in self.message_history if m.speaker == 'user')
        system_messages = len(self.message_history) - user_messages
        
        # Coherence trajectory
        coherence_values = self.coherence_history
        coherence_trend = 'improving' if coherence_values[-1] > coherence_values[0] else 'declining'
        
        # Flow rate variations
        flow_rates = []
        for i in range(1, len(self.timestamp_history)):
            dt = self.timestamp_history[i] - self.timestamp_history[i-1]
            tokens = self.token_history[i] - self.token_history[i-1]
            if dt > 0:
                flow_rates.append(tokens / dt)
        
        flow_variance = np.var(flow_rates) if flow_rates else 0
        
        # Crisis detection
        crisis_moments = sum(1 for c in coherence_values if c < 1.0)
        high_coherence_moments = sum(1 for c in coherence_values if c > 2.5)
        
        return {
            'total_messages': len(self.message_history),
            'total_tokens': total_tokens,
            'duration_seconds': duration,
            'average_flow_rate': avg_flow_rate,
            'flow_variance': flow_variance,
            'user_messages': user_messages,
            'system_messages': system_messages,
            'turn_ratio': user_messages / len(self.message_history),
            'coherence_trajectory': {
                'start': coherence_values[0],
                'end': coherence_values[-1],
                'average': np.mean(coherence_values),
                'std': np.std(coherence_values),
                'trend': coherence_trend
            },
            'crisis_moments': crisis_moments,
            'high_coherence_moments': high_coherence_moments,
            'current_interpretation': self.interpret_dynamics(
                self.calculate_token_derivatives()[0],
                self.calculate_flow_rate(),
                coherence_values[-1]
            )
        }
    
    def recommend_intervention(self, result: EnhancedGCTResult) -> Dict[str, Any]:
        """
        Recommend intervention based on current dynamics
        
        Args:
            result: Enhanced GCT analysis result
            
        Returns:
            Intervention recommendations
        """
        recommendations = {
            'intervention_needed': False,
            'urgency': 'none',
            'actions': [],
            'reasoning': []
        }
        
        # Crisis intervention
        if result.dynamics_interpretation in ['crisis_spiral_detected', 'rapid_deterioration']:
            recommendations['intervention_needed'] = True
            recommendations['urgency'] = 'high'
            recommendations['actions'].extend([
                'Immediately slow response pace',
                'Use grounding language',
                'Validate emotional state',
                'Simplify communication'
            ])
            recommendations['reasoning'].append(
                f"Crisis pattern detected: {result.dynamics_interpretation}"
            )
        
        # Coherence collapse
        elif result.dynamics_interpretation == 'coherence_collapse':
            recommendations['intervention_needed'] = True
            recommendations['urgency'] = 'medium'
            recommendations['actions'].extend([
                'Pause and check understanding',
                'Clarify recent points',
                'Reduce complexity'
            ])
            recommendations['reasoning'].append("Sudden coherence drop detected")
        
        # Disengagement
        elif result.dynamics_interpretation in ['slow_disengagement', 'gradual_decline']:
            recommendations['intervention_needed'] = True
            recommendations['urgency'] = 'low'
            recommendations['actions'].extend([
                'Re-engage with open questions',
                'Shift perspective or topic',
                'Increase energy level'
            ])
            recommendations['reasoning'].append("Disengagement pattern emerging")
        
        # Positive patterns - enhance them
        elif result.dynamics_interpretation in ['high_energy_convergence', 
                                               'contemplative_growth',
                                               'breakthrough_moment']:
            recommendations['actions'].extend([
                'Maintain current approach',
                'Deepen exploration',
                'Follow their lead'
            ])
            recommendations['reasoning'].append(
                f"Positive pattern: {result.dynamics_interpretation}"
            )
        
        # Flow rate adjustments
        if result.flow_rate > 100:
            recommendations['actions'].append("Consider slowing pace")
            recommendations['reasoning'].append("Very high token flow rate")
        elif result.flow_rate < 20:
            recommendations['actions'].append("Consider increasing engagement")
            recommendations['reasoning'].append("Very low token flow rate")
        
        return recommendations
    
    def reset(self):
        """Reset all history tracking"""
        self.coherence_history = []
        self.token_history = []
        self.timestamp_history = []
        self.message_history = []
"""