import streamlit as st
import pandas as pd

from database import tum_kayitlar


def anormal_harcama_sayfasi():

    st.title("🕵️ Anormal Harcama Dedektifi")

    kayitlar = tum_kayitlar()

    if not kayitlar:
        st.info("Analiz için henüz yeterli finansal kayıt bulunmuyor.")
        return


    df = pd.DataFrame(
        kayitlar,
        columns=[
            "Tip",
            "Miktar",
            "Kategori",
            "Açıklama",
            "Tarih"
        ]
    )


    giderler = df[
        df["Tip"] == "Gider"
    ]


    if giderler.empty:

        st.info(
            "Henüz gider kaydı bulunmuyor."
        )

        return


    st.subheader(
        "📊 Harcama Kontrolü"
    )


    kategori_analiz = (
        giderler
        .groupby("Kategori")["Miktar"]
        .sum()
        .reset_index()
    )


    ortalama = (
        kategori_analiz["Miktar"]
        .mean()
    )


    for _, satir in kategori_analiz.iterrows():

        kategori = satir["Kategori"]
        miktar = satir["Miktar"]


        artis = (
            (miktar - ortalama)
            /
            ortalama
            *
            100
        )


        if artis > 50:

            st.warning(
                f"""
                ⚠️ {kategori} harcamanız yüksek görünüyor.

                Toplam:
                {miktar:,.0f} TL

                Ortalama kategori harcamasından:
                %{artis:.0f} daha fazla.
                """
            )


    st.subheader(
        "📈 Harcama Dağılımı"
    )


    st.bar_chart(
        kategori_analiz.set_index(
            "Kategori"
        )
    )