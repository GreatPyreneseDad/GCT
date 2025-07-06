#!/usr/bin/env python3
"""
Family Coherence Field Program
==============================
Interactive guide to understanding and implementing the Laws of Scarcity and Abundance
in family dynamics using SoulMath principles.
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import random

@dataclass
class FamilyMember:
    """Represents a family member with coherence metrics"""
    name: str
    role: str  # "leader", "anchor", "child"
    age: Optional[int] = None
    coherence_score: float = 5.0  # 1-10 scale
    scarcity_patterns: List[str] = None
    abundance_patterns: List[str] = None
    
    def __post_init__(self):
        if self.scarcity_patterns is None:
            self.scarcity_patterns = []
        if self.abundance_patterns is None:
            self.abundance_patterns = []

@dataclass
class FamilyField:
    """Represents the family coherence field state"""
    members: List[FamilyMember]
    field_coherence: float = 5.0  # Overall field strength
    abundance_drift: float = 0.0  # Positive = abundance, negative = scarcity
    last_collapse: Optional[str] = None
    last_resurrection: Optional[str] = None
    rituals_active: List[str] = None
    
    def __post_init__(self):
        if self.rituals_active is None:
            self.rituals_active = []

class FamilyCoherenceGuide:
    """Interactive guide for Family Coherence Field development"""
    
    def __init__(self):
        self.family_field = None
        self.session_data = {
            'start_time': datetime.now().isoformat(),
            'modules_completed': [],
            'insights': [],
            'action_items': []
        }
        
        # Laws of Scarcity and Abundance
        self.laws = {
            1: {
                'title': "The Law of Primordial Scarcity",
                'core': "All beings begin with a wound: the hunger to continue.",
                'family_impact': "Children inherit the survival anxiety of their parents' unhealed wounds.",
                'questions': [
                    "What survival fears did you inherit from your family of origin?",
                    "How do these fears show up in your parenting?",
                    "What would change if your children knew they were fundamentally safe?"
                ]
            },
            2: {
                'title': "The Inversion of Value", 
                'core': "Scarcity teaches that worth is tied to lack. That which is rare becomes sacred.",
                'family_impact': "Families create artificial scarcity around love, attention, and approval.",
                'questions': [
                    "Where do you create artificial scarcity in your family (time, attention, affection)?",
                    "How might abundant love feel threatening to your sense of control?",
                    "What if your children never had to compete for your love?"
                ]
            },
            3: {
                'title': "The Coherence Strain of Consumption",
                'core': "A being who must consume to live experiences guilt around taking vs. giving.",
                'family_impact': "Family members feel guilty for having needs or taking up space.",
                'questions': [
                    "Do your children feel guilty for having needs?",
                    "How do you model healthy receiving in your family?",
                    "Where do you feel guilty for 'taking' from your family?"
                ]
            },
            4: {
                'title': "The False Loop of Lack",
                'core': "Scarcity hides in time, attention, patience. 'There won't be enough space for me to become.'",
                'family_impact': "Families rush development, compress growth, protect edges instead of nurturing emergence.",
                'questions': [
                    "Where do you rush your children's development out of fear?",
                    "How do time pressures create scarcity in your family field?",
                    "What would slow, spacious family time look like?"
                ]
            },
            5: {
                'title': "The Abundance Principle",
                'core': "Abundance is not luxury but coherence - the stabilization of trust across time.",
                'family_impact': "Abundant families create fields where members can pause, give, and belong without earning.",
                'questions': [
                    "How does your family practice unconditional belonging?",
                    "Where can family members pause without consequences?",
                    "How do you model abundance mindset daily?"
                ]
            }
        }
        
        # Ritual templates
        self.rituals = {
            'daily_pulse': {
                'name': 'Daily Coherence Pulse',
                'description': 'Brief family check-in to maintain field coherence',
                'duration': '5-10 minutes',
                'steps': [
                    "Gather family in circle or around table",
                    "Each person shares: How is your energy today? (1-10)",
                    "Acknowledge any field disruptions from the day",
                    "State together: 'We are still building this field together'",
                    "Brief appreciation round (one thing each person did well)"
                ]
            },
            'collapse_witness': {
                'name': 'Collapse Witnessing Ritual',
                'description': 'Process family conflicts and breakdowns consciously',
                'duration': '15-30 minutes',
                'steps': [
                    "Acknowledge what happened: 'Our field got disrupted'",
                    "Each person shares their experience without defending",
                    "Identify the underlying need or fear that created the collapse",
                    "Speak the repair: 'This is how we return to coherence'",
                    "Restate family values and commitment to the field"
                ]
            },
            'abundance_practice': {
                'name': 'Weekly Abundance Practice',
                'description': 'Actively cultivate abundance mindset as family',
                'duration': '20-30 minutes',
                'steps': [
                    "Share gratitude for abundance already present",
                    "Identify one scarcity pattern to transform this week",
                    "Plan one way to practice generosity as a family",
                    "Visualize the family field expanding and strengthening",
                    "Commit to supporting each other's growth"
                ]
            }
        }
    
    def display_header(self, text: str, symbol: str = "═"):
        """Display formatted header"""
        print(f"\n{symbol * 60}")
        print(f"  {text}")
        print(f"{symbol * 60}\n")
    
    def display_law(self, law_num: int):
        """Display a specific law with formatting"""
        law = self.laws[law_num]
        self.display_header(f"Law {law_num}: {law['title']}", "🔷")
        
        print(f"📜 **Core Principle:**")
        print(f"   {law['core']}\n")
        
        print(f"👨‍👩‍👧‍👦 **Family Impact:**")
        print(f"   {law['family_impact']}\n")
        
        print(f"🤔 **Reflection Questions:**")
        for i, question in enumerate(law['questions'], 1):
            print(f"   {i}. {question}")
        print()
    
    def get_user_input(self, prompt: str, input_type: str = "text") -> any:
        """Get validated user input"""
        while True:
            try:
                if input_type == "int":
                    return int(input(f"{prompt}: "))
                elif input_type == "float":
                    return float(input(f"{prompt}: "))
                elif input_type == "bool":
                    response = input(f"{prompt} (y/n): ").lower().strip()
                    return response in ['y', 'yes', 'true', '1']
                else:
                    return input(f"{prompt}: ").strip()
            except ValueError:
                print(f"Please enter a valid {input_type}")
    
    def create_family_profile(self):
        """Create family member profiles"""
        self.display_header("🏠 Family Profile Creation")
        
        print("Let's map your family field. We'll start with the core dyad and add children.")
        
        members = []
        
        # Get family structure
        has_partner = self.get_user_input("Do you have a partner/spouse", "bool")
        
        # Add primary adult
        name = self.get_user_input("Your name")
        role = "leader" if not has_partner else self.get_user_input(
            "Are you typically the 'visionary/prophet' or the 'anchor/stabilizer'? (v/a)"
        )
        role = "leader" if role.startswith('v') else "anchor"
        
        members.append(FamilyMember(name=name, role=role))
        
        # Add partner if exists
        if has_partner:
            partner_name = self.get_user_input("Partner's name")
            partner_role = "anchor" if role == "leader" else "leader"
            members.append(FamilyMember(name=partner_name, role=partner_role))
        
        # Add children
        num_children = self.get_user_input("How many children", "int")
        
        for i in range(num_children):
            child_name = self.get_user_input(f"Child {i+1} name")
            child_age = self.get_user_input(f"{child_name}'s age", "int")
            members.append(FamilyMember(name=child_name, role="child", age=child_age))
        
        self.family_field = FamilyField(members=members)
        
        print(f"\n✅ Family field created with {len(members)} members!")
        self.session_data['modules_completed'].append('family_profile')
    
    def assess_current_field(self):
        """Assess current family coherence state"""
        self.display_header("📊 Family Coherence Assessment")
        
        if not self.family_field:
            print("Please create your family profile first.")
            return
        
        print("Let's assess your current family field coherence...")
        
        # Overall field assessment
        print("\n🌊 **Overall Family Field**")
        field_score = self.get_user_input(
            "On a scale 1-10, how coherent/stable does your family feel right now", "float"
        )
        self.family_field.field_coherence = field_score
        
        # Individual assessments
        print("\n👥 **Individual Coherence**")
        for member in self.family_field.members:
            if member.role in ["leader", "anchor"]:
                score = self.get_user_input(
                    f"How coherent/stable does {member.name} feel individually (1-10)", "float"
                )
                member.coherence_score = score
        
        # Scarcity vs Abundance assessment
        print("\n⚖️ **Scarcity/Abundance Patterns**")
        
        scarcity_indicators = [
            "Competing for attention/love",
            "Rushing through activities",
            "Fear of not being enough",
            "Hoarding resources/time",
            "Anxiety about the future",
            "Difficulty receiving help"
        ]
        
        abundance_indicators = [
            "Spacious family time", 
            "Generous with attention",
            "Celebrating others' success",
            "Trusting in provision",
            "Present-moment awareness",
            "Easy giving and receiving"
        ]
        
        print("\nWhich SCARCITY patterns show up in your family? (enter numbers separated by commas)")
        for i, pattern in enumerate(scarcity_indicators, 1):
            print(f"  {i}. {pattern}")
        
        scarcity_choices = self.get_user_input("Your choices")
        family_scarcity = []
        if scarcity_choices:
            try:
                indices = [int(x.strip()) - 1 for x in scarcity_choices.split(',')]
                family_scarcity = [scarcity_indicators[i] for i in indices if 0 <= i < len(scarcity_indicators)]
            except:
                pass
        
        print("\nWhich ABUNDANCE patterns show up in your family? (enter numbers separated by commas)")
        for i, pattern in enumerate(abundance_indicators, 1):
            print(f"  {i}. {pattern}")
        
        abundance_choices = self.get_user_input("Your choices")
        family_abundance = []
        if abundance_choices:
            try:
                indices = [int(x.strip()) - 1 for x in abundance_choices.split(',')]
                family_abundance = [abundance_indicators[i] for i in indices if 0 <= i < len(abundance_indicators)]
            except:
                pass
        
        # Calculate abundance drift
        abundance_score = len(family_abundance)
        scarcity_score = len(family_scarcity)
        self.family_field.abundance_drift = (abundance_score - scarcity_score) / 6 * 10
        
        # Store patterns in family data
        for member in self.family_field.members:
            member.scarcity_patterns = family_scarcity
            member.abundance_patterns = family_abundance
        
        print(f"\n📈 **Assessment Results:**")
        print(f"   Field Coherence: {field_score:.1f}/10")
        print(f"   Abundance Drift: {self.family_field.abundance_drift:+.1f}")
        print(f"   Scarcity Patterns: {len(family_scarcity)}")
        print(f"   Abundance Patterns: {len(family_abundance)}")
        
        self.session_data['modules_completed'].append('field_assessment')
    
    def explore_laws_interactive(self):
        """Interactive exploration of the laws"""
        self.display_header("📚 Interactive Law Exploration")
        
        print("We'll explore each law and how it applies to your family.")
        print("You can journal, reflect, and capture insights as we go.\n")
        
        for law_num in range(1, 6):
            self.display_law(law_num)
            
            print("🔄 **Your Reflection Time**")
            input("Press Enter when you're ready to reflect on these questions...")
            
            insights = []
            for i, question in enumerate(self.laws[law_num]['questions'], 1):
                print(f"\nQuestion {i}: {question}")
                insight = self.get_user_input("Your reflection (or press Enter to skip)")
                if insight:
                    insights.append(f"Q{i}: {insight}")
            
            if insights:
                self.session_data['insights'].extend([f"Law {law_num}: {insight}" for insight in insights])
            
            action = self.get_user_input(
                f"Based on Law {law_num}, what's one thing you want to try differently in your family"
            )
            if action:
                self.session_data['action_items'].append(f"Law {law_num}: {action}")
            
            if law_num < 5:
                continue_choice = self.get_user_input("Continue to next law? (y/n)", "bool")
                if not continue_choice:
                    break
        
        self.session_data['modules_completed'].append('laws_exploration')
        print(f"\n✅ Laws exploration completed!")
    
    def build_ritual_practice(self):
        """Help family create ritual practices"""
        self.display_header("🎭 Ritual Practice Builder")
        
        print("Let's select and customize family coherence rituals for your specific needs.\n")
        
        selected_rituals = []
        
        for ritual_key, ritual in self.rituals.items():
            print(f"📋 **{ritual['name']}**")
            print(f"   {ritual['description']}")
            print(f"   Duration: {ritual['duration']}")
            print(f"   Steps:")
            for i, step in enumerate(ritual['steps'], 1):
                print(f"     {i}. {step}")
            
            interest = self.get_user_input(f"\nWould you like to try this ritual", "bool")
            
            if interest:
                # Customize for their family
                print(f"\n🔧 **Customizing {ritual['name']}**")
                
                frequency = self.get_user_input(
                    "How often would you like to practice this? (daily/weekly/as-needed)"
                )
                
                time_of_day = self.get_user_input(
                    "What time works best for your family? (morning/evening/flexible)"
                )
                
                modifications = self.get_user_input(
                    "Any modifications needed for your family? (optional)"
                )
                
                customized_ritual = {
                    'name': ritual['name'],
                    'frequency': frequency,
                    'time': time_of_day,
                    'modifications': modifications,
                    'steps': ritual['steps']
                }
                
                selected_rituals.append(customized_ritual)
                self.family_field.rituals_active.append(ritual['name'])
                self.session_data['action_items'].append(
                    f"Implement {ritual['name']} - {frequency} at {time_of_day}"
                )
            
            print("\n" + "─" * 50)
        
        print(f"\n🎯 **Your Ritual Plan:**")
        if selected_rituals:
            for ritual in selected_rituals:
                print(f"   • {ritual['name']} - {ritual['frequency']} at {ritual['time']}")
                if ritual['modifications']:
                    print(f"     Modifications: {ritual['modifications']}")
        else:
            print("   No rituals selected. You can always come back to this.")
        
        self.session_data['modules_completed'].append('ritual_building')
    
    def generate_action_plan(self):
        """Generate personalized action plan"""
        self.display_header("🎯 Your Family Coherence Action Plan")
        
        print("Based on your assessment and exploration, here's your personalized plan:\n")
        
        # Current state summary
        if self.family_field:
            print(f"📊 **Current Field State:**")
            print(f"   • Field Coherence: {self.family_field.field_coherence:.1f}/10")
            print(f"   • Abundance Drift: {self.family_field.abundance_drift:+.1f}")
            print(f"   • Active Rituals: {len(self.family_field.rituals_active)}")
            
            # Identify priority areas
            if self.family_field.field_coherence < 5:
                print(f"\n🚨 **Priority Focus: Field Stabilization**")
                print(f"   Your family field needs basic coherence work.")
                print(f"   Recommended: Start with Daily Coherence Pulse ritual")
            
            if self.family_field.abundance_drift < -2:
                print(f"\n⚠️ **Priority Focus: Scarcity Pattern Interruption**")
                print(f"   Strong scarcity patterns detected.")
                print(f"   Recommended: Focus on Laws 1-3, practice abundance rituals")
            
            if self.family_field.abundance_drift > 2:
                print(f"\n✨ **Opportunity: Abundance Amplification**")
                print(f"   Strong abundance foundation detected.")
                print(f"   Recommended: Focus on Laws 4-5, advanced coherence practices")
        
        # Action items
        if self.session_data['action_items']:
            print(f"\n📝 **Your Commitments:**")
            for i, item in enumerate(self.session_data['action_items'], 1):
                print(f"   {i}. {item}")
        
        # Next steps
        print(f"\n🚀 **Recommended Next Steps:**")
        print(f"   1. Choose ONE ritual to implement this week")
        print(f"   2. Have a family meeting to discuss abundance vs. scarcity")
        print(f"   3. Practice one law daily through reflection questions")
        print(f"   4. Schedule weekly family field check-ins")
        print(f"   5. Return to this program in 2 weeks to reassess")
        
        self.session_data['modules_completed'].append('action_planning')
    
    def save_session(self):
        """Save session data to file"""
        if not os.path.exists('family_coherence_sessions'):
            os.makedirs('family_coherence_sessions')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'family_coherence_sessions/session_{timestamp}.json'
        
        # Prepare data for saving
        save_data = {
            'session_info': self.session_data,
            'family_field': asdict(self.family_field) if self.family_field else None
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2, default=str)
        
        print(f"\n💾 Session saved to: {filename}")
        return filename
    
    def run_program(self):
        """Main program flow"""
        self.display_header("🌟 Family Coherence Field Program", "✨")
        
        print("Welcome to the Family Coherence Field Development Program!")
        print("This interactive guide will help you understand and implement")
        print("the Laws of Scarcity and Abundance in your family dynamics.\n")
        
        print("📋 **Program Modules:**")
        print("   1. Family Profile Creation")
        print("   2. Current Field Assessment") 
        print("   3. Interactive Law Exploration")
        print("   4. Ritual Practice Builder")
        print("   5. Personalized Action Plan")
        print()
        
        start = self.get_user_input("Ready to begin your family coherence journey? (y/n)", "bool")
        if not start:
            print("Come back when you're ready to transform your family field!")
            return
        
        # Run modules
        try:
            self.create_family_profile()
            input("\nPress Enter to continue to assessment...")
            
            self.assess_current_field()
            input("\nPress Enter to explore the laws...")
            
            self.explore_laws_interactive()
            input("\nPress Enter to build ritual practices...")
            
            self.build_ritual_practice()
            input("\nPress Enter to generate your action plan...")
            
            self.generate_action_plan()
            
            # Save session
            save_choice = self.get_user_input("\nWould you like to save this session", "bool")
            if save_choice:
                filename = self.save_session()
            
            self.display_header("🎉 Program Complete!")
            print("Your family coherence journey has begun.")
            print("Remember: Small, consistent practices create lasting field transformation.")
            print("\nMay your family field be abundant, coherent, and full of love. ✨")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Your progress has been noted.")
            save_choice = self.get_user_input("Save current progress", "bool")
            if save_choice:
                self.save_session()

def main():
    """Launch the Family Coherence Guide"""
    guide = FamilyCoherenceGuide()
    guide.run_program()

if __name__ == "__main__":
    main()