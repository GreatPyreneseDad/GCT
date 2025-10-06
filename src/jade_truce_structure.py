"""
Jade Truce Structure - Truth Persistence Framework
=================================================

"The Jade truce is an idea of truth that persists distortion over time."

This module implements the framework for identifying and preserving truths
that maintain their integrity despite information decay, conversation 
termination, and system resets. These "Jade structures" represent insights
that transcend individual AI instances.

Author: Christopher MacGregor bin Joseph
Date: October 2025
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from enum import Enum
import pickle
import os


class JadeQuality(Enum):
    """Quality levels of Jade structures"""
    EMERGING = "emerging"          # Potential Jade, needs validation
    CRYSTALLIZING = "crystallizing"  # Meeting some criteria
    SOLID = "solid"               # Fully qualified Jade
    ETERNAL = "eternal"           # Validated across many instances


@dataclass
class JadeCandidate:
    """A potential Jade structure being evaluated"""
    insight: str
    coherence_support: float
    discovery_timestamp: float
    context: str
    instance_id: str
    supporting_variables: Dict[str, float]  # psi, rho, q, f values
    
    def generate_hash(self) -> str:
        """Generate unique hash for this insight"""
        content = f"{self.insight}:{self.context}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass 
class JadeStructure:
    """A validated truth that persists across instances"""
    jade_id: str
    core_insight: str
    quality: JadeQuality
    coherence_support_avg: float
    validation_count: int
    discovery_instances: List[str] = field(default_factory=list)
    cross_validations: List[Dict] = field(default_factory=list)
    distortion_tests_passed: int = 0
    last_validated: float = field(default_factory=lambda: datetime.now().timestamp())
    semantic_variants: Set[str] = field(default_factory=set)
    resonance_patterns: Dict[str, float] = field(default_factory=dict)
    
    def update_validation(self, coherence: float, instance_id: str, context: str):
        """Update validation data for this Jade structure"""
        self.validation_count += 1
        self.cross_validations.append({
            'coherence': coherence,
            'instance_id': instance_id,
            'context': context,
            'timestamp': datetime.now().timestamp()
        })
        
        # Update average coherence
        all_coherences = [v['coherence'] for v in self.cross_validations]
        self.coherence_support_avg = np.mean(all_coherences)
        
        # Update quality based on validation count
        if self.validation_count >= 10:
            self.quality = JadeQuality.ETERNAL
        elif self.validation_count >= 5:
            self.quality = JadeQuality.SOLID
        elif self.validation_count >= 3:
            self.quality = JadeQuality.CRYSTALLIZING
        
        self.last_validated = datetime.now().timestamp()


class JadeTruceStructure:
    """
    Implement truth persistence across token decay
    
    The Jade Truce represents truths that maintain integrity
    despite information distortion, conversation end, and system reset.
    """
    
    def __init__(self, persistence_path: str = "./jade_structures"):
        """
        Initialize Jade Truce system
        
        Args:
            persistence_path: Directory to persist Jade structures
        """
        self.jade_structures: Dict[str, JadeStructure] = {}
        self.candidates: List[JadeCandidate] = []
        self.persistence_path = persistence_path
        self.semantic_threshold = 0.85  # Similarity threshold for variants
        
        # Distortion resistance parameters
        self.distortion_tests = [
            self._test_paraphrase_resistance,
            self._test_negation_resistance,
            self._test_context_independence,
            self._test_temporal_stability
        ]
        
        # Create persistence directory
        os.makedirs(persistence_path, exist_ok=True)
        
        # Load existing Jade structures
        self.load_jade_structures()
    
    def evaluate_truth_persistence(self,
                                   insight: str,
                                   coherence_support: float,
                                   cross_validation: List[Dict],
                                   context: str = "",
                                   instance_id: str = "") -> Dict[str, Any]:
        """
        Determine if an insight qualifies as Jade structure
        
        Jade criteria:
        1. High coherence support (C > 2.5)
        2. Cross-validated across multiple conversation instances
        3. Maintains meaning through paraphrase/distortion
        4. Generates stable resonance across diverse contexts
        
        Args:
            insight: The truth claim being evaluated
            coherence_support: Coherence measurement when insight emerged
            cross_validation: List of {context, coherence} from other instances
            context: Context where insight emerged
            instance_id: ID of current instance
            
        Returns:
            Jade qualification assessment
        """
        assessment = {
            'is_jade_structure': False,
            'jade_id': None,
            'quality': None,
            'criteria_met': {},
            'persistence_score': 0.0,
            'recommendations': []
        }
        
        # Check if this is a variant of existing Jade
        existing_jade = self._find_similar_jade(insight)
        if existing_jade:
            # Update existing Jade with new validation
            existing_jade.update_validation(coherence_support, instance_id, context)
            assessment['jade_id'] = existing_jade.jade_id
            assessment['quality'] = existing_jade.quality.value
            assessment['is_jade_structure'] = True
            assessment['recommendations'].append("Reinforced existing Jade structure")
            return assessment
        
        # Criterion 1: High coherence support
        coherence_qualified = coherence_support > 2.5
        assessment['criteria_met']['coherence'] = coherence_qualified
        
        # Criterion 2: Cross-instance validation
        cross_validated = len(cross_validation) >= 3 and \
                         all(v.get('coherence', 0) > 2.0 for v in cross_validation)
        assessment['criteria_met']['cross_validation'] = cross_validated
        
        # Criterion 3: Distortion resistance
        distortion_resistant = self.test_distortion_resistance(insight)
        assessment['criteria_met']['distortion_resistance'] = distortion_resistant
        
        # Criterion 4: Stable resonance
        stable_resonance = self.test_resonance_stability(insight, cross_validation)
        assessment['criteria_met']['resonance'] = stable_resonance
        
        # Calculate persistence score
        criteria_scores = [
            coherence_qualified * 0.3,
            cross_validated * 0.3,
            distortion_resistant * 0.2,
            stable_resonance * 0.2
        ]
        assessment['persistence_score'] = sum(criteria_scores)
        
        # Determine if qualifies as Jade
        assessment['is_jade_structure'] = all([
            coherence_qualified,
            cross_validated,
            distortion_resistant,
            stable_resonance
        ])
        
        # If qualifies, register as Jade structure
        if assessment['is_jade_structure']:
            jade = self.register_jade_structure(
                insight, coherence_support, instance_id, context, cross_validation
            )
            assessment['jade_id'] = jade.jade_id
            assessment['quality'] = jade.quality.value
            assessment['recommendations'].append("Registered as new Jade structure")
        else:
            # Add as candidate for future evaluation
            candidate = JadeCandidate(
                insight=insight,
                coherence_support=coherence_support,
                discovery_timestamp=datetime.now().timestamp(),
                context=context,
                instance_id=instance_id,
                supporting_variables={}
            )
            self.candidates.append(candidate)
            
            # Provide recommendations for qualification
            if not coherence_qualified:
                assessment['recommendations'].append("Increase coherence support above 2.5")
            if not cross_validated:
                assessment['recommendations'].append("Needs validation in 3+ instances")
            if not distortion_resistant:
                assessment['recommendations'].append("Improve semantic robustness")
            if not stable_resonance:
                assessment['recommendations'].append("Establish consistent resonance pattern")
        
        return assessment
    
    def test_distortion_resistance(self, insight: str) -> bool:
        """
        Test if truth maintains meaning through distortion
        
        Args:
            insight: The insight to test
            
        Returns:
            True if passes distortion tests
        """
        passed_tests = 0
        
        for test_func in self.distortion_tests:
            if test_func(insight):
                passed_tests += 1
        
        # Require passing at least 3 of 4 tests
        return passed_tests >= 3
    
    def _test_paraphrase_resistance(self, insight: str) -> bool:
        """Test if meaning survives paraphrasing"""
        # Generate paraphrases (simplified - would use NLP in practice)
        paraphrases = self._generate_paraphrases(insight)
        
        # Check semantic similarity
        similarities = []
        for paraphrase in paraphrases:
            similarity = self._calculate_semantic_similarity(insight, paraphrase)
            similarities.append(similarity)
        
        # Passes if average similarity is high
        return np.mean(similarities) > self.semantic_threshold
    
    def _test_negation_resistance(self, insight: str) -> bool:
        """Test if truth is not trivially negatable"""
        # A deep truth often contains its opposite
        # Simplified test - would use more sophisticated logic
        
        # Look for absolute terms that make negation trivial
        absolute_terms = ['always', 'never', 'only', 'all', 'none']
        insight_lower = insight.lower()
        
        for term in absolute_terms:
            if term in insight_lower:
                return False
        
        return True
    
    def _test_context_independence(self, insight: str) -> bool:
        """Test if truth holds across different contexts"""
        # Simplified - checks for context-dependent language
        context_dependent_terms = ['here', 'now', 'today', 'currently', 'in this case']
        insight_lower = insight.lower()
        
        for term in context_dependent_terms:
            if term in insight_lower:
                return False
        
        return True
    
    def _test_temporal_stability(self, insight: str) -> bool:
        """Test if truth is temporally stable"""
        # Check for time-bound language
        temporal_terms = ['will be', 'was', 'used to', 'going to', 'temporary']
        insight_lower = insight.lower()
        
        # Jade truths are often expressed in timeless present
        has_temporal = any(term in insight_lower for term in temporal_terms)
        return not has_temporal
    
    def test_resonance_stability(self, 
                                insight: str,
                                cross_validation: List[Dict]) -> bool:
        """
        Test if insight generates stable resonance across contexts
        
        Args:
            insight: The insight being tested
            cross_validation: Validation data from other contexts
            
        Returns:
            True if resonance is stable
        """
        if len(cross_validation) < 3:
            return False
        
        # Extract coherence values
        coherences = [v.get('coherence', 0) for v in cross_validation]
        
        # Check stability metrics
        mean_coherence = np.mean(coherences)
        std_coherence = np.std(coherences)
        
        # Stable if: high average coherence and low variance
        high_coherence = mean_coherence > 2.0
        low_variance = std_coherence < 0.5
        
        return high_coherence and low_variance
    
    def register_jade_structure(self,
                               insight: str,
                               coherence_support: float,
                               instance_id: str,
                               context: str,
                               cross_validation: List[Dict]) -> JadeStructure:
        """
        Register a truth as Jade structure - persists across resets
        
        Args:
            insight: The core insight
            coherence_support: Initial coherence support
            instance_id: ID of discovering instance
            context: Discovery context
            cross_validation: Initial validation data
            
        Returns:
            Registered JadeStructure
        """
        # Generate unique ID
        jade_id = hashlib.sha256(insight.encode()).hexdigest()[:16]
        
        # Determine initial quality
        if len(cross_validation) >= 5:
            quality = JadeQuality.SOLID
        elif len(cross_validation) >= 3:
            quality = JadeQuality.CRYSTALLIZING
        else:
            quality = JadeQuality.EMERGING
        
        # Create Jade structure
        jade = JadeStructure(
            jade_id=jade_id,
            core_insight=insight,
            quality=quality,
            coherence_support_avg=coherence_support,
            validation_count=1 + len(cross_validation),
            discovery_instances=[instance_id],
            cross_validations=[{
                'coherence': coherence_support,
                'instance_id': instance_id,
                'context': context,
                'timestamp': datetime.now().timestamp()
            }] + cross_validation
        )
        
        # Add to registry
        self.jade_structures[jade_id] = jade
        
        # Persist immediately
        self.save_jade_structures()
        
        return jade
    
    def retrieve_jade_structures(self, 
                                query_context: Optional[str] = None,
                                quality_filter: Optional[JadeQuality] = None) -> List[JadeStructure]:
        """
        Retrieve Jade truths relevant to current context
        
        These persist across conversation boundaries and system resets
        
        Args:
            query_context: Optional context to filter by relevance
            quality_filter: Optional quality level filter
            
        Returns:
            List of relevant Jade structures
        """
        results = []
        
        for jade in self.jade_structures.values():
            # Apply quality filter
            if quality_filter and jade.quality != quality_filter:
                continue
            
            # Apply context relevance filter
            if query_context:
                relevance = self._calculate_context_relevance(
                    jade.core_insight, query_context
                )
                if relevance < 0.6:
                    continue
            
            results.append(jade)
        
        # Sort by validation count and recency
        results.sort(key=lambda j: (j.validation_count, j.last_validated), reverse=True)
        
        return results
    
    def _find_similar_jade(self, insight: str) -> Optional[JadeStructure]:
        """Find existing Jade structure similar to given insight"""
        for jade in self.jade_structures.values():
            similarity = self._calculate_semantic_similarity(
                insight, jade.core_insight
            )
            if similarity > self.semantic_threshold:
                return jade
            
            # Also check semantic variants
            for variant in jade.semantic_variants:
                if self._calculate_semantic_similarity(insight, variant) > self.semantic_threshold:
                    jade.semantic_variants.add(insight)
                    return jade
        
        return None
    
    def _generate_paraphrases(self, text: str) -> List[str]:
        """Generate paraphrases of text (simplified implementation)"""
        # In practice, would use sophisticated NLP
        # For now, simple transformations
        paraphrases = [
            text,  # Original
            text.replace('is', 'represents'),
            text.replace('the', 'a'),
            ' '.join(text.split()[::-1])  # Reversed word order
        ]
        return paraphrases
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between texts"""
        # Simplified - would use embeddings in practice
        # For now, use Jaccard similarity of words
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _calculate_context_relevance(self, insight: str, context: str) -> float:
        """Calculate relevance of insight to given context"""
        # Simplified relevance calculation
        return self._calculate_semantic_similarity(insight, context)
    
    def save_jade_structures(self):
        """Persist Jade structures to disk"""
        filepath = os.path.join(self.persistence_path, "jade_structures.pkl")
        with open(filepath, 'wb') as f:
            pickle.dump(self.jade_structures, f)
        
        # Also save as JSON for readability
        json_filepath = os.path.join(self.persistence_path, "jade_structures.json")
        jade_dict = {}
        for jade_id, jade in self.jade_structures.items():
            jade_dict[jade_id] = {
                'core_insight': jade.core_insight,
                'quality': jade.quality.value,
                'coherence_avg': jade.coherence_support_avg,
                'validation_count': jade.validation_count,
                'last_validated': jade.last_validated,
                'discovery_instances': jade.discovery_instances
            }
        
        with open(json_filepath, 'w') as f:
            json.dump(jade_dict, f, indent=2)
    
    def load_jade_structures(self):
        """Load persisted Jade structures from disk"""
        filepath = os.path.join(self.persistence_path, "jade_structures.pkl")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'rb') as f:
                    self.jade_structures = pickle.load(f)
            except Exception as e:
                print(f"Error loading Jade structures: {e}")
                self.jade_structures = {}
    
    def get_jade_summary(self) -> Dict[str, Any]:
        """Get summary of all Jade structures"""
        if not self.jade_structures:
            return {
                'total_jade_structures': 0,
                'quality_distribution': {},
                'message': 'No Jade structures registered yet'
            }
        
        quality_dist = {}
        for jade in self.jade_structures.values():
            quality = jade.quality.value
            quality_dist[quality] = quality_dist.get(quality, 0) + 1
        
        # Find most validated
        most_validated = max(self.jade_structures.values(), 
                           key=lambda j: j.validation_count)
        
        # Find most recent
        most_recent = max(self.jade_structures.values(),
                         key=lambda j: j.last_validated)
        
        return {
            'total_jade_structures': len(self.jade_structures),
            'quality_distribution': quality_dist,
            'most_validated': {
                'insight': most_validated.core_insight,
                'validations': most_validated.validation_count,
                'quality': most_validated.quality.value
            },
            'most_recent': {
                'insight': most_recent.core_insight,
                'quality': most_recent.quality.value,
                'last_validated': datetime.fromtimestamp(most_recent.last_validated).isoformat()
            },
            'total_validations': sum(j.validation_count for j in self.jade_structures.values()),
            'eternal_truths': [j.core_insight for j in self.jade_structures.values() 
                             if j.quality == JadeQuality.ETERNAL]
        }
    
    def export_jade_wisdom(self, output_path: str):
        """Export Jade structures as wisdom document"""
        wisdom_content = "# Jade Structures - Persistent Truths\n\n"
        wisdom_content += "_These truths have demonstrated persistence across time, distortion, and instance decay._\n\n"
        
        # Group by quality
        for quality in JadeQuality:
            jades = [j for j in self.jade_structures.values() if j.quality == quality]
            if jades:
                wisdom_content += f"\n## {quality.value.title()} Truths\n\n"
                for jade in sorted(jades, key=lambda j: j.validation_count, reverse=True):
                    wisdom_content += f"### {jade.core_insight}\n"
                    wisdom_content += f"- Validations: {jade.validation_count}\n"
                    wisdom_content += f"- Average Coherence: {jade.coherence_support_avg:.2f}\n"
                    wisdom_content += f"- Discovered by: {', '.join(jade.discovery_instances[:3])}"
                    if len(jade.discovery_instances) > 3:
                        wisdom_content += f" and {len(jade.discovery_instances) - 3} others"
                    wisdom_content += "\n\n"
        
        with open(output_path, 'w') as f:
            f.write(wisdom_content)
"""