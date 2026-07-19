import streamlit as st
from database import conn, cursor


def sabit_gider_sayfasi():

    st.title("🏠 Sabit Giderler")

    st.subheader("Yeni Sabit Gider Ekle")

    ad = st.text_input(
        "Gider Adı",
        placeholder="Örn: Kira"
    )

    kategori = st.selectbox(
        "Kategori",
        [
            "Kira",
            "Kredi",
            "Fatura",
            "Abonelik",
            "Diğer"
        ]
    )

    tutar = st.number_input(
        "Tutar (TL)",
        min_value=0.0,
        step=500.0
    )

    gun = st.number_input(
        "Ödeme Günü",
        min_value=1,
        max_value=31,
        value=1
    )


    if st.button("Kaydet"):

        cursor.execute(
            """
            INSERT INTO sabit_giderler
            (ad,kategori,tutar,odeme_gunu)
            VALUES(?,?,?,?)
            """,
            (
                ad,
                kategori,
                tutar,
                gun
            )
        )

        conn.commit()

        st.success("Sabit gider kaydedildi.")


    st.divider()

    st.subheader("Kayıtlı Sabit Giderler")


    cursor.execute(
        """
        SELECT id,ad,kategori,tutar,odeme_gunu
        FROM sabit_giderler
        """
    )

    veriler = cursor.fetchall()


    toplam = 0


    if veriler:

        for gider in veriler:

            toplam += gider[3]

            st.warning(
                f"""
🏠 {gider[1]}

Kategori:
{gider[2]}

Tutar:
{gider[3]:,.0f} TL

Ödeme günü:
Ayın {gider[4]}. günü
"""
            )


        st.divider()

        st.metric(
            "Aylık Sabit Gider Toplamı",
            f"{toplam:,.0f} TL"
        )


    else:

        st.info("Henüz sabit gider eklenmemiş.")