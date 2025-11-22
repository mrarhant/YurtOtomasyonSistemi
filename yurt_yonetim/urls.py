from django.contrib import admin
from django.urls import path
from yurt.views import ogrenci_dashboard_api, izin_iste, ana_sayfa, odeme_yap, giris_yap, cikis_yap, yonetici_paneli, ogrenci_yonetimi, ogrenci_sil, izin_durum_guncelle, toplu_fatura_kes, ogrenci_detay




urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Giriş / Çıkış
    path('giris/', giris_yap, name='giris_yap'),
    path('cikis/', cikis_yap, name='cikis_yap'),
    
    # API'ler
    path('api/dashboard-data/', ogrenci_dashboard_api),
    path('api/izin-iste/', izin_iste),
    path('api/odeme-yap/', odeme_yap),
    
    # Patronun Kapısı (Bu satır eksikti veya kaydedilmemişti)
    path('patron/', yonetici_paneli, name='yonetici_paneli'),
    path('patron/ogrenciler/', ogrenci_yonetimi, name='ogrenci_yonetimi'),
    path('patron/ogrenci-sil/<int:id>/', ogrenci_sil, name='ogrenci_sil'),
    path('patron/izin-guncelle/<int:id>/<str:durum>/', izin_durum_guncelle, name='izin_durum_guncelle'),
    path('patron/fatura-kes/', toplu_fatura_kes, name='toplu_fatura_kes'),
    path('patron/ogrenci-detay/<int:id>/', ogrenci_detay, name='ogrenci_detay'),
    
    # Ana Sayfa
    path('', ana_sayfa, name='ana_sayfa'),
]