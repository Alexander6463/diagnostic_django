import datetime

from django.shortcuts import HttpResponse, render

from .forms import UploadFileForm
from .utils.crud import check_questions, create_answers, create_user, get_info
from .utils.configure_logging import configure_logging

# Create your views here.

logger = configure_logging(__file__)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            questions, users_and_answers = get_info(form)
            q_db = check_questions(questions=questions)
            for info in users_and_answers:
                try:
                    user = create_user(info=info["user"])
                    create_answers(answers=info["answers"], questions=q_db, user=user)
                except BaseException as err:
                    logger.exception(err)
            return HttpResponse("Successfully uploaded")
    else:
        form = UploadFileForm()
    return render(request, "index.html", {"form": form})
