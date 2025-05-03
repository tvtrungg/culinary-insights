import streamlit as st

def inject_css():
    st.markdown("""
    <style>
        table {
            width: 100% !important;
            table-layout: auto;
        }
        
        section.stMain > div {
            max-width: 90% !important;
        }
                
        .st-emotion-cache-1gb1rig:has(a[href$="/Aspects"]),
        a[data-testid="stSidebarNavLink"][href$="/Aspects"] {
            pointer-events: none;         
            cursor: default;              
            font-weight: normal !important;            
            opacity: 0.8;
            position: relative;
        }

        a[data-testid="stSidebarNavLink"][href$="/Aspects"]::before {
            content: "";
            position: absolute;
            bottom: 0px;
            left: 0;
            width: 100%;
            height: 1px;
            background-color: #999;
            opacity: 0.6;
        }

        a[data-testid="stSidebarNavLink"][href$="/Aspects"]:hover {
            background-color: transparent !important;
            color: #999 !important;
        }
                
        a[data-testid="stSidebarNavLink"][href$="/Cultural"],
        a[data-testid="stSidebarNavLink"][href$="/Economic"],
        a[data-testid="stSidebarNavLink"][href$="/Health"],
        a[data-testid="stSidebarNavLink"][href$="/Environment"] {
            margin-left: 40px;
            
        }

    </style>
    """, unsafe_allow_html=True)
