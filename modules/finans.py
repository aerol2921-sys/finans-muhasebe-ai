import streamlit as st

from ai import finans_analizi


def finans_sayfasi():

    st.title("📈 Kıdemli Finansal Analist ve Piyasa Robotu")

    st.write(
        "Yapay zekâ destekli finansal değerlendirme sistemi."
    )


    varlik = st.text_input(
        "Analiz edilecek varlık:",
        placeholder="Örn: Bitcoin, Altın, THY"
    )


    if st.button("📊 Analiz Oluştur"):

        if varlik:

            with st.spinner("Analiz hazırlanıyor..."):

                try:

                    cevap = finans_analizi(
                        f"""
                        Varlık: {varlik}

                        Bu varlık hakkında kısa ve anlaşılır
                        finansal değerlendirme yap.
                        """
                    )

                    st.success("Analiz Tamamlandı")
                    st.write(cevap)


                    st.warning(
                        "⚠️ Bu bilgiler yatırım tavsiyesi değildir."
                    )


                except Exception as e:

                    st.error(
                        f"AI Hatası: {e}"
                    )

        else:

            st.warning(
                "Lütfen bir varlık adı giriniz."
            )