import streamlit as st
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

st.sidebar.title("🤖 Yapay Zeka Menüsü")

mod = st.sidebar.radio(
    "Çalışma Modunu Seçiniz:",
    [
        "📈 Kıdemli Finansal Analist",
        "💼 Mali Müşavir & Akıllı Muhasebe",
        "🗂️ Geçmiş İşlemler Arşivi",
        "🕵️ Harcama Dedektifi",
        "💼 Sabit Gelirler"
    ]
)
elif mod == "🕵️ Harcama Dedektifi":
    anormal_harcama_sayfasi()

elif mod == "💼 Sabit Gelirler":
    sabit_gelir_sayfasi()
