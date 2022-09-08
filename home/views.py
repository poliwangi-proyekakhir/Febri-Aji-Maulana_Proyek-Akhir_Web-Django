from datetime import date, datetime, timedelta

from django.views import View
from django.shortcuts import redirect, render
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from home.utils import *
from home.forms import *
from home.models import *
from facerec.main import train_model, predict

def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = 'Invalid user'
        else:
            error_message = 'Error Login'
    
    context = {'form': form, 'error': error_message}
    return render(request, 'pages/login.html', context)

def index_view(request):
    return redirect('dashboard')
    # context = {}
    # if request.method == 'POST':
    #     file = request.FILES['foto']
    #     fs = FileSystemStorage(DIR_PRESENSI)
    #     filename = fs.save(file.name, file)
    #     fileurl = os.path.join(DIR_PRESENSI, filename)
    #     predictions = predict(fileurl, model_path='media/model/facemodel.clf')
    #     print(predictions)
    #     if predictions[0][0] != 'unknown':
    #         pegawai = Pegawai.objects.get(nama=predictions[0][0])
    #         now = datetime.now().time()
    #         jam_masuk = pegawai.shift.masuk
    #         jam_pulang = pegawai.shift.pulang
    #         today = date.today()
    #         hadir = Presensi.objects.filter(pegawai=pegawai, tanggal=today)
    #         mulai_presensi = (datetime.combine(date.min, jam_masuk) - timedelta(minutes=30)).time()
    #         akhir_presensi = (datetime.combine(date.min, jam_masuk) + timedelta(minutes=30)).time()
    #         print(hadir)
    #         # Presensi masuk
    #         if now >= mulai_presensi: # and now <= akhir_presensi:
    #             if not hadir.exists():
    #                 ket = 'Telat' if now >= jam_masuk else 'Hadir'
    #                     # difference = (datetime.combine(date.min, now) - datetime.combine(date.min, jam_masuk)).seconds
    #                     # telat = int(difference/60)
    #                     # print(telat)
    #                 Presensi(
    #                     pegawai = pegawai,
    #                     tanggal = today,
    #                     masuk = now,
    #                     pulang = datetime.strptime('00:00', '%H:%M'),
    #                     keterangan = ket,
    #                 ).save()

    #         elif now >= jam_pulang:
    #             print('masuk')
    #             if not hadir.exists():
    #                 return
    #             else:
    #                 print('masuk')
    #                 hadir.update(
    #                     pulang=now
    #                 )
                    
    #         # print(pegawai)
    #         # print(now)
    #         # print(jam_masuk)
    #         # print(mulai_presensi)
        
    # #     return render(request, 'index.html', context)
    # return render(request, 'index.html', context)

@login_required
def dashboard_view(request):
    today = date.today()
    context = {'nav': 'dashboard'}
    context.update(Presensi.info(today=today, newest=5))
    context['pegawai'] = Pegawai.total()
    context['absen'] = context['pegawai'] - context['hadir'] - context['izin']
    context['model'] = ModelWajah.get_data()
    return render(request, 'pages/dashboard.html', context)

@method_decorator(login_required, name='dispatch')
class PegawaiView(View):
    context = {}
    form = PegawaiForm()

    def get(self, request, pk=None, action=None):
        path = request.get_full_path()

        if '/delete/confirm' in path:
            pk = int(path.split('/')[2])
            response = {'valid': 'success', 'message': 'Berhasil menghapus data.'}
            self.delete(pk)
            return JsonResponse(response)

        if is_ajax(request):
            if 'delete' in path:
                self.context['template'] = self.get_del_modal(pk)
            else:
                self.context['template'] = self.get_create_form(pk)
            return JsonResponse(self.context)
        if '/tambah' in path:
            context = {'nav': 'tambah', 'form': self.form}
            return render(request, 'pages/tambah.html', context)
        else:
            context = {'nav': 'pegawai', 'data': Pegawai.objects.all(),}
            return render(request, 'pages/pegawai.html', context)
    
    def post(self, request):
        form = PegawaiForm(request.POST)
        files = request.FILES.getlist('foto')
        if form.is_valid():
            if files:
                nama = form.cleaned_data['nama']
                save_image(nama, files)
                obj = form.save(commit=False)
                obj.foto = f'{nama}/'
                obj.save()
            else:
                form.save()
            return redirect('pegawai')

    def put(self, request, pk=None, action=None):
        id_ = self.get_object(pk)
        form = PegawaiForm(QueryDict(request.body), instance=id_)
        if form.is_valid():
            form.save()
            response = {'valid': 'success', 'message': 'Berhasil memperbarui data.'}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def delete(self, pk=None):
        data = Pegawai.objects.get(id=pk)
        data.delete()
        delete_image(data.nama)
        return redirect('pegawai')
        
    def get_create_form(self, pk=None):
        form = PegawaiForm()
        if pk:
            form = PegawaiForm(instance=self.get_object(pk))
        return render_to_string('partial/modal_form.html', {'form': form, 'data': 'pegawai'})
    
    def get_del_modal(self, pk=None):
        id_ = pk
        if pk:
            id_ = self.get_object(pk)
        return render_to_string('partial/modal_del.html', {'data': id_, 'page': 'pegawai'})

    def get_object(self, pk):
        return Pegawai.objects.get(id=pk)

