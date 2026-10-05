import pandas as pd
import matplotlib.pyplot as plt

# 1) CSV ve XML dosyalarını oku
csv_df = pd.read_csv("personel.csv")
xml_df = pd.read_xml("personel.xml")

# 2) Dosyaları birleştir
personel = pd.concat([csv_df, xml_df], ignore_index=True)

# 3) Birleştirilen veriyi JSON olarak kaydet
personel.to_json(
    "personel_birlesik.json",
    orient="records",
    force_ascii=False,
    indent=4
)

# 4) Veri temizleme
# Tekrarlanan kayıtları sil
personel = personel.drop_duplicates()

# Gerçek dışı yaşları (18-65 arası dışında kalanları) ortalama yaş ile değiştir
ortalama_yas = int(
    round(
        personel[
            (personel["Yaş"] >= 18) &
            (personel["Yaş"] <= 65)
        ]["Yaş"].mean()
    )
)

personel.loc[
    (personel["Yaş"] < 18) |
    (personel["Yaş"] > 65),
    "Yaş"
] = ortalama_yas

# Eksik cinsiyet bilgisini doldur
personel["Cinsiyet"] = (
    personel["Cinsiyet"]
    .replace("None", pd.NA)
    .fillna("Erkek")
)

# Eksik bölüm bilgisini doldur
personel["Bölüm"] = personel["Bölüm"].fillna("Satış")

# 5) Temiz veriyi JSON olarak kaydet
personel.to_json(
    "personel_temiz.json",
    orient="records",
    force_ascii=False,
    indent=4
)

# 6) Bölümlere göre pasta grafik
plt.figure(figsize=(7, 7))
personel["Bölüm"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Bölümlere Göre Personel Sayısı")
plt.ylabel("")
plt.tight_layout()
plt.savefig("bolum_pasta_grafik.png", dpi=200)
plt.show()

# 7) Kadın ve erkek personel sayısı çubuk grafik
plt.figure(figsize=(6, 4))
personel["Cinsiyet"].value_counts().plot(kind="bar")
plt.title("Kadın ve Erkek Personel Sayısı")
plt.xlabel("Cinsiyet")
plt.ylabel("Personel Sayısı")
plt.tight_layout()
plt.savefig("cinsiyet_cubuk_grafik.png", dpi=200)
plt.show()