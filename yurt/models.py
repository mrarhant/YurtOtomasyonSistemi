from django.db import models
from django.contrib.auth.models import User

class Ogrenci(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    oda_no = models.CharField(max_length=10, verbose_name="Oda Numarası")
    telefon_no = models.CharField(max_length=15, verbose_name="Telefon Numarası", blank=True, null=True)
    depozito_bakiyesi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Depozito Bakiyesi")

    def borcu_var_mi(self):
        return self.fatura_set.filter(durum='odenmedi').exists()

    def __str__(self):
        return f"{self.kullanici.first_name} {self.kullanici.last_name} ({self.oda_no})"

class Fatura(models.Model):
    ODEME_DURUMLARI = [
        ('odenmedi', 'Ödenmedi'),
        ('odendi_online', 'Ödendi (Online)'),
        ('odendi_manuel', 'Ödendi (Elden/Havale)'),
        ('odendi_depozito', 'Ödendi (Depozitodan)'),
    ]

    ogrenci = models.ForeignKey(Ogrenci, on_delete=models.CASCADE, verbose_name="Öğrenci")
    donem = models.CharField(max_length=20, verbose_name="Dönem")
    tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar")
    son_odeme_tarihi = models.DateField(verbose_name="Son Ödeme Tarihi")
    
    durum = models.CharField(max_length=20, choices=ODEME_DURUMLARI, default='odenmedi')
    odeme_tarihi = models.DateTimeField(null=True, blank=True)
    odeme_aciklamasi = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ogrenci.kullanici.username} - {self.donem} - {self.tutar} TL"

class IzinTalebi(models.Model):
    DURUMLAR = [
        ('beklemede', 'Beklemede'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
    ]

    ogrenci = models.ForeignKey(Ogrenci, on_delete=models.CASCADE, verbose_name="Öğrenci")
    baslangic_tarihi = models.DateField(verbose_name="Başlangıç Tarihi")
    bitis_tarihi = models.DateField(verbose_name="Bitiş Tarihi")
    adres = models.TextField(verbose_name="Gidilecek Adres", null=True, blank=True)
    aciklama = models.TextField(verbose_name="Açıklama", null=True, blank=True)
    
    durum = models.CharField(max_length=20, choices=DURUMLAR, default='beklemede')
    yonetici_notu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ogrenci.kullanici.first_name} - {self.durum}"

class Duyuru(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    icerik = models.TextField(verbose_name="İçerik")
    tarih = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.baslik