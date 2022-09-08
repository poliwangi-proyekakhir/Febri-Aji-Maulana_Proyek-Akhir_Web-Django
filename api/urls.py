from django.urls import path, re_path

from .views import *

urlpatterns = [
    re_path(r'model/(?:(?P<action>\w+)/)?', ModelApiView.as_view()),
    path('presensi/', PresensiApiView.as_view()),
    re_path(r'pegawai/(?:(?P<pk>\d+)/)?', PegawaiApiView.as_view()),
    # path('<str:nama>/', PegawaiDetailApiView.as_view()),
    # path('jabatan/', JabatanApiView.as_view(), name='jabatan_api'),
    # path('jabatan/<int:jabatan_id>/', JabatanDetailApiView.as_view()),
]