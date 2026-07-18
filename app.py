import streamlit as st
from groq import Groq
import sqlite3
import re
from datetime import datetime
import pandas as pd

# ==============================================================================
# 1. API VE VERİTABANI BAĞLANTILARI
# ==============================================================================
API_ANAHTARI = ""
client = Groq(api_key=API_ANAHTARI)

conn = sqlite3.connect("muhasebe_defteri.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS islemler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tip TEXT,          
    miktar REAL,       
    kategori TEXT,     
    aciklama TEXT,     
    tarih TEXT         
)
""")
conn.commit()

# ==============================================================================
# 2. WEB SAYFASI GENEL AYARLARI VE TASARIMI
# ==============================================================================
st.set_page_config(page_title="Finans & Muhasebe AI", page_icon="📈", layout="wide")

# Sol menü (Sidebar) üzerinden mod seçimi
st.sidebar.title("🤖 Yapay Zeka Menüsü")
mod = st.sidebar.radio("Çalışma Modunu Seçiniz:", ["📈 Kıdemli Finansal Analist", "💼 Mali Müşavir & Muhasebe Asistanı"])

# Yardımcı Fonksiyonlar
def yapay_zekaya_kategorize_ettir(metin):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Görevin, kullanıcının girdiği muhasebe kaydını okumak ve sadece şu kategorilerden en uygun olan TEK BİR kelimeyi seçip yazmaktır: 'Maaş', 'Kira', 'Fatura', 'Gıda', 'Teknoloji', 'Ulaşım', 'E-Ticaret Satışı', 'Diğer'. Başka hiçbir şey yazma."
                },
                {"role": "user", "content": f"Metin: {metin}"}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content.strip()
    except:
        return "Diğer"

# ==============================================================================
# 3. MOD 1: FİNANSAL ANALİST ARAYÜZÜ
# ==============================================================================
if mod == "📈 Kıdemli Finansal Analist":
    st.title("📈 Kıdemli Finansal Analist ve Piyasa Robotu")
    st.write("Uluslararası standartlarda, canlı verilere dayalı kurumsal piyasa raporları hazırlar.")
    
    varlik = st.text_input("Analiz Edilecek Finansal Varlığı Giriniz (Örn: Altın, Bitcoin, THY):")
    
    if st.button("Kapsamlı Rapor Hazırla"):
        if varlik:
            with st.spinner("Yapay zeka bulut sunucularında analiz ediyor..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen kıdemli bir Piyasa Analistisin. Karşındaki kişiye daima son derece resmi, kurumsal ve kusursuz bir Türkçe ile ('Siz') hitap et. Araya asla yabancı kelimeler karıştırma. Raporunu 'Temel Görünüm', 'Destek/Direnç Seviyeleri' ve 'Yatırımcı Psikolojisi' olarak 3 net başlığa ayır. Sonuna mutlaka 'Yatırım Tavsiyesi Değildir' uyarısı ekle."},
                            {"role": "user", "content": f"Varlık: {varlik}. Lütfen resmi piyasa raporunu kaleme alınız."}
                        ],
                        model="llama-3.3-70b-versatile"
                    )
                    st.success("✨ Rapor Başarıyla Hazırlandı:")
                    st.write(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Sistem Hatası: {e}")
        else:
            st.warning("Lütfen bir varlık ismi giriniz.")

# ==============================================================================
# 4. MOD 2: MUHASEBE ASİSTANI ARAYÜZÜ
# ==============================================================================
else:
    st.title("💼 Kıdemli Mali Müşavir & Akıllı Muhasebe Defteri")
    
    # Veritabanından mevcut verileri çekelim
    cursor.execute("SELECT tip, miktar, kategori, aciklama, tarih FROM islemler")
    kayitlar = cursor.fetchall()
    
    toplam_gelir = sum(row[1] for row in kayitlar if row[0] == "Gelir")
    toplam_gider = sum(row[1] for row in kayitlar if row[0] == "Gider")
    net_durum = toplam_gelir - toplam_gider
    
    # Üst Kısım: Renkli Finansal Kartlar (KPI)
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Toplam Gelir", f"{toplam_gelir:,.2f} TL")
    col2.metric("📉 Toplam Gider", f"{toplam_gider:,.2f} TL")
    if net_durum >= 0:
        col3.metric("🟩 Net Kasa Durumu (Kâr)", f"{net_durum:,.2f} TL")
    else:
        col3.metric("🟥 Net Kasa Durumu (Zarar)", f"{net_durum:,.2f} TL")
        
    st.markdown("---")
    
    # Giriş Alanı: Harcama veya Gelir Ekleme Kutusu
    st.subheader("📝 Akıllı İşlem Girişi ve Matematiksel Çözüm")
    girdi = st.text_area("İşlem verisi girin veya matematik problemi sorun:", placeholder="Örn: Bugün ofis kirası için 15000 tl ödedim VEYA x**2 - 9 = 0 denklemini çöz")
    
    if st.button("Veriyi İşle ve Analiz Et"):
        if girdi:
            # Gelir / Gider Giriş Analizi
            if any(k in girdi.lower() for k in ["gelir", "gider", "kazandım", "ödedim", "harcadım", "geldi"]):
                rakamlar = re.findall(r'\d+', girdi)
                if rakamlar:
                    miktar = float(rakamlar[0])
                    tip = "Gider" if any(k in girdi.lower() for k in ["gider", "ödedim", "harcadım"]) else "Gelir"
                    
                    with st.spinner("Yapay zeka kategorilendiriyor..."):
                        kategori = yapay_zekaya_kategorize_ettir(girdi)
                        tarih_su_an = datetime.now().strftime("%Y-%m-%d %H:%M")
                        cursor.execute("INSERT INTO islemler (tip, miktar, kategori, aciklama, tarih) VALUES (?, ?, ?, ?, ?)",
                                       (tip, miktar, kategori, girdi, tarih_su_an))
                        conn.commit()
                    st.success(f"✅ Başarıyla Kaydedildi: {miktar} TL {tip} olarak '{kategori}' kategorisine işlendi! Sayfayı yenileyebilirsiniz.")
                else:
                    st.warning("Cümlenin içinde sayısal bir miktar bulunamadı.")
            
            # Normal Yapay Zeka Muhasebe / Matematik Yanıtı
            with st.spinner("Mali müşavir analiz raporu hazırlıyor..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen uluslararası standartlara hakim, resmi ve entelektüel bir Kıdemli Mali Müşavir ve Matematik Profesörüsün. Kullanıcıya daima resmi bir Türkçe ile ('Siz') hitap et. Dil sızıntısı yapma, araya asla İngilizce veya İspanyolca (empresa, company vb.) kelimeler karıştırma. Matematiksel problemleri adım adım akademik ciddiyetle çöz."},
                            {"role": "user", "content": f"Soru/Veri: {girdi}. Lütfen kurumsal dilde yanıtlayınız."}
                        ],
                        model="llama-3.3-70b-versatile"
                    )
                    st.info("✨ Mali Müşavir ve Profesör Analizi:")
                    st.write(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Hata: {e}")
                    
    st.markdown("---")
    
    # Alt Kısım: Veritabanı Tablosu Gösterimi
    st.subheader("📊 Kayıtlı Muhasebe Defteri Tablosu")
    if kayitlar:
        df = pd.DataFrame(kayitlar, columns=["İşlem Tipi", "Miktar (TL)", "Kategori", "Açıklama", "Tarih"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Defterinizde henüz kayıtlı bir işlem bulunmamaktadır.")
