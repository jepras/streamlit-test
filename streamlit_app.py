# Construction Site DeepWiki - Enhanced Version
# Multi-page Streamlit app with DeepWiki-style layout, logging, and source citations

import streamlit as st
import pandas as pd
import time
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid

# Page configuration
st.set_page_config(
    page_title="Construction DeepWiki",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"  # No sidebar needed
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('construction_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Custom CSS for DeepWiki-style layout
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    .stHeader {display: none;}
    
    /* Three-column layout */
    .main-container {
        display: flex;
        gap: 20px;
        height: calc(100vh - 100px);
    }
    
    /* Left navigation */
    .left-nav {
        width: 250px;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        overflow-y: auto;
    }
    
    /* Center content */
    .center-content {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Right TOC */
    .right-toc {
        width: 200px;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        overflow-y: auto;
    }
    
    /* Navigation links */
    .nav-link {
        display: block;
        padding: 8px 12px;
        color: #333;
        text-decoration: none;
        border-radius: 4px;
        margin: 2px 0;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .nav-link:hover {
        background-color: #e9ecef;
        color: #0066cc;
    }
    
    .nav-link.active {
        background-color: #0066cc;
        color: white;
    }
    
    /* Floating question box */
    .floating-question {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        border: 2px solid #0066cc;
        border-radius: 25px;
        padding: 15px 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        min-width: 400px;
    }
    
    /* Source citation boxes */
    .source-box {
        background-color: #f8f9fa;
        border-left: 4px solid #0066cc;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    
    /* Log entry styling */
    .log-entry {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 10px;
        margin: 5px 0;
        font-family: monospace;
        font-size: 12px;
    }
    
    .log-info { border-left: 4px solid #17a2b8; }
    .log-warning { border-left: 4px solid #ffc107; }
    .log-error { border-left: 4px solid #dc3545; }
    
    /* Project cards */
    .project-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Mock data with enhanced structure
CONSTRUCTION_SITES = {
    "harbor_bridge": {
        "name": "Harbor Bridge Renovation",
        "location": "Copenhagen Harbor",
        "status": "In Progress",
        "documents": ["Structural Plans", "Safety Protocols", "Material Specs", "Environmental Report"],
        "last_updated": "2025-01-20",
        "progress": 65,
        "sections": {
            "overview": "Project Overview",
            "structural_plans": "Structural Engineering",
            "safety_protocols": "Safety Management",
            "material_specs": "Material Specifications",
            "environmental": "Environmental Impact"
        }
    },
    "office_complex": {
        "name": "Green Office Complex",
        "location": "Ørestad District",
        "status": "Planning",
        "documents": ["Environmental Impact", "Foundation Plans", "HVAC Systems", "Energy Analysis"],
        "last_updated": "2025-01-18",
        "progress": 25,
        "sections": {
            "overview": "Project Overview",
            "foundation": "Foundation Engineering",
            "hvac": "HVAC Systems",
            "environmental": "Environmental Analysis",
            "energy": "Energy Efficiency"
        }
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
- **Total Budget**: 450M DKK
- **Spent to Date**: 292M DKK
- **Remaining**: 158M DKK

## Project Stakeholders
- **Client**: Copenhagen Municipality
- **Main Contractor**: Nordic Infrastructure A/S
- **Engineering**: Ramboll Group
- **Environmental Consultant**: COWI A/S""",

        "structural_plans": """# Structural Engineering Plans

## Foundation Specifications
The bridge foundation requires significant reinforcement to meet modern load standards and extend service life by 75 years.

### Load Requirements
- **Dead Load**: 25,000 tons (permanent structure weight)
- **Live Load**: 15,000 tons (traffic and pedestrians)
- **Wind Load**: 2,500 tons at 200 km/h (design storm)
- **Seismic Rating**: Zone 2 compliance (EU standards)

### Materials Specification
- **Primary Steel**: Grade S355 structural steel with enhanced corrosion resistance
- **Concrete**: C40/50 high-performance concrete with marine additives
- **Reinforcement**: B500B ribbed steel bars, epoxy-coated for marine environment

### Critical Dimensions
- **Main Span**: 120 meters (no intermediate supports)
- **Tower Height**: 85 meters above mean sea level
- **Foundation Depth**: 35 meters below sea floor
- **Clearance**: 45 meters for ship passage

## Engineering Calculations
All structural calculations follow Eurocode standards with Danish National Annexes. Safety factors exceed minimum requirements by 15%.

### Load Distribution Analysis
Foundation load distribution has been analyzed using finite element modeling. Peak stress concentrations occur at tower base connections."""
    }
}

# Mock source data for citations
MOCK_SOURCES = {
    "structural_plans": [
        {
            "document": "Structural_Engineering_Report.pdf",
            "page": 15,
            "excerpt": "The bridge foundation requires a dead load capacity of 25,000 tons with live load capacity of 15,000 tons...",
            "confidence": 0.95,
            "table_ref": "Load Requirements Table 3.2",
            "image_ref": None
        },
        {
            "document": "Foundation_Analysis.pdf", 
            "page": 8,
            "excerpt": "Foundation depth of 35 meters below sea floor provides adequate bearing capacity for design loads...",
            "confidence": 0.92,
            "table_ref": None,
            "image_ref": "Foundation Cross-Section Figure 2.1"
        },
        {
            "document": "Material_Specifications.pdf",
            "page": 22,
            "excerpt": "Grade S355 structural steel with marine-grade corrosion protection coating system...",
            "confidence": 0.88,
            "table_ref": "Steel Grades Table 5.1",
            "image_ref": None
        }
    ]
}

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'overview'
    if 'current_site' not in st.session_state:
        st.session_state.current_site = None
    if 'current_section' not in st.session_state:
        st.session_state.current_section = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {}
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'question_answer_id' not in st.session_state:
        st.session_state.question_answer_id = None
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = {}

def log_action(action: str, details: Dict = None, level: str = "INFO"):
    """Log user actions and system events"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details or {},
        "level": level,
        "session_id": st.session_state.get('session_id', 'unknown'),
        "user_agent": "streamlit_browser"  # In production, get from request headers
    }
    
    # Add to session state logs for UI display
    st.session_state.logs.append(log_entry)
    
    # Keep only last 100 logs in memory
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]
    
    # Log to Python logger (this goes to files/external systems)
    log_message = f"{action} | {json.dumps(details or {})}"
    
    if level == "INFO":
        logger.info(log_message)
    elif level == "WARNING":
        logger.warning(log_message)
    elif level == "ERROR":
        logger.error(log_message)

def navigate_to_site(site_id: str):
    """Navigate to a specific construction site"""
    log_action("navigate_to_site", {"site_id": site_id, "previous_page": st.session_state.current_page})
    st.session_state.current_site = site_id
    st.session_state.current_section = "overview"
    st.session_state.current_page = "site_detail"

def navigate_to_section(section: str):
    """Navigate to a specific section within a site"""
    log_action("navigate_to_section", {
        "section": section, 
        "site_id": st.session_state.current_site,
        "previous_section": st.session_state.current_section
    })
    st.session_state.current_section = section

def extract_table_of_contents(markdown_content: str) -> List[Tuple[str, str]]:
    """Extract table of contents from markdown headers"""
    lines = markdown_content.split('\n')
    toc = []
    
    for line in lines:
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('# ').strip()
            anchor = title.lower().replace(' ', '-').replace('&', '').replace(',', '')
            toc.append((title, anchor, level))
    
    return toc

def mock_rag_query(site_id: str, section: str, query: str) -> Tuple[str, List[Dict]]:
    """Mock RAG pipeline response with sources"""
    log_action("rag_query", {
        "site_id": site_id,
        "section": section, 
        "query": query,
        "query_length": len(query)
    })
    
    time.sleep(2)  # Simulate processing time
    
    # Generate response based on query
    if "load" in query.lower() or "capacity" in query.lower():
        response = """Based on the structural engineering documentation for the Harbor Bridge project, the load requirements are:

**Dead Load Capacity**: 25,000 tons - This represents the permanent weight of the bridge structure itself, including steel framework, concrete decking, and fixed installations.

**Live Load Capacity**: 15,000 tons - This accounts for variable loads including vehicle traffic, pedestrians, and temporary loads during maintenance.

**Wind Load Design**: 2,500 tons at 200 km/h - The bridge is designed to withstand extreme weather conditions including design storm events.

The foundation system extends 35 meters below the sea floor to provide adequate bearing capacity. All calculations follow Eurocode standards with Danish National Annexes, and safety factors exceed minimum requirements by 15%."""
        
        sources = MOCK_SOURCES.get(section, [])
    
    elif "safety" in query.lower():
        response = """The Harbor Bridge project implements comprehensive safety protocols:

**Personal Protective Equipment (PPE)**:
- Level 1: Hard hat, safety boots, high-vis vest (all personnel)
- Level 2: Fall protection harness (work above 2m height)
- Level 3: Marine rescue equipment (work near water)

**Emergency Procedures**:
- Fire Emergency: Evacuation routes marked in red, muster points at safe distance
- Marine Incident: Direct coast guard contact (+45 72 19 60 18)
- Medical Emergency: On-site medic available 24/7 with helicopter landing pad

**Restricted Access Zones**:
- 50-meter radius around crane operations
- Underwater work areas with maritime exclusion
- High-voltage electrical installations (authorized personnel only)"""
        
        sources = [
            {
                "document": "Safety_Management_Plan.pdf",
                "page": 12,
                "excerpt": "All personnel working above 2 meters must use fall protection harness systems...",
                "confidence": 0.94,
                "table_ref": "PPE Requirements Table 4.1",
                "image_ref": None
            }
        ]
    
    else:
        response = f"""Based on the {section.replace('_', ' ')} documentation for the {CONSTRUCTION_SITES[site_id]['name']}, I found relevant information about your query: "{query}".

This response demonstrates how the RAG pipeline would search through your document embeddings, retrieve the most relevant chunks, and generate a contextual answer with proper source citations.

In production, this would include:
- Semantic search through ChromaDB embeddings
- Retrieval of relevant document chunks
- LLM-generated response with source attribution
- Confidence scoring and relevance ranking"""
        
        sources = MOCK_SOURCES.get(section, [])[:2]  # Limit sources for demo
    
    log_action("rag_response_generated", {
        "response_length": len(response),
        "sources_count": len(sources),
        "processing_time": 2.0
    })
    
    return response, sources

def process_uploaded_files(uploaded_files: List, project_name: str) -> str:
    """Process uploaded PDF files for new project"""
    log_action("file_upload_started", {
        "project_name": project_name,
        "file_count": len(uploaded_files),
        "total_size": sum(f.size for f in uploaded_files)
    })
    
    project_id = f"project_{uuid.uuid4().hex[:8]}"
    
    # Simulate processing steps
    processing_steps = [
        "Validating PDF files...",
        "Extracting text and metadata...", 
        "Processing images and tables...",
        "Generating embeddings...",
        "Creating project structure...",
        "Finalizing project setup..."
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, step in enumerate(processing_steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(processing_steps))
        
        log_action("processing_step", {
            "project_id": project_id,
            "step": step,
            "progress": (i + 1) / len(processing_steps)
        })
        
        time.sleep(1)  # Simulate processing time
    
    # Add new project to mock data
    CONSTRUCTION_SITES[project_id] = {
        "name": project_name,
        "location": "User Uploaded",
        "status": "Processing Complete",
        "documents": [f.name for f in uploaded_files],
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "progress": 100,
        "sections": {
            "overview": "Project Overview",
            "structural": "Structural Analysis", 
            "safety": "Safety Documentation",
            "materials": "Material Specifications"
        }
    }
    
    log_action("project_created", {
        "project_id": project_id,
        "project_name": project_name,
        "files_processed": len(uploaded_files)
    })
    
    return project_id

def render_sites_overview():
    """Render the main sites overview page"""
    log_action("page_view", {"page": "sites_overview"})
    
    st.title("🏗️ Construction Sites Overview")
    st.markdown("Select a construction project to explore its documentation and ask questions.")
    
    # New Project Section
    st.markdown("### ➕ Create New Project")
    with st.expander("Upload Construction Documents", expanded=False):
        project_name = st.text_input("Project Name", placeholder="Enter project name...")
        uploaded_files = st.file_uploader(
            "Upload PDF Documents",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload up to 50 PDF files (max 200 pages each)"
        )
        
        if st.button("Create Project", disabled=not (project_name and uploaded_files)):
            log_action("create_project_clicked", {
                "project_name": project_name,
                "file_count": len(uploaded_files)
            })
            
            new_project_id = process_uploaded_files(uploaded_files, project_name)
            st.success(f"✅ Project '{project_name}' created successfully!")
            st.info("Navigate to your new project to start exploring the documentation.")
    
    st.markdown("### 📋 Existing Projects")
    
    # Create project cards
    cols = st.columns(min(len(CONSTRUCTION_SITES), 3))
    
    for idx, (site_id, site_info) in enumerate(CONSTRUCTION_SITES.items()):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <h3>{site_info['name']}</h3>
                    <p><strong>📍 Location:</strong> {site_info['location']}</p>
                    <p><strong>🔄 Status:</strong> {site_info['status']}</p>
                    <p><strong>📅 Updated:</strong> {site_info['last_updated']}</p>
                    <p><strong>📄 Documents:</strong> {len(site_info['documents'])}</p>
                    <div style="margin-top: 10px;">
                        <div style="background-color: #e9ecef; border-radius: 10px; height: 8px;">
                            <div style="background-color: #0066cc; height: 8px; border-radius: 10px; width: {site_info['progress']}%;"></div>
                        </div>
                        <small>Progress: {site_info['progress']}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Explore Project", key=f"nav_{site_id}"):
                    navigate_to_site(site_id)
                    st.rerun()

def render_site_detail():
    """Render individual site detail page with DeepWiki layout"""
    site_id = st.session_state.current_site
    site_info = CONSTRUCTION_SITES[site_id]
    section = st.session_state.current_section
    
    log_action("page_view", {
        "page": "site_detail",
        "site_id": site_id,
        "section": section
    })
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if st.button("← Back to Sites", key="back_btn"):
            log_action("navigation_back", {"from": "site_detail", "to": "overview"})
            st.session_state.current_site = None
            st.session_state.current_page = 'overview'
            st.rerun()
        st.title(f"🏗️ {site_info['name']}")
    
    with col2:
        st.metric("Progress", f"{site_info['progress']}%")
    
    with col3:
        st.metric("Documents", len(site_info['documents']))
    
    # Three-column layout
    col_nav, col_content, col_toc = st.columns([1, 3, 1])
    
    with col_nav:
        st.markdown("### 📚 Sections")
        
        for section_id, section_name in site_info['sections'].items():
            is_current = section == section_id
            
            if is_current:
                st.markdown(f"**📖 {section_name}**")
            else:
                if st.button(f"📄 {section_name}", key=f"sect_{section_id}", use_container_width=True):
                    navigate_to_section(section_id)
                    st.rerun()
    
    with col_content:
        # Main content
        if section in SAMPLE_SECTIONS.get(site_id, {}):
            content = SAMPLE_SECTIONS[site_id][section]
            st.markdown(content)
        else:
            st.info(f"📝 Documentation for {section.replace('_', ' ')} is being processed...")
    
    with col_toc:
        st.markdown("### 📋 Contents")
        
        if section in SAMPLE_SECTIONS.get(site_id, {}):
            content = SAMPLE_SECTIONS[site_id][section]
            toc = extract_table_of_contents(content)
            
            for title, anchor, level in toc:
                indent = "  " * (level - 1)
                st.markdown(f"{indent}• {title}")
    
    # Floating question box (simulated with bottom container)
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 💬 Ask a Question")
        col1, col2 = st.columns([4, 1])
        
        with col1:
            question = st.text_input("", placeholder=f"Ask about {section.replace('_', ' ')}...", key="question_input")
        
        with col2:
            if st.button("Ask", key="ask_btn", use_container_width=True):
                if question:
                    log_action("question_submitted", {
                        "question": question,
                        "site_id": site_id,
                        "section": section
                    })
                    
                    # Generate unique ID for this Q&A
                    qa_id = f"qa_{uuid.uuid4().hex[:8]}"
                    st.session_state.question_answer_id = qa_id
                    st.session_state.current_question = question
                    st.session_state.current_page = 'question_answer'
                    st.rerun()

def render_question_answer():
    """Render question and answer page with sources"""
    site_id = st.session_state.current_site
    site_info = CONSTRUCTION_SITES[site_id]
    section = st.session_state.current_section
    question = st.session_state.current_question
    
    log_action("page_view", {
        "page": "question_answer",
        "site_id": site_id,
        "section": section
    })
    
    # Header with breadcrumb
    if st.button("← Back to Project", key="back_to_project"):
        log_action("navigation_back", {"from": "question_answer", "to": "site_detail"})
        st.session_state.current_page = 'site_detail'
        st.rerun()
    
    st.title(f"💬 Question & Answer")
    st.caption(f"Project: {site_info['name']} • Section: {section.replace('_', ' ').title()}")
    
    # Two-column layout for Q&A and sources
    col_qa, col_sources = st.columns([2, 1])
    
    with col_qa:
        st.markdown("### ❓ Question")
        st.markdown(f"> {question}")
        
        st.markdown("### 🤖 Answer")
        
        with st.spinner("Generating answer..."):
            answer, sources = mock_rag_query(site_id, section, question)
        
        st.markdown(answer)
    
    with col_sources:
        st.markdown("### 📚 Sources")
        
        st.markdown("#### 📄 Documents Referenced")
        for i, source in enumerate(sources):
            with st.expander(f"{source['document']} (p.{source['page']})"):
                st.markdown(f"**Confidence:** {source['confidence']:.1%}")
                st.markdown(f"**Excerpt:** {source['excerpt']}")
                
                if source['table_ref']:
                    st.markdown(f"**📊 Table:** {source['table_ref']}")
                
                if source['image_ref']:
                    st.markdown(f"**🖼️ Image:** {source['image_ref']}")
        
        st.markdown("#### 🔍 Query Details")
        st.markdown(f"**Processing Time:** 2.0s")
        st.markdown(f"**Sources Found:** {len(sources)}")
        st.markdown(f"**Section Context:** {section.replace('_', ' ').title()}")

def render_logging_dashboard():
    """Render logging dashboard to show all tracked events"""
    log_action("page_view", {"page": "logging_dashboard"})
    
    st.title("📊 Logging Dashboard")
    st.markdown("Real-time view of all user interactions and system events")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    total_logs = len(st.session_state.logs)
    info_logs = len([log for log in st.session_state.logs if log['level'] == 'INFO'])
    warning_logs = len([log for log in st.session_state.logs if log['level'] == 'WARNING'])
    error_logs = len([log for log in st.session_state.logs if log['level'] == 'ERROR'])
    
    with col1:
        st.metric("Total Events", total_logs)
    with col2:
        st.metric("Info", info_logs)
    with col3:
        st.metric("Warnings", warning_logs)
    with col4:
        st.metric("Errors", error_logs)
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        log_level_filter = st.selectbox("Filter by Level", ["ALL", "INFO", "WARNING", "ERROR"])
    with col2:
        action_filter = st.selectbox("Filter by Action", ["ALL"] + list(set([log['action'] for log in st.session_state.logs])))
    
    # Log display
    st.markdown("### 📝 Recent Events")
    
    filtered_logs = st.session_state.logs.copy()
    
    if log_level_filter != "ALL":
        filtered_logs = [log for log in filtered_logs if log['level'] == log_level_filter]
    
    if action_filter != "ALL":
        filtered_logs = [log for log in filtered_logs if log['action'] == action_filter]
    
    # Show logs in reverse chronological order
    for log_entry in reversed(filtered_logs[-50:]):  # Show last 50 logs
        level_class = f"log-{log_entry['level'].lower()}"
        
        st.markdown(f"""
        <div class="log-entry {level_class}">
            <strong>{log_entry['timestamp']}</strong> | 
            <span style="color: #0066cc;">{log_entry['level']}</span> | 
            <strong>{log_entry['action']}</strong><br>
            <small>{json.dumps(log_entry['details'], indent=2)}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Export logs
    if st.button("📥 Export Logs as JSON"):
        log_action("export_logs", {"exported_count": len(filtered_logs)})
        
        logs_json = json.dumps(filtered_logs, indent=2)
        st.download_button(
            label="Download logs.json",
            data=logs_json,
            file_name=f"construction_app_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main app logic
def main():
    # Initialize session state FIRST
    init_session_state()
    
    # Then initialize session and generate session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
        log_action("session_started", {"session_id": st.session_state.session_id})
    
    # Navigation menu
    st.markdown("### 🧭 Navigation")
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        if st.button("🏠 Projects Overview", use_container_width=True):
            log_action("navigation", {"to": "overview"})
            st.session_state.current_page = 'overview'
            st.session_state.current_site = None
            st.rerun()
    
    with nav_col2:
        if st.button("📊 Logging Dashboard", use_container_width=True):
            log_action("navigation", {"to": "logging_dashboard"})
            st.session_state.current_page = 'logging_dashboard'
            st.rerun()
    
    with nav_col3:
        if st.session_state.current_site:
            site_name = CONSTRUCTION_SITES[st.session_state.current_site]['name']
            if st.button(f"🏗️ {site_name[:15]}...", use_container_width=True):
                log_action("navigation", {"to": "site_detail"})
                st.session_state.current_page = 'site_detail'
                st.rerun()
    
    with nav_col4:
        if st.session_state.get('question_answer_id'):
            if st.button("💬 Q&A", use_container_width=True):
                log_action("navigation", {"to": "question_answer"})
                st.session_state.current_page = 'question_answer'
                st.rerun()
    
    st.markdown("---")
    
    # Route to appropriate page
    if st.session_state.current_page == 'overview':
        render_sites_overview()
    elif st.session_state.current_page == 'site_detail':
        render_site_detail()
    elif st.session_state.current_page == 'question_answer':
        render_question_answer()
    elif st.session_state.current_page == 'logging_dashboard':
        render_logging_dashboard()

if __name__ == "__main__":
    main()
