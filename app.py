import streamlit as st
import pandas as pd
import time

# --- KONFIGURATION & STYLING (THE "HIGH END" LOOK) ---
st.set_page_config(
    page_title="Bencke & Partners | Client Portal",
    page_icon="Bd",
    layout="wide"
)

# Her injicerer vi avanceret CSS for at overskrive Streamlits standard "look"
st.markdown("""
<style>
    /* 1. Hent Google Fonts der matcher Bencke & Partners stilen */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

    /* 2. Generel App Baggrund */
    .stApp {
        background-color: #f4f6f9; /* Meget lys grå, eksklusiv */
        font-family: 'Lato', sans-serif;
    }

    /* 3. Overskrifter med Serif (Ligner logoet) */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #0E1117;
        font-weight: 700;
    }
    
    /* 4. Sidebar - Mørk Navy */
    section[data-testid="stSidebar"] {
        background-color: #0c1622; /* Dyb Navy */
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* 5. "Kort" Design - Det der får det til at ligne en rigtig app */
    div.stContainer, div.stExpander {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 5px;
        /* box-shadow: 0 4px 6px rgba(0,0,0,0.05);  <- Streamlit containers driller lidt med skygger, men hvid baggrund hjælper */
    }

    /* 6. Metrics (De tre tal i toppen) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 4px solid #C5A065; /* Guld accent */
    }
    div[data-testid="metric-container"] label {
        color: #666;
        font-family: 'Lato', sans-serif;
    }

    /* 7. Knapper (Buttons) - Gør dem mere elegante */
    div.stButton > button {
        background-color: #0E1117;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-family: 'Lato', sans-serif;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #C5A065; /* Guld ved hover */
        color: #000000;
    }

    /* 8. Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid #ddd;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        color: #666;
    }
    .stTabs [aria-selected="true"] {
        color: #0E1117 !important;
        font-weight: bold;
        border-bottom: 3px solid #C5A065 !important; /* Guld streg under valgt fane */
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE & DATA (Beholder logikken intakt) ---
if 'data_initialized' not in st.session_state:
    st.session_state.company_name = "Tech Solutions A/S"
    st.session_state.user_name = "Anders Jensen"
    
    # Opgaver
    st.session_state.tasks = [
        {"id": 101, "title": "Group CFO", "status": "Active", "phase": "Kandidater", "desc": "Strategisk CFO til børsnotering."},
        {"id": 102, "title": "Financial Controller", "status": "Active", "phase": "Annoncering", "desc": "Hands-on controller til driften."}
    ]

    # Kandidater
    candidates_pool = [
        {"id": 1, "name": "Henrik Nielsen", "title": "CFO", "exp": "15 år", "skills": ["M&A", "IPO", "Change Mgmt"]},
        {"id": 2, "name": "Maria Svendsen", "title": "Finance Manager", "exp": "8 år", "skills": ["Reporting", "Navision", "Team Lead"]},
        {"id": 3, "name": "Lars Boje", "title": "Group Controller", "exp": "10 år", "skills": ["IFRS", "Compliance", "Excel Expert"]},
        {"id": 4, "name": "Sophie Madsen", "title": "CFO", "exp": "12 år", "skills": ["Strategy", "Stakeholder Mgmt", "BI"]},
        {"id": 5, "name": "Christian Friis", "title": "Senior Controller", "exp": "6 år", "skills": ["SAP", "Month-end", "Auditing"]},
    ]
    st.session_state.candidates = {c["id"]: c for c in candidates_pool}

    # Junction Logik (Task <-> Candidates)
    st.session_state.task_candidates = [
        {"task_id": 101, "candidate_id": 1, "status": "presented_to_customer", "match_score": 92, "consultant_note": "Stærk strategisk profil. Har prøvet en IPO før."},
        {"task_id": 101, "candidate_id": 4, "status": "presented_to_customer", "match_score": 88, "consultant_note": "Godt kulturelt match, stærk på drift."},
        {"task_id": 102, "candidate_id": 2, "status": "presented_to_customer", "match_score": 95, "consultant_note": "Perfekt match på Navision erfaring."},
    ]
    st.session_state.approvals = {101: True, 102: False}
    st.session_state.data_initialized = True

# --- SIDEBAR ---
with st.sidebar:
    # Logo Placeholder
    try:
        st.image("Bencke-Partners logo.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align: center; color: white;'>BENCKE & PARTNERS</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio("MENU", ["Dashboard", "Mine Opgaver", "Market Insights"], label_visibility="collapsed")
    
    st.markdown("---")
    st.caption("LOGGET IND SOM")
    st.markdown(f"**{st.session_state.user_name}**")
    st.caption(st.session_state.company_name)

# --- HOVEDINDHOLD ---

# 1. DASHBOARD
if menu == "Dashboard":
    st.title("Overblik")
    st.markdown(f"Velkommen tilbage, {st.session_state.user_name.split()[0]}. Her er status på dine rekrutteringer.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics i pæne bokse
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Aktive Processer", len(st.session_state.tasks))
    with col2:
        cands_count = len([c for c in st.session_state.task_candidates if c["status"] == "presented_to_customer"])
        st.metric("Nye Kandidater", cands_count, "Klar til review")
    with col3:
        st.metric("Markeds Index", "104.2", "+2.1% ift. Q3")

    st.markdown("### Seneste nyt")
    # Lave en "Card" lignende container manuelt
    with st.container():
        st.info(f"**Action required:** Du har 1 annonce der afventer godkendelse.")
        st.success(f"**Nyt match:** Vi har uploadet 2 kandidater til stillingen 'Group CFO'.")

# 2. MINE OPGAVER
elif menu == "Mine Opgaver":
    st.title("Mine Opgaver")
    
    # Task Selector
    task_map = {t["id"]: t["title"] for t in st.session_state.tasks}
    selected_id = st.selectbox("Vælg stilling", list(task_map.keys()), format_func=lambda x: task_map[x])
    current_task = next(t for t in st.session_state.tasks if t["id"] == selected_id)

    st.markdown("---")
    
    # FASER
    t1, t2, t3 = st.tabs(["1. Afdækning", "2. Annoncering", "3. Kandidater"])
    
    with t1:
        st.subheader("Jobprofil & Analyse")
        st.markdown(f"Godkendt jobprofil for **{current_task['title']}**.")
        with st.expander("Se detaljeret profil"):
            st.write("Her vises den fulde kompetenceprofil, lederprofil og succeskriterier.")
            st.caption("Dokument ID: 2024-DOC-882")

    with t2:
        st.subheader("Annoncemateriale")
        is_approved = st.session_state.approvals[selected_id]
        
        col_ad1, col_ad2 = st.columns([2,1])
        with col_ad1:
            st.text_area("Annoncetekst", value=f"Vi søger en {current_task['title']} til...", height=200)
        with col_ad2:
            st.markdown("**Status**")
            if is_approved:
                st.success("✅ Publiceret")
            else:
                st.warning("⚠️ Afventer godkendelse")
                if st.button("Godkend Nu"):
                    st.session_state.approvals[selected_id] = True
                    st.rerun()

    with t3:
        st.subheader("Kandidatliste")
        
        cands = [tc for tc in st.session_state.task_candidates if tc["task_id"] == selected_id]
        
        if not cands:
            st.info("Ingen kandidater præsenteret endnu.")
        else:
            for c in cands:
                profile = st.session_state.candidates[c["candidate_id"]]
                
                # CUSTOM CARD DESIGN START
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0; color: #0E1117;">{profile['name']}</h3>
                            <p style="margin: 0; color: #666;">{profile['title']} • {profile['exp']} erfaring</p>
                        </div>
                        <div style="text-align: right;">
                            <h2 style="margin: 0; color: #C5A065;">{c['match_score']}%</h2>
                            <span style="font-size: 0.8em; color: #999;">MATCH SCORE</span>
                        </div>
                    </div>
                    <hr style="margin: 10px 0; border: none; border-top: 1px solid #eee;">
                    <p style="font-style: italic; color: #444;">"{c['consultant_note']}"</p>
                    <div style="margin-top: 10px;">
                        {' '.join([f'<span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; margin-right: 5px;">{s}</span>' for s in profile['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # CUSTOM CARD DESIGN END
                
                # Knapper under kortet
                c_act1, c_act2 = st.columns([1, 4])
                with c_act1:
                    if st.button("Book Interview", key=f"book_{c['candidate_id']}"):
                        st.toast(f"Invitation sendt til {profile['name']}")

# 3. INSIGHTS
elif menu == "Market Insights":
    st.title("Market Insights")
    st.markdown("Realtidsdata fra Bencke & Partners database.")
    
    chart_data = pd.DataFrame({
        "Måned": ["Jan", "Feb", "Mar", "Apr", "Maj"],
        "Aktivitet": [20, 35, 30, 45, 60]
    })
    st.bar_chart(chart_data, x="Måned", y="Aktivitet", color="#C5A065")
