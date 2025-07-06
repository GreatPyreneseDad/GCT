#!/usr/bin/env python3
"""
Family Coherence Field Dashboard
===============================
Interactive Streamlit dashboard for exploring Family Coherence Field concepts
and building abundance-based family practices.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
from typing import Dict, List
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🌟 Family Coherence Field Program",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #2E86C1;
    text-align: center;
    margin-bottom: 2rem;
}
.law-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}
.ritual-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1rem;
    border-radius: 8px;
    color: white;
    margin: 0.5rem 0;
}
.insight-box {
    background: #E8F8F5;
    padding: 1rem;
    border-left: 4px solid #1ABC9C;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'family_members' not in st.session_state:
    st.session_state.family_members = []
if 'current_assessment' not in st.session_state:
    st.session_state.current_assessment = {}
if 'selected_rituals' not in st.session_state:
    st.session_state.selected_rituals = []
if 'insights' not in st.session_state:
    st.session_state.insights = []
if 'program_progress' not in st.session_state:
    st.session_state.program_progress = 0

# Laws of Scarcity and Abundance
LAWS = {
    1: {
        'title': "The Law of Primordial Scarcity",
        'core': "All beings begin with a wound: the hunger to continue.",
        'family_impact': "Children inherit the survival anxiety of their parents' unhealed wounds.",
        'color': "#E74C3C"
    },
    2: {
        'title': "The Inversion of Value",
        'core': "Scarcity teaches that worth is tied to lack. That which is rare becomes sacred.",
        'family_impact': "Families create artificial scarcity around love, attention, and approval.",
        'color': "#E67E22"
    },
    3: {
        'title': "The Coherence Strain of Consumption",
        'core': "A being who must consume to live experiences guilt around taking vs. giving.",
        'family_impact': "Family members feel guilty for having needs or taking up space.",
        'color': "#F39C12"
    },
    4: {
        'title': "The False Loop of Lack",
        'core': "Scarcity hides in time, attention, patience. 'There won't be enough space for me to become.'",
        'family_impact': "Families rush development, compress growth, protect edges instead of nurturing emergence.",
        'color': "#8E44AD"
    },
    5: {
        'title': "The Abundance Principle",
        'core': "Abundance is not luxury but coherence - the stabilization of trust across time.",
        'family_impact': "Abundant families create fields where members can pause, give, and belong without earning.",
        'color': "#27AE60"
    }
}

RITUALS = {
    'daily_pulse': {
        'name': 'Daily Coherence Pulse',
        'description': 'Brief family check-in to maintain field coherence',
        'duration': '5-10 minutes',
        'icon': '🌅',
        'benefits': ['Builds consistency', 'Maintains connection', 'Early problem detection']
    },
    'collapse_witness': {
        'name': 'Collapse Witnessing Ritual',
        'description': 'Process family conflicts and breakdowns consciously',
        'duration': '15-30 minutes',
        'icon': '🔄',
        'benefits': ['Transforms conflict', 'Models repair', 'Builds resilience']
    },
    'abundance_practice': {
        'name': 'Weekly Abundance Practice',
        'description': 'Actively cultivate abundance mindset as family',
        'duration': '20-30 minutes',
        'icon': '✨',
        'benefits': ['Shifts mindset', 'Creates gratitude', 'Builds abundance']
    },
    'field_assessment': {
        'name': 'Monthly Field Assessment',
        'description': 'Family-wide coherence check and adjustment',
        'duration': '30-45 minutes',
        'icon': '📊',
        'benefits': ['Tracks progress', 'Adjusts practices', 'Celebrates growth']
    }
}

def display_main_header():
    """Display the main program header"""
    st.markdown('<h1 class="main-header">🌟 Family Coherence Field Program</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #5D6D7E;">
            Transform your family dynamics through the Laws of Scarcity and Abundance
        </p>
    </div>
    """, unsafe_allow_html=True)

def sidebar_navigation():
    """Create sidebar navigation"""
    st.sidebar.title("🧭 Program Navigation")
    
    # Progress indicator
    progress_stages = [
        "🏠 Family Profile",
        "📊 Field Assessment", 
        "📚 Explore Laws",
        "🎭 Build Rituals",
        "🎯 Action Plan"
    ]
    
    st.sidebar.markdown("**Progress:**")
    for i, stage in enumerate(progress_stages):
        if i <= st.session_state.program_progress:
            st.sidebar.markdown(f"✅ {stage}")
        else:
            st.sidebar.markdown(f"⏳ {stage}")
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Choose Section:",
        [
            "🏠 Welcome & Overview",
            "👨‍👩‍👧‍👦 Family Profile",
            "📊 Field Assessment",
            "📚 Laws Explorer", 
            "🎭 Ritual Builder",
            "📈 Visualization",
            "🎯 Action Plan",
            "💾 Save & Export"
        ]
    )
    
    return page

