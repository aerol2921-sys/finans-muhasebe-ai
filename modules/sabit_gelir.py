import streamlit as st
from database import conn, cursor

def sabit_gelir_sayfasi():

    st.title("💼 Sabit Gelirler")

    st.subheader("Yeni Sabit Gelir")

    ad = st.text_input(
        "Gelir Adı",
        value="Brüt Maaş"
    )

    tutar = st.number_input(
        "Tutar (TL)",
        min_value=0.0,
        step=1000.0
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
            INSERT INTO sabit_gelirler
            (ad,tutar,odeme_gunu)
            VALUES(?,?,?)
            """,
            (
                ad,
                tutar,
                gun
            )
        )

        conn.commit()

        st.success("Sabit gelir kaydedildi.")

    st.divider()

    st.subheader("Kayıtlı Sabit Gelirler")

    cursor.execute(
        """
        SELECT id,ad,tutar,odeme_gunu
        FROM sabit_gelirler
        """
    )

    veriler = cursor.fetchall()

    if veriler:

        for satir in veriler:

            st.info(
                f"""
💼 {satir[1]}

Tutar : {satir[2]:,.0f} TL

Ayın {satir[3]}. günü
"""
            )

    else:

        st.warning("Henüz sabit gelir eklenmemiş.")