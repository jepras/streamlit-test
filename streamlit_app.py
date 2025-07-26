# Construction Site DeepWiki PoC
# Multi-page Streamlit app with navigation and markdown support

import streamlit as st
import pandas as pd
import time
from datetime import datetime
from typing import Dict, List, Optional
import json

# Page configuration
st.set_page_config(
    page_title="Construction DeepWiki",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mock data for demonstration
CONSTRUCTION_SITES = {
    "harbor_bridge": {
        "name": "Harbor Bridge Renovation",
        "location": "Copenhagen Harbor",
        "status": "In Progress",
        "documents": ["Structural Plans", "Safety Protocols", "Material Specs"],
        "last_updated": "2025-01-20",
        "progress": 65
    },
    "office_complex": {
        "name": "Green Office Complex",
        "location": "Ørestad District",
        "status": "Planning",
        "documents": ["Environmental Impact", "Foundation Plans", "HVAC Systems"],
        "last_updated": "2025-01-18",
        "progress": 25
    },
    "metro_extension": {
        "name": "Metro Line Extension",
        "location": "Amager",
        "status": "Active",
        "documents": ["Tunnel Specs", "Station Designs", "Electrical Plans"],
        "last_updated": "2025-01-22",
        "progress": 80
    }
}

SAMPLE_SECTIONS = {
    "harbor_bridge": {
        "overview": """# Harbor Bridge Renovation Project

## Project Summary
The Harbor Bridge Renovation is a comprehensive infrastructure upgrade project aimed at modernizing the historic Copenhagen Harbor Bridge while preserving its architectural heritage.

### Key Objectives
- Structural reinforcement for increased load capacity
- Integration of modern safety systems
- Environmental sustainability improvements
- Minimal disruption to harbor traffic

### Timeline
- **Start Date**: March 2024
- **Expected Completion**: December 2025
- **Current Phase**: Foundation reinforcement

### Budget Allocation
- Total Budget: 450M DKK
- Spent to Date: 292M DKK
- Remaining: 158M DKK""",

        "structural_plans": """# Structural Engineering Plans

## Foundation Specifications
The bridge foundation requires significant reinforcement to meet modern load standards.

### Load Requirements
- **Dead Load**: 25,000 tons
- **Live Load**: 15,000 tons  
- **Wind Load**: 2,500 tons at 200 km/h
- **Seismic Rating**: Zone 2 compliance

### Materials
- **Primary Steel**: Grade S355 structural steel
- **Concrete**: C40/50 high-performance concrete
- **Reinforcement**: B500B ribbed steel bars

### Critical Measurements
- Main span: 120 meters
- Tower height: 85 meters above sea level
- Foundation depth: 35 meters below sea floor""",

        "safety_protocols": """# Safety Management Plan

## Site Safety Requirements
All personnel must adhere to strict safety protocols due to the marine environment and heavy construction activities.

### Personal Protective Equipment (PPE)
- **Level 1**: Hard hat, safety boots, high-vis vest
- **Level 2**: Fall protection harness (work above 2m)
- **Level 3**: Marine rescue equipment (near water)

### Emergency Procedures
1. **Fire Emergency**: Evacuation routes marked in red
2. **Marine Incident**: Coast guard contact: +45 72 19 60 18
3. **Medical Emergency**: On-site medic available 24/7

### Restricted Areas
- Crane operation zones (50m radius)
- Underwater work areas
- High-voltage electrical installations""",

        "material_specs": """# Material Specifications & Requirements

## Steel Components
All structural steel must meet European standards for marine environments.

### Corrosion Protection
- **Primer**: Zinc-rich epoxy (75 μm)
- **Intermediate**: Epoxy coating (150 μm)
- **Topcoat**: Polyurethane finish (50 μm)
- **Total System**: 275 μm dry film thickness

### Quality Standards
- **Welding**: EN ISO 3834-2 certification required
- **Inspection**: UT testing for all critical welds
- **Documentation**: Full material traceability required

### Delivery Schedule
- Phase 1 Steel: March 2024 (Delivered ✓)
- Phase 2 Steel: July 2024 (Delivered ✓)
- Phase 3 Steel: November 2024 (In Transit)
- Final Phase: February 2025 (Pending)"""
    }
}

# Initialize session state
if 'current_site' not in st.session_state:
    st.session_state.current_site = None
if 'current_section' not in st.session_state:
    st.session_state.current_section = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}
