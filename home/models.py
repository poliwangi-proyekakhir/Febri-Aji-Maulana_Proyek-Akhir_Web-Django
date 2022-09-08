from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

class Shift(models.Model):
    masuk = models.TimeField()
    pulang = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.id} ({self.masuk} - {self.pulang})'

class Jabatan(models.Model):
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.nama}'

class Pegawai(models.Model):
    nip = models.CharField(max_length=18)
    nama = models.CharField(max_length=255)
    nohp = models.CharField(max_length=12)
    foto = models.ImageField(upload_to='media/pegawai/', blank=True)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.nama}'

    @classmethod
    def total(cls):
        return cls.objects.all().count()

class Presensi(models.Model):
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    tanggal = models.DateField()
    masuk = models.TimeField()
    pulang = models.TimeField()
    suhu = models.CharField(max_length=5, blank=True)
    keterangan = models.CharField(max_length=100)

    @classmethod
    def info(cls, today, newest):
        res = {}
        data = cls.objects.filter(tanggal=today)
        res['data'] = data.order_by('-id')[:newest]
        res['hadir'] = data.filter(Q(keterangan='Hadir') | Q(keterangan='Telat')).count()
        res['izin'] = data.filter(Q(keterangan='Izin') | Q(keterangan='Sakit')).count()
        return res

class ModelWajah(models.Model):
    nama = models.FileField(upload_to='media/model/')
    total = models.CharField(max_length=4)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.nama}'
    
    @classmethod
    def get_data(cls):
        try:
            return ModelWajah.objects.get(id=1)
        except ObjectDoesNotExist:
            return None