@method_decorator(login_required, name='dispatch')
class JabatanView(View):
    context = {}
    form = JabatanForm()

    def get(self, request, pk=None, action=None):
        path = request.get_full_path()
        
        if '/delete/confirm' in path:
            pk = int(path.split('/')[2])
            response = {'valid': 'success', 'message': 'Berhasil menghapus data.'}
            self.delete(pk)
            return JsonResponse(response)
        
        if is_ajax(request):
            print('masuk')
            if 'delete' in path:
                self.context['template'] = self.get_del_modal(pk)
            else:
                self.context['template'] = self.get_create_form(pk)
            return JsonResponse(self.context)
        
        context = {
            'data': Jabatan.objects.all(),
            'form': self.form,
            'nav': 'jabatan'
        }
        return render(request, 'pages/jabatan.html', context)
    
    def post(self, request, pk=None, action=None):
        form = JabatanForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('jabatan')
        
    def put(self, request, pk=None, action=None):
        id_ = self.get_object(pk)
        form = JabatanForm(QueryDict(request.body), instance=id_)
        if form.is_valid():
            form.save()
            response = {'valid': 'success', 'message': 'Berhasil memperbarui data.'}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def delete(self, pk=None):
        data = Jabatan.objects.get(id=pk)
        data.delete()
        return redirect('jabatan')

    def get_create_form(self, pk=None):
        form = JabatanForm()
        if pk:
            form = JabatanForm(instance=self.get_object(pk))
        return render_to_string('partial/modal_form.html', {'form': form, 'data': 'jabatan'})
    
    def get_del_modal(self, pk=None):
        id_ = pk
        if pk:
            id_ = self.get_object(pk)
        return render_to_string('partial/modal_del.html', {'data': id_, 'page': 'jabatan'})

    def get_object(self, pk):
        return Jabatan.objects.get(id=pk)

@method_decorator(login_required, name='dispatch')
class PresensiView(View):
    def get(self, request, pk=None, action=None):
        today = date.today()
        path = request.get_full_path()

        if action:
            pegawai = self.get_object(pk)
            now = datetime.now().time()
            ket = action.title()
            
            hadir = Presensi.objects.filter(pegawai=pegawai, tanggal=today)
            if not hadir.exists():
                Presensi(
                    pegawai = pegawai,
                    tanggal = today,
                    masuk = now,
                    pulang = datetime.strptime('00:00', '%H:%M'),
                    keterangan = ket,
                ).save()
            return redirect('kelolaizin')

        params = request.GET
        tgl = datetime.strptime(params.get('date'), '%d-%m-%Y').date() if params.get('date') else today
        context = {'tanggal': tgl.strftime('%d-%m-%Y')}

        if '/kelolaizin' in path:
            pegawai = Pegawai.objects.exclude(presensi__tanggal=tgl)
            context.update({'nav': 'izin', 'data': pegawai})
            return render(request, 'pages/izin.html', context)
        else:
            presensi = Presensi.objects.all().filter(tanggal=tgl)
            context.update({'nav': 'pegawai', 'data': presensi,})
            return render(request, 'pages/presensi.html', context)
    
    def get_object(self, pk):
        return Pegawai.objects.get(id=pk)

@method_decorator(login_required, name='dispatch')
class ShiftView(View):
    context = {}
    form = ShiftForm()
    
    def get(self, request, pk=None, action=None):
        path = request.get_full_path()
        if '/delete/confirm' in path:
            pk = int(path.split('/')[2])
            response = {'valid': 'success', 'message': 'Berhasil menghapus data.'}
            self.delete(pk)
            return JsonResponse(response)

        if is_ajax(request):
            if 'delete' in path:
                self.context['template'] = self.get_del_modal(pk)
            else:
                self.context['template'] = self.get_create_form(pk)
            return JsonResponse(self.context)
        context = {
            'nav': 'shift',
            'data': Shift.objects.all(),
            'form': self.form
        }
        return render(request, 'pages/shift.html', context)
    
    def post(self, request, pk=None, action=None):
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            response = {'valid': 'success', 'message': 'Berhasil menambahkan data.'}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)
    
    def put(self, request, pk=None, action=None):
        id_ = self.get_object(pk)
        form = ShiftForm(QueryDict(request.body), instance=id_)
        if form.is_valid():
            form.save()
            response = {'valid': 'success', 'message': 'Berhasil memperbarui data.'}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def delete(self, pk=None):
        shift = Shift.objects.get(id=pk)
        shift.delete()
        return redirect('shift')
        
    def get_create_form(self, pk=None):
        form = ShiftForm()
        if pk:
            form = ShiftForm(instance=self.get_object(pk))
        return render_to_string('partial/modal_form.html', {'form': form, 'data': 'shift'})
    
    def get_del_modal(self, pk=None):
        id_ = pk
        if pk:
            id_ = self.get_object(pk)
        return render_to_string('partial/modal_del.html', {'data': id_, 'page': 'shift'})

    def get_object(self, pk):
        return Shift.objects.get(id=pk)

@login_required
def train_view(request):
    nama_model = 'model/facemodel.clf'
    total = train_model(DIR_PEGAWAI, model_name=nama_model, n_neighbors=2)
    content = {'nama': nama_model, 'total': total}
    ModelWajah.objects.update_or_create(pk=1, defaults=content)
    return redirect('dashboard')