if 'navigation_history' not in st.session_state:
    st.session_state.navigation_history = []

def navigate_to_site(site_id: str):
    """Navigate to a specific construction site"""
    st.session_state.current_site = site_id
    st.session_state.current_section = "overview"
    st.session_state.navigation_history.append(f"site_{site_id}")

def navigate_to_section(section: str):
    """Navigate to a specific section within a site"""
    st.session_state.current_section = section
    st.session_state.navigation_history.append(f"section_{section}")

def mock_rag_query(site_id: str, section: str, query: str) -> str:
    """Mock RAG pipeline response"""
    time.sleep(1)  # Simulate processing time
    
    responses = {
        "structural_plans": {
            "load capacity": "The bridge is designed for a total load capacity of 40,000 tons (25,000 dead load + 15,000 live load). Current safety factor is 2.5x above minimum requirements.",
            "materials": "Primary materials include Grade S355 structural steel with C40/50 high-performance concrete. All steel components have marine-grade corrosion protection.",
            "foundation": "Foundation extends 35 meters below sea floor with reinforced concrete piles. Seismic rating complies with Zone 2 standards."
        },
        "safety_protocols": {
            "emergency": "Emergency procedures include 3 levels: Fire (red evacuation routes), Marine incidents (coast guard +45 72 19 60 18), Medical (24/7 on-site medic).",
            "ppe": "PPE requirements vary by zone: Level 1 (basic), Level 2 (fall protection above 2m), Level 3 (marine rescue equipment near water).",
            "restricted": "Restricted areas include 50m crane operation zones, underwater work areas, and high-voltage electrical installations."
        },
        "material_specs": {
            "steel": "All structural steel meets EN standards with zinc-rich epoxy primer (75μm), epoxy intermediate (150μm), and polyurethane topcoat (50μm).",
            "delivery": "Current delivery status: Phase 1&2 delivered, Phase 3 in transit (Nov 2024), Final phase pending (Feb 2025).",
            "quality": "Quality standards require EN ISO 3834-2 welding certification, UT testing for critical welds, and full material traceability."
        }
    }
    
    # Simple keyword matching for demo
    query_lower = query.lower()
    section_responses = responses.get(section, {})
    
    for keyword, response in section_responses.items():
        if keyword in query_lower:
            return response
    
    return f"Based on the {section.replace('_', ' ')} documentation for {CONSTRUCTION_SITES[site_id]['name']}, I found relevant information. However, this is a demo response. In production, this would use your RAG pipeline to search through the actual document embeddings and return contextual information."

def render_site_overview():
    """Render the main sites overview page"""
    st.title("🏗️ Construction Sites Overview")
    st.markdown("Select a construction project to explore its documentation and ask questions.")
    
    # Create cards for each site
    cols = st.columns(len(CONSTRUCTION_SITES))
    
    for idx, (site_id, site_info) in enumerate(CONSTRUCTION_SITES.items()):
        with cols[idx]:
            with st.container():
                st.markdown(f"### {site_info['name']}")
                st.markdown(f"📍 **Location:** {site_info['location']}")
                st.markdown(f"🔄 **Status:** {site_info['status']}")
                st.markdown(f"📅 **Updated:** {site_info['last_updated']}")
                
                # Progress bar
                st.progress(site_info['progress'] / 100)
                st.caption(f"Progress: {site_info['progress']}%")
                
                # Documents count
                st.markdown(f"📄 **Documents:** {len(site_info['documents'])}")
                
                # Navigation button
                if st.button(f"Explore {site_info['name']}", key=f"nav_{site_id}"):
                    navigate_to_site(site_id)
                    st.rerun()

