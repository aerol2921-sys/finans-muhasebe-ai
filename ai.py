import streamlit as st
from groq import Groq


client = Groq(
    api_key=st.secrets["groq_api_key"]
)


def finans_analizi(metin):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": """
                Siz kişisel finans asistanısınız.
                Kullanıcının sorusuna doğrudan cevap verin.
                Gereksiz rapor oluşturmayın.
                Matematik işlemlerini kendiniz yapın.
                Kısa ve anlaşılır cevap verin.
                """
            },
            {
                "role": "user",
                "content": metin
            }
        ]
    )

    return response.choices[0].message.content



def muhasebe_ayristir(metin):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": """
                Finans metnini işlemlere ayır.

                Sadece şu formatta cevap ver:

                Gelir:Miktar:Kategori
                Gider:Miktar:Kategori

                Açıklama yazma.

                Kategoriler:
                Maaş,Kira,Fatura,Gıda,Teknoloji,
                Ulaşım,E-Ticaret Satışı,Diğer
                """
            },
            {
                "role": "user",
                "content": metin
            }
        ]
    )

    return response.choices[0].message.content