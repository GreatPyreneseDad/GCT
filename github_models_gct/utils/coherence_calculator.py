"""
Coherence calculation utilities for Grounded Coherence Theory
Implements the mathematical framework for GCT measurements
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class CoherenceMeasurement:
    """Single coherence measurement with all components"""
    timestamp: float
    psi: float  # Internal consistency (0-1)
    rho: float  # Network influence coefficient
    q_optimal: float  # Biological optimization
    f: float  # Feedback strength
    coherence: float  # Total coherence C
    metadata: Dict[str, any] = None


class CoherenceCalculator:
    """Calculate coherence metrics according to GCT framework"""
    
    # Biological optimization parameters
    K_M = 0.2  # Cooperation threshold
    K_I = 0.8  # Competition threshold
    
    def __init__(self, q_max: float = 1.0):
        """
        Initialize coherence calculator
        
        Args:
            q_max: Maximum behavioral efficiency (default 1.0)
        """
        self.q_max = q_max
        self.measurements: List[CoherenceMeasurement] = []
    
    def calculate_q_optimal(self, q: float) -> float:
        """
        Calculate biologically optimized action patterns
        
        Uses the biological optimization curve:
        q^optimal = (q_max × q) / (K_m + q + q²/K_i)
        
        Args:
            q: Raw behavioral efficiency (0-1)
            
        Returns:
            Optimized q value
        """
        if q < 0 or q > 1:
            raise ValueError("q must be between 0 and 1")
        
        numerator = self.q_max * q
        denominator = self.K_M + q + (q**2 / self.K_I)
        
        return numerator / denominator
    
    def calculate_coherence(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> float:
        """
        Calculate total coherence using GCT equation
        
        C = Ψ + (ρ × Ψ) + q^optimal + (f × Ψ)
        
        Args:
            psi: Internal consistency (0-1)
            rho: Network influence coefficient
            q: Raw behavioral efficiency (0-1)
            f: Feedback strength
            
        Returns:
            Total coherence score
        """
        # Validate inputs
        if not 0 <= psi <= 1:
            raise ValueError("Ψ must be between 0 and 1")
        if not 0 <= q <= 1:
            raise ValueError("q must be between 0 and 1")
        
        q_optimal = self.calculate_q_optimal(q)
        
        # Apply GCT equation
        coherence = psi + (rho * psi) + q_optimal + (f * psi)
        
        return coherence
    
    def calculate_psi_from_beliefs_actions(
        self,
        beliefs: List[float],
        actions: List[float]
    ) -> float:
        """
        Calculate internal consistency from belief-action pairs
        
        Args:
            beliefs: List of belief strength scores (0-1)
            actions: List of corresponding action alignment scores (0-1)
            
        Returns:
            Ψ score (correlation coefficient)
        """
        if len(beliefs) != len(actions):
            raise ValueError("Beliefs and actions must have same length")
        
        if len(beliefs) < 2:
            raise ValueError("Need at least 2 measurements")
        
        # Calculate Pearson correlation
        correlation = np.corrcoef(beliefs, actions)[0, 1]
        
        # Transform to 0-1 scale (correlation is -1 to 1)
        psi = (correlation + 1) / 2
        
        return psi
    
    def calculate_rho_from_network(
        self,
        individual_coherence: float,
        neighbor_coherences: List[float],
        tie_strengths: Optional[List[float]] = None
    ) -> float:
        """
        Calculate network influence coefficient
        
        Args:
            individual_coherence: Individual's coherence score
            neighbor_coherences: Coherence scores of network neighbors
            tie_strengths: Optional weights for each neighbor (0-1)
            
        Returns:
            ρ value (network influence coefficient)
        """
        if not neighbor_coherences:
            return 0.0
        
        if tie_strengths is None:
            tie_strengths = [1.0] * len(neighbor_coherences)
        
        if len(tie_strengths) != len(neighbor_coherences):
            raise ValueError("Tie strengths must match neighbor count")
        
        # Calculate weighted average neighbor coherence
        weighted_sum = sum(c * w for c, w in zip(neighbor_coherences, tie_strengths))
        weight_total = sum(tie_strengths)
        
        if weight_total == 0:
            return 0.0
        
        avg_neighbor_coherence = weighted_sum / weight_total
        
        # Calculate influence based on coherence differential
        # High coherence individuals resist negative influence
        if individual_coherence > avg_neighbor_coherence:
            # Resistance to negative influence
            rho = 0.1 * (avg_neighbor_coherence / individual_coherence)
        else:
            # Susceptibility to positive influence
            rho = 0.5 * (avg_neighbor_coherence - individual_coherence)
        
        return max(0, min(rho, 1))  # Bound between 0 and 1
    
    def calculate_feedback_strength(
        self,
        coherence_history: List[float],
        window_size: int = 5
    ) -> float:
        """
        Calculate feedback loop strength from historical data
        
        Args:
            coherence_history: List of past coherence measurements
            window_size: Number of measurements to consider
            
        Returns:
            f value (feedback strength)
        """
        if len(coherence_history) < 2:
            return 0.0
        
        # Use recent history
        recent = coherence_history[-window_size:]
        
        if len(recent) < 2:
            return 0.0
        
        # Calculate trend (positive trend = positive feedback)
        x = np.arange(len(recent))
        slope, _ = np.polyfit(x, recent, 1)
        
        # Normalize slope to feedback strength
        # Steeper positive slopes indicate stronger positive feedback
        f = np.tanh(slope * 10)  # Sigmoid-like transformation
        
        return max(0, f)  # Only positive feedback
    
    def calculate_coherence_velocity(
        self,
        measurements: List[CoherenceMeasurement],
        dt: float = 1.0
    ) -> List[float]:
        """
        Calculate coherence velocity (dC/dt) from measurements
        
        Uses: dC/dt = Ψ̇(1 + ρ + f) + ρ̇Ψ + dq*/dt + ḟΨ
        
        Args:
            measurements: List of coherence measurements
            dt: Time step between measurements
            
        Returns:
            List of velocity values
        """
        if len(measurements) < 2:
            return []
        
        velocities = []
        
        for i in range(1, len(measurements)):
            m0 = measurements[i-1]
            m1 = measurements[i]
            
            # Calculate derivatives
            dpsi_dt = (m1.psi - m0.psi) / dt
            drho_dt = (m1.rho - m0.rho) / dt
            dq_dt = (m1.q_optimal - m0.q_optimal) / dt
            df_dt = (m1.f - m0.f) / dt
            
            # Apply velocity equation
            velocity = (
                dpsi_dt * (1 + m1.rho + m1.f) +
                drho_dt * m1.psi +
                dq_dt +
                df_dt * m1.psi
            )
            
            velocities.append(velocity)
        
        return velocities
    
    def identify_breakthrough_moments(
        self,
        measurements: List[CoherenceMeasurement],
        threshold: float = 0.5
    ) -> List[Tuple[int, float]]:
        """
        Identify breakthrough moments in coherence trajectory
        
        Args:
            measurements: List of coherence measurements
            threshold: Velocity threshold for breakthrough
            
        Returns:
            List of (index, velocity) tuples for breakthroughs
        """
        velocities = self.calculate_coherence_velocity(measurements)
        
        breakthroughs = []
        for i, velocity in enumerate(velocities):
            if velocity > threshold:
                breakthroughs.append((i + 1, velocity))
        
        return breakthroughs
    
    def add_measurement(
        self,
        timestamp: float,
        psi: float,
        rho: float,
        q: float,
        f: float,
        metadata: Optional[Dict] = None
    ) -> CoherenceMeasurement:
        """
        Add a new coherence measurement
        
        Args:
            timestamp: Measurement timestamp
            psi: Internal consistency
            rho: Network influence
            q: Raw behavioral efficiency
            f: Feedback strength
            metadata: Optional metadata
            
        Returns:
            CoherenceMeasurement object
        """
        q_optimal = self.calculate_q_optimal(q)
        coherence = self.calculate_coherence(psi, rho, q, f)
        
        measurement = CoherenceMeasurement(
            timestamp=timestamp,
            psi=psi,
            rho=rho,
            q_optimal=q_optimal,
            f=f,
            coherence=coherence,
            metadata=metadata or {}
        )
        
        self.measurements.append(measurement)
        return measurement
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Calculate summary statistics for all measurements
        
        Returns:
            Dictionary of statistics
        """
        if not self.measurements:
            return {}
        
        coherences = [m.coherence for m in self.measurements]
        psis = [m.psi for m in self.measurements]
        rhos = [m.rho for m in self.measurements]
        
        return {
            "mean_coherence": np.mean(coherences),
            "std_coherence": np.std(coherences),
            "min_coherence": np.min(coherences),
            "max_coherence": np.max(coherences),
            "mean_psi": np.mean(psis),
            "mean_rho": np.mean(rhos),
            "total_measurements": len(self.measurements),
            "coherence_trend": self._calculate_trend(coherences)
        }
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate linear trend in values"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        return slope
    
    def export_measurements(self, filepath: str):
        """Export measurements to JSON file"""
        data = [
            {
                "timestamp": m.timestamp,
                "psi": m.psi,
                "rho": m.rho,
                "q_optimal": m.q_optimal,
                "f": m.f,
                "coherence": m.coherence,
                "metadata": m.metadata
            }
            for m in self.measurements
        ]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_measurements(self, filepath: str):
        """Import measurements from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.measurements = []
        for item in data:
            measurement = CoherenceMeasurement(
                timestamp=item["timestamp"],
                psi=item["psi"],
                rho=item["rho"],
                q_optimal=item["q_optimal"],
                f=item["f"],
                coherence=item["coherence"],
                metadata=item.get("metadata", {})
            )
            self.measurements.append(measurement)