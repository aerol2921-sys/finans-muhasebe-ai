import streamlit as st
from groq import Groq
import sqlite3
import re
from datetime import datetime
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. API VE VERİTABANI BAĞLANTILARI
# ==============================================================================
API_ANAHTARI = st.secrets["groq_api_key"]
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
# 2. WEB SAYFASI GENEL AYARLARI VE YENİ MENÜ TASARIMI
# ==============================================================================
st.set_page_config(page_title="Finans & Muhasebe AI", page_icon="📈", layout="wide")

st.sidebar.title("🤖 Yapay Zeka Menüsü")
mod = st.sidebar.radio("Çalışma Modunu Seçiniz:", [
    "📈 Kıdemli Finansal Analist", 
    "💼 Mali Müşavir & Akıllı Muhasebe",
    "🗂️ Geçmiş İşlemler Arşivi"
])

def yapay_zeka_bütce_analizcisi(metin):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Görevin, kullanıcının girdiği finansal metni okumak ve içindeki TÜM gelir veya gider işlemlerini ayıklamaktır.
                    
                    KESİN KURALLAR:
                    1. 'vergi', 'kdv', 'ötv', 'stopaj', 'borç' gibi ödemeleri doğrudan Gider tipine bağla.
                    2. 'maaş', 'kazanç', 'hakediş', 'satış', 'brüt' gibi girdileri doğrudan Gelir tipine bağla.
                    3. Miktarları yazarken asla nokta veya virgül kullanma, saf sayı yaz.
                    
                    Yanıtı SADECE şu formatta ver, başka hiçbir açıklama yazma:
                    TIP:MİKTAR:KATEGORİ (Birden fazla işlem varsa alt alta yaz)
                    
                    Kategoriler sadece şunlar olabilir: 'Maaş', 'Kira', 'Fatura', 'Gıda', 'Teknoloji', 'Ulaşım', 'E-Ticaret Satışı', 'Diğer'.
                    Girdi: 'brüt 116000 vergi 16000'
                    Yanıt:
                    Gelir:116000:Maaş
                    Gider:16000:Fatura"""
                },
                {"role": "user", "content": f"Metin: {metin}"}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content.strip()
    except:
        return None

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
elif mod == "💼 Mali Müşavir & Akıllı Muhasebe":
    st.title("💼 Kıdemli Mali Müşavir & Akıllı Muhasebe Defteri")
    
    cursor.execute("SELECT tip, miktar, kategori, aciklama, tarih FROM islemler")
    kayitlar = cursor.fetchall()
    
    toplam_gelir = sum(row[1] for row in kayitlar if row[0] == "Gelir")
    toplam_gider = sum(row[1] for row in kayitlar if row[0] == "Gider")
    net_durum = toplam_gelir - toplam_gider
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Toplam Gelir", f"{toplam_gelir:,.2f} TL")
    col2.metric("📉 Toplam Gider", f"{toplam_gider:,.2f} TL")
    if net_durum >= 0:
        col3.metric("🟩 Net Kasa Durumu (Kâr)", f"{net_durum:,.2f} TL")
    else:
        col3.metric("🟥 Net Kasa Durumu (Zarar)", f"{net_durum:,.2f} TL")
        
    st.markdown("---")
    
    st.subheader("📝 Akıllı İşlem Girişi ve Matematiksel Çözüm")
    girdi = st.text_area("İşlem verisi girin veya vergi/maaş hesabı yaptırın:", placeholder="Örn: brüt 116000 vergi 16000")
    
    if st.button("Veriyi İşle ve Analiz Et"):
        if girdi:
            if any(k in girdi.lower() for k in ["gelir", "gider", "kazandım", "ödedim", "harcadım", "geldi", "borç", "vergi", "maaş", "kdv", "ötv", "brüt"]):
                with st.spinner("Yapay zeka bütçeyi analiz ediyor..."):
                    analiz_sonucu = yapay_zeka_bütce_analizcisi(girdi)
                    if analiz_sonucu:
                        satirlar = analiz_sonucu.split("\n")
                        for satir in satirlar:
                            if ":" in satir:
                                parcalar = satir.split(":")
                                if len(parcalar) == 3:
                                    try:
                                        v_tip = parcalar[0].strip()
                                        temiz_miktar = parcalar[1].strip().replace(".", "").replace(",", "")
                                        v_miktar = float(temiz_miktar)
                                        v_kategori = parcalar[2].strip()
                                        tarih_su_an = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        
                                        cursor.execute("INSERT INTO islemler (tip, miktar, kategori, aciklama, tarih) VALUES (?, ?, ?, ?, ?)",
                                                       (v_tip, v_miktar, v_kategori, girdi, tarih_su_an))
                                        conn.commit()
                                    except:
                                        continue
                        st.success("✅ Finansal kayıtlar başarıyla ayrıştırıldı ve veritabanına işlendi!")
                        st.rerun()
            
            with st.spinner("Mali müşavir analiz raporu hazırlıyor..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen uluslararası standartlara hakim, resmi ve entelektüel bir Kıdemli Mali Müşavirsiniz. Kullanıcıya daima resmi bir Türkçe ile ('Siz') hitap et. Dil sızıntısı yapma, araya asla İngilizce kelimeler karıştırma."},
                            {"role": "user", "content": f"Soru/Veri: {girdi} Lütfen kurumsal dilde hesaplamaları da içerecek şekilde yanıtlayınız."}
                        ],
                        model="llama-3.3-70b-versatile"
                    )
                    st.info("✨ Mali Müşavir ve Profesör Analizi:")
                    st.write(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Hata: {e}")
                    
    st.markdown("---")
    
    if kayitlar:
        df = pd.DataFrame(kayitlar, columns=["İşlem Tipi", "Miktar (TL)", "Kategori", "Açıklama", "Tarih"])
        st.subheader("📊 Canlı Finansal Grafik Analizleri")
        grafik_col1, grafik_col2 = st.columns(2)
        
        gider_df = df[df["İşlem Tipi"] == "Gider"]
        if not gider_df.empty:
            fig_pie = px.pie(gider_df, values="Miktar (TL)", names="Kategori", title="📈 Harcamaların Dağılımı", hole=0.4)
            grafik_col1.plotly_chart(fig_pie, use_container_width=True)
        else:
            grafik_col1.info("Harcama grafiği için henüz bir 'Gider' kaydı bulunmamaktadır.")
            
        df_sorted = df.sort_values(by="Tarih")
        fig_line = px.line(df_sorted, x="Tarih", y="Miktar (TL)", color="İşlem Tipi", title="📉 Nakit Akışı Trendi", markers=True)
        grafik_col2.plotly_chart(fig_line, use_container_width=True)

# ==============================================================================
# 5. MOD 3: GEÇMİŞ İŞLEMLER ARŞİV SEKME TASARIMI
# ==============================================================================
else:
    st.title("🗂️ Geçmiş Muhasebe ve İşlem Kayıtları Arşivi")
    st.write("Veritabanına kaydedilen tüm finansal hareketlerin kurumsal dökümü.")
    
    cursor.execute("SELECT tip, miktar, kategori, aciklama, tarih FROM islemler ORDER BY id DESC")
    arşiv_kayitlar = cursor.fetchall()
    
    if arşiv_kayitlar:
        df_arsiv = pd.DataFrame(arşiv_kayitlar, columns=["İşlem Tipi", "Miktar (TL)", "Kategori", "Açıklama", "Tarih"])
        
 filtre_col1, filtre_col2 = st.columns(2)
        secilen_tip = filtre_col1.selectbox("İşlem Tipine Göre Filtrele:", ["Hepsi", "Gelir", "Gider"])
        secilen_kat = filtre_col2.selectbox("Kategoriye Göre Filtrele:", ["Hepsi", "Maaş", "Kira", "Fatura", "Gıda", "Teknoloji", "Ulaşım", "E-Ticaret Satışı", "Diğer"])
if secilen_tip != "Hepsi":
    df_arsiv = df_arsiv[df_arsiv["İşlem Tipi"] == secilen_tip]
    if secilen_kat != "Hepsi":
        df_arsiv = df_arsiv[df_arsiv["Kategori"] == secilen_kat]
        st.markdown("---")
        st.dataframe(df_arsiv, use_container_width=True)
        st.markdown("---")
        if st.button("🗑️ Tüm Arşivi Temizle"):
            cursor.execute("DELETE FROM islemler")
            conn.commit()
            st.success("Tüm geçmiş veriler başarıyla temizlendi!")
            st.rerun()
        else:
            st.info("Arşivinizde henüz kayıtlı bir işlem bulunmamaktadır.")
