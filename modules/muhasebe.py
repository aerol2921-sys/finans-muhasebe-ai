import streamlit as st
import pandas as pd
import plotly.express as px
import re

from datetime import datetime

from database import (
    kayit_ekle,
    tum_kayitlar
)

from ai import (
    muhasebe_ayristir,
    finans_analizi
)


def muhasebe_sayfasi():

    st.title("💼 Kıdemli Mali Müşavir & Akıllı Muhasebe Defteri")


    kayitlar = tum_kayitlar()


    toplam_gelir = sum(
        x[1] for x in kayitlar
        if x[0] == "Gelir"
    )

    toplam_gider = sum(
        x[1] for x in kayitlar
        if x[0] == "Gider"
    )

    kalan = toplam_gelir - toplam_gider


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Toplam Gelir",
        f"{toplam_gelir:,.0f} TL"
    )

    col2.metric(
        "📉 Toplam Gider",
        f"{toplam_gider:,.0f} TL"
    )

    col3.metric(
        "💵 Kalan",
        f"{kalan:,.0f} TL"
    )


    st.divider()


    st.subheader(
        "📝 Akıllı Finans Girişi"
    )


    girdi = st.text_area(
        "İşleminizi yazınız:",
        placeholder=
        "Örn: 100000 maaş aldım 65700 borcum var"
    )


    if st.button("Analiz Et ve Kaydet"):


        if girdi:


            # Basit matematik soruları
            sayilar = re.findall(
                r'\d+',
                girdi.replace(".", "")
            )


            if (
                len(sayilar) >= 2
                and (
                    "kalır" in girdi.lower()
                    or "kaldı" in girdi.lower()
                    or "ne kadar" in girdi.lower()
                )
            ):

                sonuc = (
                    int(sayilar[0])
                    -
                    int(sayilar[1])
                )


                st.success(
                    f"💰 Size kalan miktar: {sonuc:,.0f} TL"
                )


            # Muhasebe kaydı
            else:

                with st.spinner(
                    "Finansal veri ayrıştırılıyor..."
                ):

                    try:

                        sonuc = muhasebe_ayristir(
                            girdi
                        )


                        for satir in sonuc.split("\n"):

                            if ":" in satir:

                                parca = satir.split(":")


                                if len(parca) == 3:

                                    tip = parca[0].strip()

                                    miktar = float(
                                        parca[1]
                                        .replace(".","")
                                        .replace(",","")
                                        .strip()
                                    )

                                    kategori = parca[2].strip()


                                    kayit_ekle(
                                        tip,
                                        miktar,
                                        kategori,
                                        girdi,
                                        datetime.now()
                                        .strftime(
                                            "%Y-%m-%d %H:%M"
                                        )
                                    )


                        st.success(
                            "✅ Kayıt başarıyla oluşturuldu."
                        )


                    except Exception as e:

                        st.error(
                            f"Kayıt hatası: {e}"
                        )


            st.divider()


            with st.spinner(
                "AI cevap hazırlıyor..."
            ):

                try:

                    cevap = finans_analizi(
                        girdi
                    )

                    st.info(
                        "🤖 Finans Asistanı"
                    )

                    st.write(
                        cevap
                    )


                except Exception as e:

                    st.error(
                        f"AI Hatası: {e}"
                    )



    # Grafikler

    if kayitlar:


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


        st.subheader(
            "📊 Finans Grafikleri"
        )


        col1, col2 = st.columns(2)


        gider = df[
            df["Tip"] == "Gider"
        ]


        if not gider.empty:

            fig = px.pie(
                gider,
                values="Miktar",
                names="Kategori",
                title="Gider Dağılımı"
            )

            col1.plotly_chart(
                fig,
                use_container_width=True
            )


        fig2 = px.line(
            df,
            x="Tarih",
            y="Miktar",
            color="Tip",
            markers=True,
            title="Nakit Akışı"
        )


        col2.plotly_chart(
            fig2,
            use_container_width=True
        )