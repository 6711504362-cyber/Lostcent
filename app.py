import streamlit as st
import pandas as pd
from datetime import datetime

# --- การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="OUTLAW LOST & FOUND", page_icon="🕵️", layout="wide")

# --- Custom CSS: สไตล์ขาวดำแบบโจร + ตัวหนังสือสีสวย ---
st.markdown("""
    <style>
    /* พื้นหลังสีดำลึก */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* หัวข้อสไตล์ประกาศจับ */
    .main-title {
        font-family: 'Courier New', Courier, monospace;
        color: #FFD700; /* สีทอง Neon Gold */
        text-align: center;
        text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
        border-bottom: 2px solid #333;
        padding-bottom: 20px;
        letter-spacing: 5px;
    }

    /* การ์ดรายการ */
    .item-card {
        background-color: #111111;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .item-card:hover {
        border-color: #00F2FF; /* สีฟ้า Cyber Blue เมื่อเอาเมาส์วาง */
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }

    /* ตัวหนังสือสีสวยๆ แยกประเภท */
    .text-gold { color: #FFD700; font-weight: bold; }
    .text-blue { color: #00F2FF; }
    .text-red { color: #FF3131; }

    /* ปรับแต่งปุ่ม */
    div.stButton > button {
        background-color: #111;
        color: #FFD700;
        border: 1px solid #FFD700;
        width: 100%;
        border-radius: 0;
        height: 3em;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FFD700;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- ส่วนเก็บข้อมูล (Simulated Database) ---
if 'db' not in st.session_state:
    st.session_state.db = []

# --- ส่วนหัวของเว็บ ---
st.markdown('<h1 class="main-title">WANTED: LOST & FOUND</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#888;'>ศูนย์รวมข้อมูลวัตถุที่หายสาบสูญในเงามืด</p>", unsafe_allow_html=True)

# --- Sidebar: เมนูแจ้งของ ---
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>REGISTER DATA</h2>", unsafe_allow_html=True)
    with st.form("entry_form", clear_on_submit=True):
        type_choice = st.selectbox("สถานะ", ["ของหาย (LOST)", "เก็บได้ (FOUND)"])
        item_name = st.text_input("ชื่อสิ่งของ", placeholder="เช่น นาฬิกาสีดำ...")
        location = st.text_input("พิกัดล่าสุด", placeholder="หน้าบาร์ X, ย่าน Y...")
        contact = st.text_input("ช่องทางติดต่อลับ", placeholder="08x-xxx-xxxx")
        
        submitted = st.form_submit_button("BROADCAST SIGNAL")
        
        if submitted:
            if item_name and location and contact:
                new_entry = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": type_choice,
                    "item": item_name,
                    "loc": location,
                    "contact": contact
                }
                st.session_state.db.insert(0, new_entry)
                st.success("บันทึกข้อมูลเข้าสู่เครือข่ายแล้ว")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# --- ส่วนแสดงผลหลัก ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 class='text-blue'>CURRENT DATABASE</h3>", unsafe_allow_html=True)
    if not st.session_state.db:
        st.info("ยังไม่มีข้อมูลในระบบ...")
    else:
        for entry in st.session_state.db:
            color_class = "text-red" if "LOST" in entry['type'] else "text-gold"
            st.markdown(f"""
                <div class="item-card">
                    <span class="{color_class}" style="font-size:0.8rem;">● {entry['type']}</span>
                    <h4 class="text-gold" style="margin: 10px 0;">{entry['item']}</h4>
                    <p style="margin:0; font-size:0.9rem; color:#ccc;">📍 <b>พิกัด:</b> {entry['loc']}</p>
                    <p style="margin:0; font-size:0.9rem; color:#ccc;">📞 <b>ติดต่อ:</b> {entry['contact']}</p>
                    <p style="text-align:right; font-size:0.7rem; color:#555;">LOGGED: {entry['time']}</p>
                </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 class='text-gold'>STATISTICS</h3>", unsafe_allow_html=True)
    lost_count = len([i for i in st.session_state.db if "LOST" in i['type']])
    found_count = len([i for i in st.session_state.db if "FOUND" in i['type']])
    
    st.metric(label="วัตถุที่สาบสูญ", value=lost_count)
    st.metric(label="วัตถุที่ถูกกู้คืน", value=found_count)
    
    st.markdown("---")
    st.markdown("<p style='color:#555; font-size:0.8rem;'>Disclaimer: ข้อมูลจะถูกลบเมื่อมีการรีเฟรช Server (Demo Version)</p>", unsafe_allow_html=True)