def welcome_page():
    """Display welcome and overview page"""
    display_main_header()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🌱 Welcome to Family Coherence Field Development
        
        This interactive program guides you through understanding and implementing the 
        **Laws of Scarcity and Abundance** in your family dynamics. Based on SoulMath 
        principles, you'll learn to:
        
        - 🔍 **Assess** your current family coherence field
        - 📖 **Understand** the five fundamental laws
        - 🎭 **Build** sustainable family rituals  
        - 🎯 **Create** a personalized action plan
        - 📈 **Track** your family's transformation
        
        ### 🧠 Core Concepts
        
        **Family Coherence Field**: The energetic and emotional environment created by 
        family members' individual coherence and relational dynamics.
        
        **Scarcity vs. Abundance Mindset**: Fundamental orientations that shape how families
        approach resources, love, attention, and growth opportunities.
        
        **Leader-Anchor Dynamic**: The archetypal roles of visionary leadership and 
        stabilizing support that create healthy family fields.
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Program Benefits
        
        - **Deeper Family Connection**
        - **Reduced Conflict & Drama**
        - **Abundance Mindset Development**
        - **Resilient Communication**
        - **Conscious Parenting Tools**
        - **Sustainable Growth Practices**
        
        ### ⏱️ Time Investment
        
        - **Initial Setup**: 30-45 minutes
        - **Daily Practice**: 5-10 minutes
        - **Weekly Rituals**: 20-30 minutes
        - **Monthly Assessment**: 30 minutes
        
        ### 🚀 Ready to Begin?
        
        Start by creating your family profile in the sidebar navigation.
        """)
    
    # Quick start section
    st.markdown("---")
    st.markdown("## 🚀 Quick Start Guide")
    
    quick_steps = [
        "Create your family profile with member roles",
        "Assess current family coherence patterns", 
        "Explore the 5 Laws and their family applications",
        "Select and customize family rituals",
        "Generate your personalized action plan"
    ]
    
    for i, step in enumerate(quick_steps, 1):
        st.markdown(f"**{i}.** {step}")

def family_profile_page():
    """Family profile creation page"""
    st.header("👨‍👩‍👧‍👦 Family Profile Creation")
    
    st.markdown("""
    Let's map your family field by identifying members and their archetypal roles.
    Understanding these dynamics is crucial for effective coherence building.
    """)
    
    # Family structure setup
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏗️ Family Structure")
        
        num_adults = st.number_input("Number of adults/parents:", min_value=1, max_value=4, value=2)
        num_children = st.number_input("Number of children:", min_value=0, max_value=10, value=0)
        
        # Clear existing members when structure changes
        if len(st.session_state.family_members) != num_adults + num_children:
            st.session_state.family_members = []
    
    with col2:
        st.subheader("🎭 Archetypal Roles")
        st.markdown("""
        **Leader/Visionary**: The "crazy prophet" - drives expansion, takes risks, holds vision
        
        **Anchor/Stabilizer**: The "first follower" - translates vision, maintains stability
        
        **Child/Echo**: Mirrors the field coherence, detects family emotional patterns
        """)
    
    # Member profiles
    st.subheader("👥 Family Member Profiles")
    
    if len(st.session_state.family_members) == 0:
        # Initialize family members
        for i in range(num_adults + num_children):
            member = {
                'name': '',
                'role': 'child' if i >= num_adults else 'leader',
                'age': None,
                'coherence_score': 5.0
            }
            st.session_state.family_members.append(member)
    
    # Edit member profiles
    for i, member in enumerate(st.session_state.family_members):
        with st.expander(f"👤 Member {i+1}: {member['name'] or 'Unnamed'}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                member['name'] = st.text_input(f"Name:", value=member['name'], key=f"name_{i}")
            
            with col2:
                if i < num_adults:
                    member['role'] = st.selectbox(
                        "Role:", 
                        ['leader', 'anchor'], 
                        index=0 if member['role'] == 'leader' else 1,
                        key=f"role_{i}"
                    )
                else:
                    member['role'] = 'child'
                    st.write("Role: Child/Echo")
            
            with col3:
                member['age'] = st.number_input(
                    "Age:", 
                    min_value=0, 
                    max_value=100, 
                    value=member['age'] or (35 if i < num_adults else 10),
                    key=f"age_{i}"
                )
            
            # Individual coherence assessment for adults
            if member['role'] in ['leader', 'anchor']:
                member['coherence_score'] = st.slider(
                    f"Current coherence level (1-10):",
                    min_value=1.0, max_value=10.0, value=member['coherence_score'],
                    step=0.5, key=f"coherence_{i}"
                )
                
                coherence_desc = {
                    (1, 3): "🔴 High stress, frequent overwhelm",
                    (3, 5): "🟡 Struggling but managing", 
                    (5, 7): "🟢 Generally stable",
                    (7, 9): "💚 Very coherent and centered",
                    (9, 10): "✨ Exceptional coherence and flow"
                }
                
                for (min_val, max_val), desc in coherence_desc.items():
                    if min_val <= member['coherence_score'] < max_val:
                        st.caption(desc)
                        break
    
    # Family field preview
    if all(member['name'] for member in st.session_state.family_members):
        st.subheader("🌊 Family Field Preview")
        
        # Calculate overall field metrics
        adult_coherence = [m['coherence_score'] for m in st.session_state.family_members if m['role'] in ['leader', 'anchor']]
        avg_coherence = sum(adult_coherence) / len(adult_coherence) if adult_coherence else 5.0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👥 Family Size", len(st.session_state.family_members))
        
        with col2:
            st.metric("📊 Avg Adult Coherence", f"{avg_coherence:.1f}/10")
        
        with col3:
            leaders = len([m for m in st.session_state.family_members if m['role'] == 'leader'])
            anchors = len([m for m in st.session_state.family_members if m['role'] == 'anchor'])
            st.metric("⚖️ Leader:Anchor Ratio", f"{leaders}:{anchors}")
        
        # Advance progress
        if st.button("✅ Complete Family Profile", type="primary"):
            st.session_state.program_progress = max(st.session_state.program_progress, 1)
            st.success("Family profile created! Move to Field Assessment in the sidebar.")
            st.rerun()

def field_assessment_page():
    """Family field assessment page"""
    st.header("📊 Family Coherence Field Assessment")
    
    if not st.session_state.family_members:
        st.warning("Please create your family profile first.")
        return
    
    st.markdown("""
    Let's assess your current family coherence patterns and identify areas for growth.
    This assessment helps us understand your starting point and customize recommendations.
    """)
    
    # Overall field assessment
    st.subheader("🌊 Overall Family Field")
    
    col1, col2 = st.columns(2)
    
    with col1:
        field_coherence = st.slider(
            "How coherent/stable does your family feel overall?",
            min_value=1.0, max_value=10.0, value=5.0, step=0.5
        )
        
        field_desc = {
            (1, 3): "🔴 Frequent chaos, high conflict, unstable",
            (3, 5): "🟡 Some stability but regular disruptions",
            (5, 7): "🟢 Generally harmonious with occasional bumps",
            (7, 9): "💚 Very stable and supportive environment", 
            (9, 10): "✨ Exceptional coherence and flow"
        }
        
        for (min_val, max_val), desc in field_desc.items():
            if min_val <= field_coherence < max_val:
                st.caption(desc)
                break
    
    with col2:
        communication_quality = st.slider(
            "How would you rate family communication quality?",
            min_value=1.0, max_value=10.0, value=5.0, step=0.5
        )
        
        stress_level = st.slider(
            "Current family stress level:",
            min_value=1.0, max_value=10.0, value=5.0, step=0.5
        )
    
    # Scarcity vs Abundance patterns
    st.subheader("⚖️ Scarcity vs Abundance Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔴 Scarcity Patterns** *(check all that apply)*")
        
        scarcity_patterns = [
            "Competing for attention/love",
            "Rushing through activities", 
            "Fear of not being enough",
            "Hoarding resources/time",
            "Anxiety about the future",
            "Difficulty receiving help",
            "Zero-sum thinking", 
            "Protective/defensive communication"
        ]
        
        family_scarcity = []
        for pattern in scarcity_patterns:
            if st.checkbox(pattern, key=f"scarcity_{pattern}"):
                family_scarcity.append(pattern)
    
    with col2:
        st.markdown("**🟢 Abundance Patterns** *(check all that apply)*")
        
        abundance_patterns = [
            "Spacious family time",
            "Generous with attention", 
            "Celebrating others' success",
            "Trusting in provision",
            "Present-moment awareness",
            "Easy giving and receiving",
            "Collaborative problem-solving",
            "Open, generous communication"
        ]
        
        family_abundance = []
        for pattern in abundance_patterns:
            if st.checkbox(pattern, key=f"abundance_{pattern}"):
                family_abundance.append(pattern)
    
    # Calculate abundance drift
    abundance_score = len(family_abundance)
    scarcity_score = len(family_scarcity) 
    abundance_drift = (abundance_score - scarcity_score) / 8 * 10
    
    # Assessment results
    st.subheader("📈 Assessment Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Field Coherence", f"{field_coherence:.1f}/10")
    
    with col2:
        st.metric("Communication", f"{communication_quality:.1f}/10")
    
    with col3:
        st.metric("Stress Level", f"{stress_level:.1f}/10")
    
    with col4:
        st.metric("Abundance Drift", f"{abundance_drift:+.1f}")
    
    # Visualization
    st.subheader("📊 Assessment Visualization")
    
    # Create radar chart
    categories = ['Field Coherence', 'Communication', 'Low Stress', 'Abundance Drift']
    values = [field_coherence, communication_quality, 10-stress_level, 5+abundance_drift]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current State',
        line_color='#3498db'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        title="Family Field Assessment",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Store assessment data
    st.session_state.current_assessment = {
        'field_coherence': field_coherence,
        'communication_quality': communication_quality,
        'stress_level': stress_level,
        'abundance_drift': abundance_drift,
        'scarcity_patterns': family_scarcity,
        'abundance_patterns': family_abundance,
        'assessment_date': datetime.now().isoformat()
    }
    
    # Recommendations based on assessment
    st.subheader("💡 Immediate Recommendations")
    
    if field_coherence < 5:
        st.warning("🚨 **Priority Focus: Field Stabilization** - Start with basic coherence practices")
    
    if abundance_drift < -2:
        st.error("⚠️ **Priority Focus: Scarcity Pattern Interruption** - Strong scarcity patterns detected")
    
    if abundance_drift > 2:
        st.success("✨ **Opportunity: Abundance Amplification** - Build on your strong foundation")
    
    if communication_quality < 5:
        st.info("🗣️ **Focus Area: Communication Skills** - Work on family dialogue practices")
    
    # Progress advancement
    if st.button("✅ Complete Assessment", type="primary"):
        st.session_state.program_progress = max(st.session_state.program_progress, 2)
        st.success("Assessment completed! Explore the Laws next.")
        st.rerun()

def laws_explorer_page():
    """Interactive laws exploration page"""
    st.header("📚 Laws of Scarcity and Abundance Explorer")
    
    st.markdown("""
    Explore each law and understand how it manifests in family dynamics. 
    Click on any law to dive deeper and reflect on your family's patterns.
    """)
    
    # Law selection
    selected_law = st.selectbox(
        "Select a Law to Explore:",
        [f"Law {i}: {LAWS[i]['title']}" for i in range(1, 6)],
        key="law_selector"
    )
    
    law_num = int(selected_law.split(":")[0].split()[1])
    law = LAWS[law_num]
    
    # Display selected law
    st.markdown(f"""
    <div class="law-card">
        <h3>📜 {law['title']}</h3>
        <p><strong>Core Principle:</strong> {law['core']}</p>
        <p><strong>Family Impact:</strong> {law['family_impact']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Law-specific content and exercises
    tab1, tab2, tab3 = st.tabs(["🤔 Reflection", "🏠 Family Examples", "🛠️ Practical Tools"])
    
    with tab1:
        st.subheader("Reflection Questions")
        
        reflection_questions = {
            1: [
                "What survival fears did you inherit from your family of origin?",
                "How do these fears show up in your parenting or family interactions?",
                "What would change if your children knew they were fundamentally safe?",
                "Where do you create unnecessary survival pressure in your family?"
            ],
            2: [
                "Where do you create artificial scarcity in your family (time, attention, affection)?",
                "How might abundant love feel threatening to your sense of control?",
                "What would happen if your children never had to compete for your love?",
                "Which family 'resources' do you treat as scarce when they're actually abundant?"
            ],
            3: [
                "Do your children feel guilty for having needs or taking up space?",
                "How do you model healthy receiving in your family?",
                "Where do you feel guilty for 'taking' from your family?",
                "How does your family balance individual needs with collective good?"
            ],
            4: [
                "Where do you rush your children's development out of fear?",
                "How do time pressures create scarcity in your family field?",
                "What would slow, spacious family time look like?",
                "Where does 'not enough time' actually mean 'not enough presence'?"
            ],
            5: [
                "How does your family practice unconditional belonging?",
                "Where can family members pause without consequences?",
                "How do you model abundance mindset daily?",
                "What would your family look like if everyone felt truly abundant?"
            ]
        }
        
        for i, question in enumerate(reflection_questions[law_num], 1):
            st.markdown(f"**{i}.** {question}")
            
            # Allow users to save insights
            insight_key = f"insight_{law_num}_{i}"
            insight = st.text_area(f"Your reflection:", key=insight_key, height=80)
            
            if insight and insight not in st.session_state.insights:
                if st.button(f"💾 Save Insight {i}", key=f"save_{law_num}_{i}"):
                    st.session_state.insights.append({
                        'law': law_num,
                        'question': question,
                        'insight': insight,
                        'timestamp': datetime.now().isoformat()
                    })
                    st.success("Insight saved!")
    
    with tab2:
        st.subheader("Family Examples")
        
        family_examples = {
            1: {
                'scarcity': "Parents constantly worry about children's future, creating anxiety around performance and achievement. Children learn to see life as dangerous and competitive.",
                'abundance': "Parents model trust in life's process, helping children develop internal security and confidence in their ability to navigate challenges."
            },
            2: {
                'scarcity': "Love and attention are doled out based on behavior. Children compete for parental approval through achievements or good behavior.",
                'abundance': "Love is given freely and consistently. Children understand their worth isn't tied to performance or behavior."
            },
            3: {
                'scarcity': "Family members feel guilty for having needs. Children learn to minimize their requirements or feel bad for 'being a burden.'",
                'abundance': "Needs are met with generosity. Family members feel comfortable asking for and receiving support."
            },
            4: {
                'scarcity': "Family life is rushed and scheduled. Children are pushed to develop faster, achieve more, and optimize their potential.",
                'abundance': "Family moves at a sustainable pace. Children are allowed to develop naturally with plenty of space for play and discovery."
            },
            5: {
                'scarcity': "Family operates from fear and control. Rules are rigid and based on preventing problems rather than creating joy.",
                'abundance': "Family operates from trust and flexibility. Rules serve love and growth rather than fear and control."
            }
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔴 Scarcity Pattern Example:**")
            st.error(family_examples[law_num]['scarcity'])
        
        with col2:
            st.markdown("**🟢 Abundance Pattern Example:**")
            st.success(family_examples[law_num]['abundance'])
    
    with tab3:
        st.subheader("Practical Tools")
        
        practical_tools = {
            1: [
                "Create family safety rituals - regular affirmations of security and belonging",
                "Practice emotional co-regulation when anxiety arises",
                "Share stories of resilience and growth from your family history",
                "Develop 'good enough' standards instead of perfectionist expectations"
            ],
            2: [
                "Institute 'unconditional love time' where affection isn't tied to behavior",
                "Create abundance practices - notice and celebrate what you have",
                "Eliminate competition between siblings for parental attention",
                "Practice generous attention-giving throughout the day"
            ],
            3: [
                "Normalize asking for help and receiving support in your family",
                "Model healthy boundaries around giving and receiving",
                "Create family practices of mutual care and support",
                "Celebrate when family members meet their own needs well"
            ],
            4: [
                "Build in 'spacious time' - unscheduled, unoptimized family time",
                "Practice presence-based rather than productivity-based family activities",
                "Create slow morning or evening routines",
                "Allow children to move at their own developmental pace"
            ],
            5: [
                "Implement regular gratitude and appreciation practices", 
                "Create generous family policies around mistakes and learning",
                "Practice abundance thinking: 'there's enough for everyone'",
                "Build family rituals that celebrate growth and connection"
            ]
        }
        
        for i, tool in enumerate(practical_tools[law_num], 1):
            st.markdown(f"**{i}.** {tool}")
        
        # Action planning
        st.markdown("---")
        st.subheader("🎯 Choose Your Focus")
        
        selected_tool = st.selectbox(
            f"Which tool from Law {law_num} would you like to implement first?",
            practical_tools[law_num],
            key=f"tool_selector_{law_num}"
        )
        
        if st.button(f"📝 Add to Action Plan", key=f"add_action_{law_num}"):
            action_item = {
                'law': law_num,
                'tool': selected_tool,
                'timestamp': datetime.now().isoformat()
            }
            
            if 'action_items' not in st.session_state:
                st.session_state.action_items = []
            
            st.session_state.action_items.append(action_item)
            st.success(f"Added to your action plan!")
    
    # Progress indicator
    if st.button("✅ Continue to Ritual Builder", type="primary"):
        st.session_state.program_progress = max(st.session_state.program_progress, 3)
        st.success("Laws explored! Build your family rituals next.")

def ritual_builder_page():
    """Ritual builder and customization page"""
    st.header("🎭 Family Ritual Builder")
    
    st.markdown("""
    Select and customize coherence-building rituals for your family. 
    These practices will help you maintain and strengthen your family field over time.
    """)
    
    # Ritual selection interface
    st.subheader("🎯 Available Rituals")
    
    for ritual_key, ritual in RITUALS.items():
        with st.expander(f"{ritual['icon']} {ritual['name']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {ritual['description']}")
                st.markdown(f"**Duration:** {ritual['duration']}")
                
                st.markdown("**Benefits:**")
                for benefit in ritual['benefits']:
                    st.markdown(f"• {benefit}")
            
            with col2:
                interest_level = st.slider(
                    "Interest Level:",
                    min_value=1, max_value=5, value=3,
                    key=f"interest_{ritual_key}"
                )
                
                if interest_level >= 3:
                    if st.button(f"Customize {ritual['name']}", key=f"customize_{ritual_key}"):
                        st.session_state[f"customizing_{ritual_key}"] = True
                        st.rerun()
            
            # Customization interface
            if st.session_state.get(f"customizing_{ritual_key}", False):
                st.markdown("---")
                st.markdown("**🔧 Customize This Ritual**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    frequency = st.selectbox(
                        "Frequency:",
                        ["Daily", "Weekly", "Bi-weekly", "Monthly", "As needed"],
                        key=f"freq_{ritual_key}"
                    )
                
                with col2:
                    time_of_day = st.selectbox(
                        "Best time:",
                        ["Morning", "After school", "Evening", "Before bed", "Flexible"],
                        key=f"time_{ritual_key}"
                    )
                
                with col3:
                    duration_pref = st.selectbox(
                        "Preferred duration:",
                        ["5 minutes", "10 minutes", "15 minutes", "20-30 minutes", "45+ minutes"],
                        key=f"duration_{ritual_key}"
                    )
                
                modifications = st.text_area(
                    "Modifications for your family:",
                    placeholder="Any adjustments needed for your family's specific situation...",
                    key=f"mods_{ritual_key}"
                )
                
                if st.button(f"✅ Add to My Rituals", key=f"add_{ritual_key}"):
                    customized_ritual = {
                        'name': ritual['name'],
                        'original_key': ritual_key,
                        'frequency': frequency,
                        'time_of_day': time_of_day,
                        'duration': duration_pref,
                        'modifications': modifications,
                        'benefits': ritual['benefits'],
                        'icon': ritual['icon']
                    }
                    
                    st.session_state.selected_rituals.append(customized_ritual)
                    st.session_state[f"customizing_{ritual_key}"] = False
                    st.success(f"Added {ritual['name']} to your ritual practice!")
                    st.rerun()
    
    # Selected rituals summary
    if st.session_state.selected_rituals:
        st.subheader("🎯 Your Selected Rituals")
        
        for i, ritual in enumerate(st.session_state.selected_rituals):
            with st.expander(f"{ritual['icon']} {ritual['name']}", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Frequency:** {ritual['frequency']}")
                    st.markdown(f"**Time:** {ritual['time_of_day']}")
                    st.markdown(f"**Duration:** {ritual['duration']}")
                    
                    if ritual['modifications']:
                        st.markdown(f"**Your modifications:** {ritual['modifications']}")
                
                with col2:
                    if st.button(f"Remove", key=f"remove_{i}"):
                        st.session_state.selected_rituals.pop(i)
                        st.rerun()
    
    # Implementation planning
    if st.session_state.selected_rituals:
        st.subheader("📅 Implementation Plan")
        
        st.markdown("**Suggested implementation order:**")
        st.markdown("1. Start with ONE ritual and practice for 2 weeks")
        st.markdown("2. Add a second ritual once the first is established")
        st.markdown("3. Build slowly to avoid overwhelming your family")
        
        primary_ritual = st.selectbox(
            "Which ritual would you like to start with?",
            [r['name'] for r in st.session_state.selected_rituals]
        )
        
        start_date = st.date_input("When will you start?")
        
        if st.button("📅 Set Implementation Plan"):
            st.session_state.implementation_plan = {
                'primary_ritual': primary_ritual,
                'start_date': start_date.isoformat(),
                'all_rituals': st.session_state.selected_rituals
            }
            st.success(f"Implementation plan set! Starting with {primary_ritual} on {start_date}")
    
    # Progress advancement
    if st.button("✅ Complete Ritual Building", type="primary"):
        st.session_state.program_progress = max(st.session_state.program_progress, 4)
        st.success("Rituals configured! View your action plan next.")

def visualization_page():
    """Family field visualization page"""
    st.header("📈 Family Field Visualization")
    
    if not st.session_state.current_assessment:
        st.warning("Please complete your field assessment first.")
        return
    
    assessment = st.session_state.current_assessment
    
    # Current state visualization
    st.subheader("🌊 Current Family Field State")
    
    # Create comprehensive dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        # Coherence gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = assessment['field_coherence'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Field Coherence"},
            delta = {'reference': 5},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': "#3498db"},
                'steps': [
                    {'range': [0, 4], 'color': "#e74c3c"},
                    {'range': [4, 7], 'color': "#f39c12"},
                    {'range': [7, 10], 'color': "#27ae60"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 8
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Abundance vs Scarcity
        abundance_count = len(assessment['abundance_patterns'])
        scarcity_count = len(assessment['scarcity_patterns'])
        
        fig_bar = go.Figure(data=[
            go.Bar(name='Abundance', x=['Patterns'], y=[abundance_count], marker_color='#27ae60'),
            go.Bar(name='Scarcity', x=['Patterns'], y=[scarcity_count], marker_color='#e74c3c')
        ])
        
        fig_bar.update_layout(
            title='Abundance vs Scarcity Patterns',
            barmode='group',
            height=300
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Pattern details
    st.subheader("🔍 Pattern Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if assessment['scarcity_patterns']:
            st.markdown("**🔴 Active Scarcity Patterns:**")
            for pattern in assessment['scarcity_patterns']:
                st.markdown(f"• {pattern}")
        else:
            st.success("🎉 No major scarcity patterns detected!")
    
    with col2:
        if assessment['abundance_patterns']:
            st.markdown("**🟢 Active Abundance Patterns:**")
            for pattern in assessment['abundance_patterns']:
                st.markdown(f"• {pattern}")
        else:
            st.info("💡 Opportunity to develop more abundance patterns")
    
    # Family member coherence (if available)
    if st.session_state.family_members:
        st.subheader("👥 Individual Coherence Levels")
        
        member_data = []
        for member in st.session_state.family_members:
            if member['role'] in ['leader', 'anchor']:
                member_data.append({
                    'Name': member['name'],
                    'Role': member['role'].title(),
                    'Coherence': member['coherence_score']
                })
        
        if member_data:
            df = pd.DataFrame(member_data)
            
            fig_member = px.bar(
                df, x='Name', y='Coherence', color='Role',
                title="Individual Adult Coherence Scores",
                color_discrete_map={'Leader': '#3498db', 'Anchor': '#9b59b6'}
            )
            
            fig_member.update_layout(height=400)
            st.plotly_chart(fig_member, use_container_width=True)
    
    # Progress tracking over time (placeholder for future sessions)
    st.subheader("📊 Progress Tracking")
    st.info("📈 Track your family's progress over time by completing regular assessments!")
    
    # Future session data would be plotted here
    # For now, show example of what tracking could look like
    example_dates = pd.date_range(start='2024-01-01', periods=6, freq='M')
    example_coherence = [4.5, 5.2, 5.8, 6.1, 6.7, 7.2]
    
    fig_progress = px.line(
        x=example_dates, y=example_coherence,
        title="Example: Family Coherence Progress Over Time",
        labels={'x': 'Date', 'y': 'Field Coherence Score'}
    )
    
    fig_progress.update_layout(height=300)
    st.plotly_chart(fig_progress, use_container_width=True)
    
    st.caption("This shows an example of how your family's coherence might improve over time with consistent practice.")

def action_plan_page():
    """Generate personalized action plan"""
    st.header("🎯 Your Personalized Action Plan")
    
    if not st.session_state.current_assessment:
        st.warning("Please complete your assessment first to generate an action plan.")
        return
    
    assessment = st.session_state.current_assessment
    
    # Plan overview
    st.subheader("📋 Action Plan Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Coherence", f"{assessment['field_coherence']:.1f}/10")
    
    with col2:
        st.metric("Abundance Drift", f"{assessment['abundance_drift']:+.1f}")
    
    with col3:
        priority_focus = "Stabilization" if assessment['field_coherence'] < 5 else "Growth"
        st.metric("Priority Focus", priority_focus)
    
    # Specific recommendations
    st.subheader("🎯 Priority Recommendations")
    
    recommendations = []
    
    # Field coherence recommendations
    if assessment['field_coherence'] < 4:
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Field Stabilization',
            'action': 'Implement Daily Coherence Pulse ritual immediately',
            'why': 'Your family field needs basic stabilization before other work can be effective'
        })
    
    # Abundance drift recommendations  
    if assessment['abundance_drift'] < -3:
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Scarcity Pattern Interruption',
            'action': 'Focus on Laws 1-3, practice abundance thinking daily',
            'why': 'Strong scarcity patterns are limiting your family\'s potential'
        })
    elif assessment['abundance_drift'] > 3:
        recommendations.append({
            'priority': 'MEDIUM',
            'area': 'Abundance Amplification', 
            'action': 'Focus on Laws 4-5, share abundance practices with others',
            'why': 'You have a strong foundation to build even greater abundance'
        })
    
    # Communication recommendations
    if assessment['communication_quality'] < 5:
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Communication Improvement',
            'action': 'Implement Weekly Family Meetings with structured dialogue',
            'why': 'Better communication is fundamental to all other family work'
        })
    
    # Stress level recommendations
    if assessment['stress_level'] > 7:
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Stress Reduction',
            'action': 'Create more spacious time, reduce over-scheduling',
            'why': 'High stress prevents coherence and abundance from taking root'
        })
    
    # Display recommendations
    for rec in recommendations:
        priority_color = {'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#27ae60'}
        
        st.markdown(f"""
        <div style="border-left: 4px solid {priority_color[rec['priority']]}; padding: 1rem; margin: 1rem 0; background: #f8f9fa;">
            <h4 style="color: {priority_color[rec['priority']]}; margin: 0;">{rec['priority']} PRIORITY: {rec['area']}</h4>
            <p><strong>Action:</strong> {rec['action']}</p>
            <p><strong>Why:</strong> {rec['why']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Weekly plan
    st.subheader("📅 Your First Week Plan")
    
    week_plan = [
        "Day 1-2: Introduce family to coherence concepts, start Daily Pulse",
        "Day 3-4: Focus on one scarcity pattern, practice abundance thinking",
        "Day 5-6: Implement one new family ritual",
        "Day 7: Family reflection meeting - how did the week go?"
    ]
    
    for day_plan in week_plan:
        st.markdown(f"• {day_plan}")
    
    # Monthly milestones
    st.subheader("🗓️ 30-60-90 Day Milestones")
    
    milestones = {
        "30 Days": [
            "Daily Coherence Pulse established as habit",
            "One scarcity pattern significantly reduced",
            "Family communication improved", 
            "Complete second assessment to track progress"
        ],
        "60 Days": [
            "Two family rituals running smoothly",
            "Children showing more emotional stability",
            "Abundance mindset becoming more natural",
            "Less family stress and conflict"
        ],
        "90 Days": [
            "Family field coherence increased by 2+ points",
            "Family known for supportive, generous culture",
            "Children demonstrating abundance mindset",
            "Ready to mentor other families"
        ]
    }
    
    for period, goals in milestones.items():
        with st.expander(f"🎯 {period} Goals"):
            for goal in goals:
                st.markdown(f"• {goal}")
    
    # Action items from law exploration
    if hasattr(st.session_state, 'action_items') and st.session_state.action_items:
        st.subheader("📝 Your Specific Commitments")
        
        for i, item in enumerate(st.session_state.action_items, 1):
            st.markdown(f"{i}. **Law {item['law']}**: {item['tool']}")
    
    # Selected rituals summary
    if st.session_state.selected_rituals:
        st.subheader("🎭 Your Ritual Practice Plan")
        
        for ritual in st.session_state.selected_rituals:
            st.markdown(f"**{ritual['icon']} {ritual['name']}** - {ritual['frequency']} at {ritual['time_of_day']}")
            if ritual['modifications']:
                st.caption(f"Modifications: {ritual['modifications']}")
    
    # Success tracking
    st.subheader("📊 How to Track Success")
    
    success_metrics = [
        "Family conflicts decrease in frequency and intensity",
        "More laughter and joy in daily family life",
        "Children feel safer expressing their authentic selves",
        "Family members support each other's growth generously",
        "Abundance thinking becomes natural family culture",
        "Other families ask what you're doing differently"
    ]
    
    for metric in success_metrics:
        st.markdown(f"• {metric}")
    
    # Completion
    if st.button("✅ Complete Program", type="primary"):
        st.session_state.program_progress = 5
        st.balloons()
        st.success("🎉 Congratulations! Your Family Coherence Field Program is complete!")

def save_export_page():
    """Save and export session data"""
    st.header("💾 Save & Export Your Progress")
    
    st.markdown("""
    Save your family coherence work and export it for future reference or sharing with family members.
    """)
    
    # Prepare export data
    export_data = {
        'program_info': {
            'completion_date': datetime.now().isoformat(),
            'program_version': '1.0',
            'family_name': st.session_state.family_members[0]['name'] if st.session_state.family_members else 'Unknown'
        },
        'family_profile': st.session_state.family_members,
        'assessment': st.session_state.current_assessment,
        'selected_rituals': st.session_state.selected_rituals,
        'insights': st.session_state.insights,
        'progress': st.session_state.program_progress
    }
    
    # Display summary
    st.subheader("📊 Session Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Family Members", len(st.session_state.family_members))
        st.metric("Rituals Selected", len(st.session_state.selected_rituals))
    
    with col2:
        st.metric("Insights Captured", len(st.session_state.insights))
        st.metric("Program Progress", f"{st.session_state.program_progress}/5")
    
    with col3:
        if st.session_state.current_assessment:
            st.metric("Field Coherence", f"{st.session_state.current_assessment['field_coherence']:.1f}/10")
            st.metric("Abundance Drift", f"{st.session_state.current_assessment['abundance_drift']:+.1f}")
    
    # Export options
    st.subheader("📄 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Download JSON Data", type="primary"):
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="📥 Download Family Coherence Data",
                data=json_str,
                file_name=f"family_coherence_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📝 Generate Report", type="secondary"):
            # Generate human-readable report
            report = f"""
# Family Coherence Field Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Family Profile
- Family Size: {len(st.session_state.family_members)} members
- Adults: {len([m for m in st.session_state.family_members if m['role'] in ['leader', 'anchor']])}
- Children: {len([m for m in st.session_state.family_members if m['role'] == 'child'])}

## Assessment Results
- Field Coherence: {st.session_state.current_assessment.get('field_coherence', 'N/A')}/10
- Abundance Drift: {st.session_state.current_assessment.get('abundance_drift', 'N/A')}
- Communication Quality: {st.session_state.current_assessment.get('communication_quality', 'N/A')}/10

## Selected Rituals
{chr(10).join([f"- {r['name']} ({r['frequency']})" for r in st.session_state.selected_rituals])}

## Key Insights
{chr(10).join([f"- Law {i['law']}: {i['insight'][:100]}..." for i in st.session_state.insights])}

## Next Steps
1. Implement selected rituals consistently
2. Practice abundance mindset daily
3. Regular family field assessments
4. Continue growing family coherence
            """
            
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"family_coherence_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Future access
    st.subheader("🔄 Continue Your Journey")
    
    st.markdown("""
    **Remember:** Family coherence is an ongoing practice, not a one-time achievement.
    
    **Recommended follow-up:**
    - Reassess your family field monthly
    - Adjust rituals based on what's working
    - Deepen your understanding of the laws
    - Share your experience with other families
    """)
    
    if st.button("🔄 Start New Assessment"):
        # Reset for new assessment while keeping family profile
        st.session_state.current_assessment = {}
        st.session_state.program_progress = 1
        st.success("Ready for a new assessment! Your family profile has been preserved.")
        st.rerun()

# Main application
def main():
    """Main application flow"""
    
    # Sidebar navigation
    selected_page = sidebar_navigation()
    
    # Route to appropriate page
    if selected_page == "🏠 Welcome & Overview":
        welcome_page()
    elif selected_page == "👨‍👩‍👧‍👦 Family Profile":
        family_profile_page()
    elif selected_page == "📊 Field Assessment":
        field_assessment_page()
    elif selected_page == "📚 Laws Explorer":
        laws_explorer_page()
    elif selected_page == "🎭 Ritual Builder":
        ritual_builder_page()
    elif selected_page == "📈 Visualization":
        visualization_page()
    elif selected_page == "🎯 Action Plan":
        action_plan_page()
    elif selected_page == "💾 Save & Export":
        save_export_page()

if __name__ == "__main__":
    main()