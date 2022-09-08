from django import forms

from home.models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                'placeholder': 'Username',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget= forms.PasswordInput(
            attrs= {
                'placeholder': 'Password',
                'class': 'form-control'
            }
        )
    )

class PegawaiForm(forms.ModelForm):
    nip = forms.CharField(
        label='NIP/NIK',
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan NIP/NIK'
            }
        )
    )
    nama = forms.CharField(
        label='Nama Pegawai',
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan Nama'
            }
        )
    )
    nohp = forms.CharField(
        max_length=13,
        label="Nomor Handphone",
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan No HP'
            }
        )
    )
    foto = forms.ImageField(
        required=False,
        label="Foto Wajah",
        widget= forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan No HP',
                'accept': 'image/*',
                'multiple': True
            }
        )
    )
    jabatan = forms.ModelChoiceField(
        queryset=Jabatan.objects.all(),
        widget= forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    shift = forms.ModelChoiceField(
        queryset=Shift.objects.all(),
        widget= forms.Select(
            attrs={
                'class': 'form-control',
            }
        ), 
    )

    class Meta:
        model = Pegawai
        fields = ['nip', 'nama', 'nohp', 'jabatan', 'shift', 'foto', ]

class JabatanForm(forms.ModelForm):
    nama = forms.CharField(
        label='Nama Jabatan',
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = Jabatan
        fields = ['nama',]

class ShiftForm(forms.ModelForm):
    masuk = forms.TimeField(
        label='Jam Masuk',
        widget=forms.TimeInput(
            attrs= {
                'class': 'form-control',
                'type': 'time',
            }
        )
    )
    pulang = forms.TimeField(
        label='Jam Pulang',
        widget=forms.TimeInput(
            attrs= {
                'class': 'form-control',
                'type': 'time',
            }
        )
    )
    class Meta:
        model = Shift
        fields = ['masuk', 'pulang',]