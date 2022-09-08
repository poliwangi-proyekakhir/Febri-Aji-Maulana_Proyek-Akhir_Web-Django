from datetime import datetime, time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from home.models import *
from api.serializers import *
from facerec.main import train_model
from home.utils import DIR_PEGAWAI, save_image_api

class ModelApiView(APIView):
    def get(self, request, action=None):
        if action == 'train':
            nama_model = 'model/facemodel.clf'
            total = train_model(DIR_PEGAWAI, model_name=nama_model, n_neighbors=2)
            content = {'nama': nama_model, 'total': total}
            ModelWajah.objects.update_or_create(pk=1, defaults=content)

        model = ModelWajah.get_data()
        if model:
            serializer = ModelWajahSerializer(model)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'error': 'Model tidak tersedia dalam database, Train Data terlebih dahulu'})

class PresensiApiView(APIView):
    def post(self, request):
        suhu = request.data.get('suhu')
        waktu = request.data.get('jam')
        nama = request.data.get('nama')
        waktu_presensi = datetime.strptime(waktu, '%Y-%m-%d %H:%M:%S.%f')
        jam = waktu_presensi.time().replace(microsecond=0)
        hari = waktu_presensi.date()
        pegawai = Pegawai.objects.get(nama=nama)
        hadir = Presensi.objects.filter(pegawai=pegawai, tanggal=hari)
        jam_masuk = pegawai.shift.masuk
        jam_pulang = pegawai.shift.pulang
        if jam < jam_pulang:
            if not hadir.exists():
                note = 'Hadir' if jam <= jam_masuk else 'Telat'
                presensi = Presensi(pegawai=pegawai, tanggal=hari, masuk=jam, pulang=time(0, 0, 0), keterangan=note, suhu=suhu)
                presensi.save()
            else:
                presensi = hadir.first()
        elif jam >= jam_pulang:
            if not hadir.exists():
                return Response({'error': 'Tidak ada data presensi'}, status=status.HTTP_404_NOT_FOUND)
            else:
                hadir.update(pulang=jam)
                presensi = hadir.first()
        serializer = PresensiSerializer(presensi)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PegawaiApiView(APIView):
    def get(self, request):
        pegawai = Pegawai.objects.filter(foto='')

        serializer = PegawaiSerializer(pegawai, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        if pk:
            pegawai = Pegawai.objects.get(id=int(pk))
            data = request.data
            save_image_api(pegawai.nama, data)
            pegawai.foto = f"{pegawai.nama}/"
            pegawai.save()
            serializer = PegawaiSerializer(pegawai)
            return Response(serializer.data, status=status.HTTP_201_CREATED)