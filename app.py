import streamlit as st
from modules.sabit_giderler import sabit_gider_sayfasi
from modules.sabit_gelir import sabit_gelir_sayfasi
from modules.finans import finans_sayfasi
from modules.muhasebe import muhasebe_sayfasi
from modules.arsiv import arsiv_sayfasi
from modules.analiz import anormal_harcama_sayfasi


st.set_page_config(
    page_title="Finans & Muhasebe AI",
    page_icon="📈",
    layout="wide"
)

st.sidebar.title("🤖 Yapay Zeka Menüsü")

mod = st.sidebar.radio(
    "Çalışma Modunu Seçiniz:",
    [
        "📈 Kıdemli Finansal Analist",
        "💼 Mali Müşavir & Akıllı Muhasebe",
        "🗂️ Geçmiş İşlemler Arşivi",
        "🕵️ Harcama Dedektifi",
        "💼 Sabit Gelirler"
        "🏠 Sabit Giderler",
    ]
    
    
)

if mod == "📈 Kıdemli Finansal Analist":
    finans_sayfasi()

elif mod == "💼 Mali Müşavir & Akıllı Muhasebe":
    muhasebe_sayfasi()

elif mod == "🗂️ Geçmiş İşlemler Arşivi":
    arsiv_sayfasi()

elif mod == "🕵️ Harcama Dedektifi":
    anormal_harcama_sayfasi()

elif mod == "💼 Sabit Gelirler":
    sabit_gelir_sayfasi()
elif mod == "🏠 Sabit Giderler":
    sabit_gider_sayfasi()