def render_site_detail():
    """Render individual site detail page"""
    site_id = st.session_state.current_site
    site_info = CONSTRUCTION_SITES[site_id]
    section = st.session_state.current_section
    
    # Header with breadcrumb
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("← Back to Sites", key="back_btn"):
            st.session_state.current_site = None
            st.session_state.current_section = None
            st.rerun()
        
        st.title(f"🏗️ {site_info['name']}")
        st.caption(f"📍 {site_info['location']} • Status: {site_info['status']}")
    
    with col2:
        st.metric("Progress", f"{site_info['progress']}%")
    
    # Create two-column layout
    col_nav, col_content = st.columns([1, 3])
    
    with col_nav:
        st.markdown("### 📚 Sections")
        
        sections = [
            ("overview", "📋 Overview", "Project summary and key information"),
            ("structural_plans", "🏗️ Structural Plans", "Engineering specifications and load requirements"),
            ("safety_protocols", "⚠️ Safety Protocols", "Safety procedures and emergency protocols"),
            ("material_specs", "🔧 Material Specs", "Material requirements and delivery schedules")
        ]
        
        for section_id, section_name, section_desc in sections:
            is_current = section == section_id
            
            # Style current section differently
            if is_current:
                st.markdown(f"**{section_name}**")
                st.caption(section_desc)
                st.markdown("---")
            else:
                if st.button(section_name, key=f"sect_{section_id}"):
                    navigate_to_section(section_id)
                    st.rerun()
                st.caption(section_desc)
    
    with col_content:
        # Main content area
        st.markdown("### 📖 Documentation")
        
        # Display section content
        if section in SAMPLE_SECTIONS.get(site_id, {}):
            content = SAMPLE_SECTIONS[site_id][section]
            st.markdown(content)
        else:
            st.info(f"Documentation for {section.replace('_', ' ')} is being processed...")
        
        st.markdown("---")
        
        # Chat interface for questions
        st.markdown("### 💬 Ask Questions About This Section")
        
        # Initialize chat history for this site/section
        chat_key = f"{site_id}_{section}"
        if chat_key not in st.session_state.chat_history:
            st.session_state.chat_history[chat_key] = []
        
        # Display chat history
        for message in st.session_state.chat_history[chat_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input(f"Ask about {section.replace('_', ' ')}..."):
            # Add user message
            st.session_state.chat_history[chat_key].append({
                "role": "user", 
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Searching through documents..."):
                    response = mock_rag_query(site_id, section, prompt)
                st.markdown(response)
            
            # Add assistant message
            st.session_state.chat_history[chat_key].append({
                "role": "assistant",
                "content": response
            })
            
            st.rerun()

def render_sidebar():
    """Render navigation sidebar"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        if st.session_state.current_site:
            site_info = CONSTRUCTION_SITES[st.session_state.current_site]
            st.markdown(f"**Current Site:**")
            st.markdown(f"{site_info['name']}")
            
            if st.session_state.current_section:
                st.markdown(f"**Section:** {st.session_state.current_section.replace('_', ' ').title()}")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("## 📊 Quick Stats")
        total_sites = len(CONSTRUCTION_SITES)
        active_sites = sum(1 for site in CONSTRUCTION_SITES.values() if site['status'] in ['Active', 'In Progress'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Sites", total_sites)
        with col2:
            st.metric("Active", active_sites)
        
        # Recent activity (mock)
        st.markdown("## 🕐 Recent Activity")
        st.markdown("• Harbor Bridge: Safety update")
        st.markdown("• Metro Extension: New drawings")
        st.markdown("• Office Complex: Material delivery")

# Main app logic
def main():
    render_sidebar()
    
    if st.session_state.current_site is None:
        render_site_overview()
    else:
        render_site_detail()

if __name__ == "__main__":
    main()
