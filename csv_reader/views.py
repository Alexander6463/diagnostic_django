from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from .forms import UploadFileForm
from csv import reader


# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            my_csv = reader(form.files['file'].read().decode("utf-8"))


            #handle_uploaded_file(request.FILES['file'])
            return HttpResponse("Successfully uploaded")
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})
