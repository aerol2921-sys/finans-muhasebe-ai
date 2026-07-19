import sqlite3

conn = sqlite3.connect(
    "muhasebe_defteri.db",
    check_same_thread=False
)

cursor = conn.cursor()


def tablo_olustur():
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


def kayit_ekle(tip, miktar, kategori, aciklama, tarih):
    cursor.execute("""
    INSERT INTO islemler
    (tip, miktar, kategori, aciklama, tarih)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        tip,
        miktar,
        kategori,
        aciklama,
        tarih
    ))

    conn.commit()


def tum_kayitlar():
    cursor.execute("""
    SELECT tip, miktar, kategori, aciklama, tarih
    FROM islemler
    ORDER BY tarih DESC
    """)

    return cursor.fetchall()


def tum_kayitlar_idli():
    cursor.execute("""
    SELECT id, tip, miktar, kategori, aciklama, tarih
    FROM islemler
    ORDER BY tarih DESC
    """)

    return cursor.fetchall()


def kayit_sil(id):
    cursor.execute(
        "DELETE FROM islemler WHERE id=?",
        (id,)
    )

    conn.commit()


def tumunu_sil():
    cursor.execute(
        "DELETE FROM islemler"
    )

    conn.commit()


tablo_olustur()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sabit_gelirler(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT,
    tutar REAL,
    odeme_gunu INTEGER
)
""")

conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sabit_giderler(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT,
    kategori TEXT,
    tutar REAL,
    odeme_gunu INTEGER
)
""")

conn.commit()
