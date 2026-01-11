import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- KONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Bencke & Partners | Kundeportal",
    page_icon="Bd",
    layout="wide"
)

# Custom CSS for at matche Bencke & Partners identitet (Mørkeblå/Guld/Hvid)
st.markdown("""
<style>
    /* Hovedfarver */
    .stApp {
        background-color: #f8f9fa;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0E1117;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* Overskrifter */
    h1, h2, h3 {
        color: #0E1117;
        font-family: 'serif';
    }
    /* Faner */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 4px;
        color: #0E1117;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .stTabs [aria-selected="true"] {
        background-color: #0E1117 !important;
        color: #ffffff !important;
    }
    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 5px solid #C5A065; /* Guld accent */
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE & DUMMY DATA ---
# Vi simulerer databasen her, da vi ikke har en rigtig backend endnu.
if 'data_initialized' not in st.session_state:
    # 1. Kunder
    st.session_state.company_name = "Tech Solutions A/S"
    st.session_state.user_name = "Anders Jensen (CEO)"

    # 2. Opgaver (Tasks)
    st.session_state.tasks = [
        {"id": 101, "title": "Group CFO", "status": "Active", "phase": "Rekruttering", "created": "2024-10-01"},
        {"id": 102, "title": "Financial Controller", "status": "Active", "phase": "Annoncering", "created": "2024-11-15"}
    ]

    # 3. Kandidater (Candidates) - Pulje af profiler
    # Færdigheder og data er tilpasset CFO/Controller segmentet
    candidates_pool = [
        {"id": 1, "name": "Henrik Nielsen", "title": "CFO", "exp": "15 år", "skills": ["M&A", "IPO", "Change Mgmt"]},
        {"id": 2, "name": "Maria Svendsen", "title": "Finance Manager", "exp": "8 år", "skills": ["Reporting", "Navision", "Team Lead"]},
        {"id": 3, "name": "Lars Boje", "title": "Group Controller", "exp": "10 år", "skills": ["IFRS", "Compliance", "Excel Expert"]},
        {"id": 4, "name": "Sophie Madsen", "title": "CFO", "exp": "12 år", "skills": ["Strategy", "Stakeholder Mgmt", "BI"]},
        {"id": 5, "name": "Christian Friis", "title": "Senior Controller", "exp": "6 år", "skills": ["SAP", "Month-end", "Auditing"]},
    ]
    st.session_state.candidates = {c["id"]: c for c in candidates_pool}

    # 4. Task_Candidates (Junction Table) - KRITISK LOGIK 
    # Her linker vi kandidater til opgaver med en specifik status og score.
    # Status flow: raw -> screened -> presented_to_customer -> interviewed
    st.session_state.task_candidates = [
        # Kandidater til "Group CFO" (Opgave 101)
        {"task_id": 101, "candidate_id": 1, "status": "presented_to_customer", "match_score": 92, "consultant_note": "Stærk strategisk profil."},
        {"task_id": 101, "candidate_id": 4, "status": "presented_to_customer", "match_score": 88, "consultant_note": "Godt kulturelt match, stærk på drift."},
        {"task_id": 101, "candidate_id": 3, "status": "screened", "match_score": 75, "consultant_note": "Endnu ikke præsenteret for kunde."}, # Skal IKKE vises

        # Kandidater til "Financial Controller" (Opgave 102) - Stadig tidligt i forløbet
        {"task_id": 102, "candidate_id": 2, "status": "presented_to_customer", "match_score": 95, "consultant_note": "Perfekt match på Navision erfaring."},
        {"task_id": 102, "candidate_id": 5, "status": "interviewed", "match_score": 82, "consultant_note": "Solid faglighed, men ung."},
    ]

    # 5. Dokumenter og Annoncer (Mock data)
    st.session_state.approvals = {
        101: {"job_profile": True, "ad_text": True},
        102: {"job_profile": True, "ad_text": False}
    }

    st.session_state.data_initialized = True

# --- SIDEBAR ---
with st.sidebar:
    # Forsøg at vise logo, ellers vis tekst
    try:
        st.image("Bencke-Partners logo.jpg", use_container_width=True)
    except:
        st.markdown("### BENCKE & PARTNERS")
        st.caption("Recruitment | Search | Selection")
    
    st.markdown("---")
    menu = st.radio("Navigation", ["Dashboard", "Mine Opgaver", "Vidensbank"])
    
    st.markdown("---")
    st.info(f"Logget ind som:\n**{st.session_state.company_name}**\n{st.session_state.user_name}")

# --- HOVEDINDHOLD ---

# 1. DASHBOARD VIEW
if menu == "Dashboard":
    st.title(f"Velkommen, {st.session_state.user_name.split()[0]}")
    st.markdown("Her er et overblik over dine igangværende rekrutteringsprocesser.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Aktive Processer", len(st.session_state.tasks))
    with col2:
        # Tæl kandidater der er præsenteret (status >= presented_to_customer)
        visible_candidates = [tc for tc in st.session_state.task_candidates if tc["status"] in ["presented_to_customer", "interviewed", "hired"]]
        st.metric("Kandidater Præsenteret", len(visible_candidates))
    with col3:
        st.metric("Gns. Time-to-Fill", "45 Dage", "+2 dage vs markedet")

    st.markdown("### Seneste Aktiviteter")
    st.info("🔔 **Ny kandidat præsenteret** på opgaven 'Financial Controller' (I går)")
    st.success("✅ **Annoncetekst godkendt** for 'Group CFO' (3 dage siden)")

# 2. MINE OPGAVER VIEW
elif menu == "Mine Opgaver":
    st.title("Mine Opgaver")
    
    # Vælg opgave selector
    task_options = {t["id"]: t["title"] for t in st.session_state.tasks}
    selected_task_id = st.selectbox("Vælg rekrutteringsopgave:", list(task_options.keys()), format_func=lambda x: task_options[x])
    
    # Find valgt opgave objekt
    selected_task = next(t for t in st.session_state.tasks if t["id"] == selected_task_id)
    
    st.markdown(f"### Status: {selected_task['title']}")
    
    # FASE TABS
    tab1, tab2, tab3 = st.tabs(["1. Afdækning & Profil", "2. Annoncering", "3. Kandidater"])
    
    # --- TAB 1: AFDÆKNING ---
    with tab1:
        st.header("Foranalyse & Jobprofil")
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.markdown("""
            **Resumé af Foranalyse:**
            Vi har gennemført workshops med direktionen. Fokus er på en CFO der kan løfte rapporteringen til IFRS standard og agere strategisk sparringspartner.
            
            **Kritiske succesfaktorer:**
            * Implementering af nyt ERP
            * Klargøring til børsnotering (IPO)
            """)
            
            with st.expander("📄 Se Udkast til Jobprofil (PDF Preview)"):
                st.markdown("*Her ville en PDF viewer blive vist*")
                st.image("https://placehold.co/600x400/EEE/31343C?text=Jobprofil+Preview", caption="Jobprofil v1.pdf")
        
        with col_b:
            st.markdown("### Godkendelse")
            is_approved = st.session_state.approvals[selected_task_id]["job_profile"]
            
            if is_approved:
                st.success("✅ Jobprofil er godkendt")
                st.caption("Godkendt d. 10. okt 2024 af Anders Jensen")
            else:
                st.warning("⚠️ Afventer din godkendelse")
                if st.button("Godkend Jobprofil"):
                    st.session_state.approvals[selected_task_id]["job_profile"] = True
                    st.rerun()

    # --- TAB 2: ANNONCERING ---
    with tab2:
        st.header("Annoncemateriale")
        st.markdown("Nedenfor ses udkast til annonceteksten genereret på baggrund af jobprofilen.")
        
        ad_text = st.text_area("Annoncetekst (Redigérbar)", height=300, value=f"""
ERFAREN GROUP CFO TIL {st.session_state.company_name.upper()}

Er du en strategisk stærk økonomiprofil med erfaring fra børsnoterede selskaber? 
{st.session_state.company_name} står overfor en spændende vækstrejse...

Dine ansvarsområder:
- Overordnet ansvar for Finance & IT
- Rapportering til Bestyrelse
- Ledelse af et team på 15 medarbejdere

Vi tilbyder:
En nøglerolle i en markedsledende virksomhed...
        """)
        
        col_ads1, col_ads2 = st.columns([3, 1])
        with col_ads2:
            st.markdown("<br>", unsafe_allow_html=True)
            is_ad_approved = st.session_state.approvals[selected_task_id]["ad_text"]
            
            if is_ad_approved:
                st.success("✅ Annonce godkendt")
            else:
                if st.button("Godkend & Publicér"):
                    st.session_state.approvals[selected_task_id]["ad_text"] = True
                    st.balloons()
                    st.rerun()

    # --- TAB 3: KANDIDATER (REKRUTTERING) ---
    with tab3:
        st.header("Præsenterede Kandidater")
        
        # Filtreringslogik: Hent kandidater fra Junction Table for denne opgave
        # Logik fra Data Relationer 5.1: Kun 'presented_to_customer' eller højere vises [cite: 201, 217]
        task_cands = [
            tc for tc in st.session_state.task_candidates 
            if tc["task_id"] == selected_task_id 
            and tc["status"] in ["presented_to_customer", "interviewed", "hired"]
        ]
        
        if not task_cands:
            st.info("Der er endnu ingen kandidater klar til præsentation i denne fase.")
        else:
            for tc in task_cands:
                cand_profile = st.session_state.candidates[tc["candidate_id"]]
                
                # Kandidat Kort Design
                with st.container():
                    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                    
                    with c1:
                        # Avatar placeholder
                        st.markdown(f"<div style='background-color:#ddd; height:80px; width:80px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;'>{cand_profile['name'][0]}</div>", unsafe_allow_html=True)
                    
                    with c2:
                        st.subheader(cand_profile["name"])
                        st.caption(f"{cand_profile['title']} | Erfaring: {cand_profile['exp']}")
                        # Vis skills som tags
                        tags = " ".join([f"`{s}`" for s in cand_profile["skills"]])
                        st.markdown(tags)
                    
                    with c3:
                        st.metric("Match Score", f"{tc['match_score']}%")
                    
                    with c4:
                        st.markdown(f"**Status:**")
                        status_map = {
                            "presented_to_customer": "🟡 Præsenteret",
                            "interviewed": "🟢 Interviewet",
                            "hired": "🏆 Ansat"
                        }
                        st.markdown(status_map.get(tc['status'], tc['status']))
                        
                    # Detalje expander
                    with st.expander(f"Se vurdering af {cand_profile['name'].split()[0]}"):
                        st.markdown(f"**Konsulentens notater:**")
                        st.info(tc["consultant_note"])
                        
                        st.markdown("**Handlinger:**")
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if st.button(f"Indkald til samtale", key=f"btn_int_{tc['candidate_id']}"):
                                st.toast(f"Invitation sendt til {cand_profile['name']}")
                        with ac2:
                            st.feedback("stars", key=f"rate_{tc['candidate_id']}")
                    
                    st.divider()

# 3. VIDENSBANK VIEW
elif menu == "Vidensbank":
    st.title("Markedsindsigt & Data")
    st.markdown("Baseret på Bencke & Partners data fra lignende rekrutteringer.")
    
    # Dummy chart
    chart_data = pd.DataFrame({
        "Måned": ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun"],
        "Lønniveau Index": [100, 102, 101, 104, 106, 105]
    })
    st.line_chart(chart_data, x="Måned", y="Lønniveau Index")
    st.caption("Udvikling i lønforventninger for CFO-profiler (YTD)")
