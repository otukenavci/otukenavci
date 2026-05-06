import streamlit as st
import pyshorteners
import qrcode
from PIL import Image
from io import BytesIO

# Sekme ayarları, şirkete özel
st.set_page_config(page_title="Teknolus QR & Link", page_icon="🏢")

# --- ŞİRKET LOGOSU KISMI ---
# GitHub'a 'logo.png' adında bir görsel atarsan tam burada çıkacak.
try:
    st.image("logo.png", width=250) # Genişliği 250 yaptık, gözüne büyük/küçük gelirse sayıyı değiştirirsin
except:
    pass # Eğer logoyu henüz yüklemediysen hata vermesin, site çökmeyecek şekilde boş geçsin

st.title("🏢 Teknolus Link & QR Oluşturucu")
st.write("Sadece linki yapıştırın, kısa linki ve QR kodunu anında indirin.")
st.markdown("---")

# Link giriş alanı
uzun_link = st.text_input("🔗 Uzun Linki Buraya Yapıştır:")

if uzun_link:
    try:
        # 1. TinyURL ile Linki Kısaltma
        s = pyshorteners.Shortener()
        kisa_link = s.tinyurl.short(uzun_link)
        
        tinyurl_kodu = kisa_link.split("/")[-1]
        
        st.success("İşlem Başarılı!")
        st.write(f"**Kısa Link:** {kisa_link}")

        # 2. QR Kod Oluşturma
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(uzun_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Ekranda Gösterim
        st.image(img.get_image(), caption=f"Dosya Adı: {tinyurl_kodu}.png", width=200)

        # 3. İndirme Butonu
        st.download_button(
            label="📥 QR Kodu İndir (PNG)",
            data=byte_im,
            file_name=f"{tinyurl_kodu}.png",
            mime="image/png"
        )

    except Exception as e:
        st.error("Usta bir yerde hata oldu, linki kontrol et istersen.")
else:
    st.info("Lütfen dönüştürülecek linki girin.")
