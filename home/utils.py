import os

from django.core.files.storage import FileSystemStorage

from web.settings import MEDIA_ROOT

DIR_PEGAWAI = os.path.join(MEDIA_ROOT, 'pegawai')
DIR_PRESENSI = os.path.join(MEDIA_ROOT, 'presensi')

def delete_image(name):
    path = os.path.join(DIR_PEGAWAI, name)
    isExist = os.path.exists(path)
    if isExist:
        for image in os.listdir(path):
            imgpath = os.path.join(path, image)
            os.remove(imgpath)
        os.rmdir(path)

def save_image_api(name, files):
    path = os.path.join(DIR_PEGAWAI, name)
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    fs = FileSystemStorage(path)
    c = 1
    for file in files:
        filename = f'{name}{c}.jpg'
        fs.save(filename, files[file])
        c+=1
    return

def save_image(name, files):
    path = os.path.join(DIR_PEGAWAI, name)
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    fs = FileSystemStorage(path)
    c = 1
    # if type(files)
    for file in files:
        filename = f'{name}{c}.jpg'
        fs.save(filename, file)
        c+=1
    return

def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'