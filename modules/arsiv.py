import streamlit as st
import pandas as pd

from database import (
    tum_kayitlar_idli,
    kayit_sil,
    tumunu_sil
)


def arsiv_sayfasi():

    st.title("🗂️ Geçmiş İşlemler Arşivi")


    veriler = tum_kayitlar_idli()


    if not veriler:

        st.info(
            "Henüz kayıt bulunmamaktadır."
        )

        return


    df = pd.DataFrame(
        veriler,
        columns=[
            "ID",
            "İşlem Tipi",
            "Miktar",
            "Kategori",
            "Açıklama",
            "Tarih"
        ]
    )


    st.subheader(
        "🔍 Filtreleme"
    )


    col1, col2 = st.columns(2)


    tip = col1.selectbox(
        "İşlem Tipi",
        [
            "Tümü",
            "Gelir",
            "Gider"
        ]
    )


    arama = col2.text_input(
        "Kategori veya açıklama ara"
    )


    filtre = df.copy()


    if tip != "Tümü":

        filtre = filtre[
            filtre["İşlem Tipi"] == tip
        ]


    if arama:

        filtre = filtre[
            filtre["Kategori"]
            .str.contains(
                arama,
                case=False,
                na=False
            )
            |
            filtre["Açıklama"]
            .str.contains(
                arama,
                case=False,
                na=False
            )
        ]


    st.dataframe(
        filtre,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Toplam İşlem",
        len(filtre)
    )


    col2.metric(
        "Gelir",
        f"{filtre[filtre['İşlem Tipi']=='Gelir']['Miktar'].sum():,.0f} TL"
    )


    col3.metric(
        "Gider",
        f"{filtre[filtre['İşlem Tipi']=='Gider']['Miktar'].sum():,.0f} TL"
    )


    st.divider()


    st.subheader(
        "📥 Veri Aktarma"
    )


    st.download_button(
        "CSV İndir",
        filtre.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="muhasebe_arsivi.csv",
        mime="text/csv"
    )


    st.divider()


    st.subheader(
        "🗑️ Kayıt Sil"
    )


    if len(filtre) > 0:

        secilen_id = st.selectbox(
            "Silinecek kayıt ID",
            filtre["ID"]
        )


        if st.button(
            "Seçili Kaydı Sil"
        ):

            kayit_sil(
                int(secilen_id)
            )

            st.success(
                "Kayıt silindi."
            )

            st.rerun()



    st.divider()


    st.subheader(
        "⚠️ Tüm Verileri Sil"
    )


    onay = st.checkbox(
        "Tüm kayıtları silmek istiyorum."
    )


    if onay:

        if st.button(
            "Tümünü Sil"
        ):

            tumunu_sil()

            st.success(
                "Tüm kayıtlar silindi."
            )

            st.rerun()