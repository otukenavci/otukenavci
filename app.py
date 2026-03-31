import pyshorteners
import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import qrcode
import io
import os
import datetime
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(page_title="Teknolus Muayene Paneli", layout="wide")

# Logo ve Başlık
col_logo, col_text = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image(Image.open("logo.png"), width=150)
with col_text:
    st.title("🛠 Kaynağında Muayene Formu Paneli")
    st.write(f"Tarih: {datetime.date.today().strftime('%d.%m.%Y')}")

st.divider()

# Giriş Formu
with st.form("muayene_formu"):
    st.subheader("📋 Malzeme ve Sipariş Bilgileri")
    c1, c2, c3 = st.columns(3)
    belge_no = c1.text_input("Envanter Belge No")
    tarih = c2.text_input("Tarih (GG.AA.YYYY)", datetime.date.today().strftime("%d.%m.%Y"))
    mal_no = c3.text_input("Malzeme No")
    
    c4, c5, c6 = st.columns(3)
    rev_no = c4.text_input("Rev No")
    mal_aciklama = c4.text_input("Malzeme Açıklaması")
    firma_adi = c5.text_input("Tedarikçi Firma İsmi")
    sip_no = c6.text_input("Sipariş Numarası")

    st.divider()
    st.subheader("📜 Kontrol Belgeleri")
    c7, c8, c9 = st.columns(3)
    seri_no = c7.text_input("Genel Seri No")
    kaplama_coc = c8.text_input("KAPLAMA COC NO")
    boya_coc = c9.text_input("BOYA COC NO")
    
    c10, c11, c12 = st.columns(3)
    kati_film = c10.text_input("KATI FİLM Y. COC NO")
    hammadde_coc = c11.text_input("HAMMALZEME COC NO")
    olcu_no = c12.text_input("Manuel Ölçü Formu No")
    
    test_no = st.text_input("Test Kontrol No")
    paketleme = st.selectbox("Paketleme Kontrolü", ["UYGUN", "UYGUN DEĞİL"])

    st.divider()
    st.subheader("📊 Miktar ve Denetim Sonuçları")
    c13, c14 = st.columns(2)
    parti_mik = c13.text_input("Denetlenen Partideki Miktar")
    ornek_mik = c14.text_input("Örnekleme Miktarı")

    col_u, col_y, col_s, col_i = st.columns(4)
    uygun_mik = col_u.text_input("Uygun Miktar")
    uygun_seri = col_u.text_input("Uygun Seri")
    yeniden_islem_onarim = col_y.text_input("Yeniden İşlem Miktarı")
    yeniden_seri = col_y.text_input("Yeniden İşlem Seri")
    sartli_kabul = col_s.text_input("Şartlı Kabul Miktarı")
    sartli_seri = col_s.text_input("Şartlı Kabul Seri")
    iade_mik = col_i.text_input("İade Miktarı")
    iade_seri = col_i.text_input("İade Seri")

    toplam_sevk_edilebilir_urun = st.text_input("Toplam Sevk Edilebilir Miktar")
    sevk_seri = st.text_input("Sevk Seri No/Lot No")

    st.divider()
    sevk_sonucu = st.text_input("Sevk Sonucu Başlığı")
    aciklamalar = st.text_area("Detaylı Açıklamalar")
    sapma_yetkilisi = st.text_input("Sapma Onayı Veren Yetkili")
    
    yapan = st.text_input("Denetimi Yapan")
    tedarikci_yetkili = st.text_input("Tedarikçi Firma Yetkilisi")
    
    cmm_data = st.text_area("QR Kod İçeriği (CMM Verileri/Seri numaraları)")

    submit = st.form_submit_button("🚀 RAPORU OLUŞTUR")

if submit:
    try:
        doc = DocxTemplate("YENİ KDF FORMU.docx")
        
        # 1. QR Kodu Oluşturma
        qr_path = "temp_qr.png"
        qrcode.make(cmm_data if cmm_data else "N/A").save(qr_path)
        qr_img = InlineImage(doc, qr_path, width=Mm(28))

        # 2. Kısa URL Oluşturma (Eğer girilen veri bir link ise)
        kisa_url = ""
        if cmm_data and (cmm_data.startswith("http://") or cmm_data.startswith("https://")):
            try:
                s = pyshorteners.Shortener()
                kisa_url = s.tinyurl.short(cmm_data)
            except Exception as e:
                kisa_url = "URL kısaltılamadı (Bağlantı hatası)"
        else:
            kisa_url = cmm_data # Eğer girilen veri link değilse düz metin olarak bırak
            
        # 3. Context (Şablona gönderilecek veriler) içine kısa url'yi ekle
        context = {
            'belge_no': belge_no, 'tarih': tarih, 'mal_no': mal_no, 'rev_no': rev_no,
            'mal_aciklama': mal_aciklama, 'firma_adi': firma_adi, 'sip_no': sip_no,
            'seri_no': seri_no, 'kaplama_coc': kaplama_coc, 'boya_coc': boya_coc,
            'kati_film': kati_film, 'hammadde_coc': hammadde_coc, 'olcu_no': olcu_no,
            'test_no': test_no, 'paketleme': paketleme, 'parti_mik': parti_mik,
            'ornek_mik': ornek_mik, 'sevk_sonucu': sevk_sonucu, 'aciklamalar': aciklamalar,
            'sapma_yetkilisi': sapma_yetkilisi, 'uygun_mik': uygun_mik, 'uygun_seri': uygun_seri,
            'yeniden_islem_onarim': yeniden_islem_onarim, 'yeniden_seri': yeniden_seri,
            'sartli_kabul': sartli_kabul, 'sartli_seri': sartli_seri,
            'iade_mik': iade_mik, 'iade_seri': iade_seri,
            'toplam_sevk_edilebilir_urun': toplam_sevk_edilebilir_urun,
            'sevk_seri': sevk_seri, 'yapan': yapan, 'tedarikci_yetkili': tedarikci_yetkili,
            'cmm_qr': qr_img,
            'kisa_url': kisa_url  # <--- YENİ EKLENEN KISIM
        }

        doc.render(context)
        buffer = io.BytesIO()
        doc.save(buffer)
        if os.path.exists(qr_path): os.remove(qr_path)

        st.success("✅ Rapor başarıyla hazırlandı!")
        st.download_button("📥 Word Dosyasını İndir", buffer.getvalue(), f"KDF_RAPOR_{belge_no}.docx")
    except Exception as e:
        st.error(f"Hata: {e}")