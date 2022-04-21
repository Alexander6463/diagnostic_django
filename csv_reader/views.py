from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from .forms import UploadFileForm
from csv import reader
import tempfile

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_file = tempfile.mktemp("upload.csv")
            with open(tmp_file, "w") as f:
                f.write(form.files['file'].read().decode("utf-8"))
            with open(tmp_file, "r") as f:
                for element in reader(f, delimiter=','):
                    print(element)



            #handle_uploaded_file(request.FILES['file'])
            return HttpResponse("Successfully uploaded")
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})
