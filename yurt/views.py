from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Min, Q  # İstatistik ve Arama için gerekli
from .models import Ogrenci, Fatura, IzinTalebi, Duyuru
import json
import datetime


def giris_yap(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('username')
        sifre = request.POST.get('password')
        
        user = authenticate(request, username=kullanici_adi, password=sifre)
        
        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('yonetici_paneli')
            return redirect('ana_sayfa')
        else:
            return render(request, 'yurt/login.html', {'error': 'Kullanıcı adı veya şifre hatalı!'})
            
    return render(request, 'yurt/login.html')

def cikis_yap(request):
    logout(request)
    return redirect('giris_yap')


@login_required(login_url='giris_yap')
def ana_sayfa(request):

    return render(request, 'yurt/dashboard.html')

@login_required(login_url='giris_yap')
def ogrenci_dashboard_api(request):
    try:
        ogrenci = Ogrenci.objects.get(kullanici=request.user)
        odenmemis_faturalar = Fatura.objects.filter(ogrenci=ogrenci, durum='odenmedi')
        hesaplanan_borc = odenmemis_faturalar.aggregate(Sum('tutar'))['tutar__sum'] or 0
        toplam_borc = float(hesaplanan_borc)
        ilk_son_odeme_tarihi = odenmemis_faturalar.aggregate(Min('son_odeme_tarihi'))['son_odeme_tarihi__min']

        ilk_fatura = odenmemis_faturalar.order_by('son_odeme_tarihi').first()
        odenecek_fatura_id = ilk_fatura.id if ilk_fatura else None

        son_odemeler_query = Fatura.objects.filter(ogrenci=ogrenci, durum__contains='odendi').order_by('-odeme_tarihi')[:5]
        son_odemeler_data = []
        for f in son_odemeler_query:
            son_odemeler_data.append({
                'tarih': f.odeme_tarihi.strftime("%d.%m.%Y") if f.odeme_tarihi else "-",
                'aciklama': f.donem + " Yurt Ücreti",
                'tutar': f.tutar,
                'durum': 'Başarılı'
            })

        izinler_query = IzinTalebi.objects.filter(ogrenci=ogrenci).order_by('-id')[:5]
        izinler_data = []
        for izin in izinler_query:
            gun_sayisi = (izin.bitis_tarihi - izin.baslangic_tarihi).days + 1
            izinler_data.append({
                'aralik': f"{izin.baslangic_tarihi.strftime('%d.%m')} - {izin.bitis_tarihi.strftime('%d.%m.%Y')}",
                'gun': gun_sayisi,
                'sebep': izin.aciklama if izin.aciklama else "Diğer",
                'durum': izin.durum
            })

        son_duyurular = list(Duyuru.objects.all().order_by('-tarih')[:3].values('baslik', 'icerik', 'tarih'))

        return JsonResponse({
            'ad_soyad': ogrenci.kullanici.first_name + " " + ogrenci.kullanici.last_name,
            'toplam_borc': toplam_borc,
            'son_odeme_tarihi': ilk_son_odeme_tarihi.strftime("%d.%m.%Y") if ilk_son_odeme_tarihi else None,
            'odenecek_fatura_id': odenecek_fatura_id,
            'son_odemeler': son_odemeler_data,
            'izinler': izinler_data,
            'duyurular': son_duyurular
        })

    except Ogrenci.DoesNotExist:
        return JsonResponse({'error': 'Öğrenci kaydı yok.'}, status=404)

@csrf_exempt
def odeme_yap(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fatura = Fatura.objects.get(id=data.get('fatura_id'))
            fatura.durum = 'odendi_online'
            fatura.odeme_tarihi = datetime.datetime.now()
            fatura.save()
            return JsonResponse({'mesaj': 'Ödeme Başarılı!'})
        except Exception as e:
            return JsonResponse({'hata': str(e)}, status=400)
    return JsonResponse({'hata': 'Hata'}, status=400)

@csrf_exempt
def izin_iste(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ogrenci = Ogrenci.objects.get(kullanici=request.user)
            IzinTalebi.objects.create(
                ogrenci=ogrenci,
                baslangic_tarihi=data.get('baslangic'),
                bitis_tarihi=data.get('bitis'),
                adres=data.get('adres'),
                aciklama=data.get('aciklama')
            )
            return JsonResponse({'mesaj': 'İzin talebi alındı!'})
        except Exception as e:
            return JsonResponse({'hata': str(e)}, status=400)
    return JsonResponse({'hata': 'Hata'}, status=400)

@login_required(login_url='giris_yap')
def yonetici_paneli(request):
    if not request.user.is_superuser:
        return redirect('ana_sayfa')


    toplam_ogrenci = Ogrenci.objects.count()
    toplam_gelir = Fatura.objects.filter(durum__contains='odendi').aggregate(Sum('tutar'))['tutar__sum'] or 0
    bekleyen_izinler = IzinTalebi.objects.filter(durum='beklemede').count()
    odenmemis_faturalar = Fatura.objects.filter(durum='odenmedi').count()


    son_izinler = IzinTalebi.objects.all().order_by('-id')[:5]
    duyurular = Duyuru.objects.all().order_by('-tarih')

    context = {
        'toplam_ogrenci': toplam_ogrenci,
        'toplam_gelir': toplam_gelir,
        'bekleyen_izinler': bekleyen_izinler,
        'odenmemis_faturalar': odenmemis_faturalar,
        'son_izinler': son_izinler,
        'duyurular': duyurular
    }
    
    return render(request, 'yurt/admin_dashboard.html', context)

@login_required(login_url='giris_yap')
def ogrenci_yonetimi(request):
    if not request.user.is_superuser:
        return redirect('ana_sayfa')

    if request.method == 'POST':
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        kullanici_adi = request.POST.get('kullanici_adi')
        sifre = request.POST.get('sifre')
        oda_no = request.POST.get('oda_no')
        depozito = request.POST.get('depozito')

        yeni_user = User.objects.create_user(username=kullanici_adi, password=sifre, first_name=ad, last_name=soyad)
        Ogrenci.objects.create(kullanici=yeni_user, oda_no=oda_no, depozito_bakiyesi=depozito)
        return redirect('ogrenci_yonetimi')

    arama_kelimesi = request.GET.get('q')
    if arama_kelimesi:
        ogrenciler = Ogrenci.objects.filter(
            Q(kullanici__first_name__icontains=arama_kelimesi) | 
            Q(kullanici__last_name__icontains=arama_kelimesi) |
            Q(oda_no__icontains=arama_kelimesi)
        ).order_by('-id')
    else:
        ogrenciler = Ogrenci.objects.all().order_by('-id')
        
    return render(request, 'yurt/admin_students.html', {'ogrenciler': ogrenciler})

@login_required(login_url='giris_yap')
def ogrenci_sil(request, id):
    if request.user.is_superuser:
        try:
            ogrenci = Ogrenci.objects.get(id=id)
            user = ogrenci.kullanici 
            user.delete()
        except:
            pass
    return redirect('ogrenci_yonetimi')

@login_required(login_url='giris_yap')
def ogrenci_detay(request, id):
    if not request.user.is_superuser:
        return redirect('ana_sayfa')
    ogrenci = Ogrenci.objects.get(id=id)
    faturalar = Fatura.objects.filter(ogrenci=ogrenci).order_by('-son_odeme_tarihi')
    izinler = IzinTalebi.objects.filter(ogrenci=ogrenci).order_by('-id')
    
    return render(request, 'yurt/admin_student_detail.html', {'ogrenci': ogrenci, 'faturalar': faturalar, 'izinler': izinler})

@login_required(login_url='giris_yap')
def izin_durum_guncelle(request, id, durum):
    if request.user.is_superuser:
        izin = IzinTalebi.objects.get(id=id)
        if durum == 'onayla': izin.durum = 'onaylandi'
        elif durum == 'reddet': izin.durum = 'reddedildi'
        izin.save()
    return redirect('yonetici_paneli')

@login_required(login_url='giris_yap')
def toplu_fatura_kes(request):
    if not request.user.is_superuser: return redirect('ana_sayfa')
    
    bugun = datetime.date.today()
    aylar = {1:'Ocak', 2:'Şubat', 3:'Mart', 4:'Nisan', 5:'Mayıs', 6:'Haziran', 7:'Temmuz', 8:'Ağustos', 9:'Eylül', 10:'Ekim', 11:'Kasım', 12:'Aralık'}
    donem_ismi = f"{aylar[bugun.month]} {bugun.year}"
    son_odeme = bugun + datetime.timedelta(days=30)
    
    tum_ogrenciler = Ogrenci.objects.all()
    for ogrenci in tum_ogrenciler:
        zaten_var = Fatura.objects.filter(ogrenci=ogrenci, donem=donem_ismi).exists()
        if not zaten_var:
            Fatura.objects.create(ogrenci=ogrenci, donem=donem_ismi, tutar=7500.00, son_odeme_tarihi=son_odeme, durum='odenmedi')
            
    return redirect('yonetici_paneli')

@login_required(login_url='giris_yap')
def duyuru_ekle(request):
    if request.user.is_superuser and request.method == 'POST':
        baslik = request.POST.get('baslik')
        icerik = request.POST.get('icerik')
        Duyuru.objects.create(baslik=baslik, icerik=icerik)
    return redirect('yonetici_paneli')

@login_required(login_url='giris_yap')
def duyuru_sil(request, id):
    if request.user.is_superuser:
        Duyuru.objects.get(id=id).delete()
    return redirect('yonetici_paneli')