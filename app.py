import streamlit as st

from modules.finans import finans_sayfasi
from modules.muhasebe import muhasebe_sayfasi
from modules.arsiv import arsiv_sayfasi

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
        "🗂️ Geçmiş İşlemler Arşivi"
    ]
)


if mod == "📈 Kıdemli Finansal Analist":
    finans_sayfasi()

elif mod == "💼 Mali Müşavir & Akıllı Muhasebe":
    muhasebe_sayfasi()

elif mod == "🗂️ Geçmiş İşlemler Arşivi":
    arsiv_sayfasi()
