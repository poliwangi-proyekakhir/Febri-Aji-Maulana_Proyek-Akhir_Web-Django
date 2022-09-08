from rest_framework import serializers

from home.models import *

class ModelWajahSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelWajah
        fields = '__all__'

class PegawaiSerializer(serializers.ModelSerializer):
    jabatan = serializers.CharField(source='jabatan.nama')
    shift = serializers.CharField(source='shift.pulang')
    class Meta:
        model = Pegawai
        fields = ('id', 'nip', 'nama', 'jabatan', 'shift')

class JabatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jabatan
        fields = '__all__'

class PresensiSerializer(serializers.ModelSerializer):
    nama = serializers.CharField(source='pegawai.nama')
    nip = serializers.CharField(source='pegawai.nip')
    jabatan = serializers.CharField(source='pegawai.jabatan.nama')
    shift = serializers.CharField(source='pegawai.shift.pulang')
    class Meta:
        model = Presensi
        fields = ('tanggal', 'masuk', 'pulang', 'suhu', 'keterangan', 'nip', 'nama', 'jabatan', 'shift')