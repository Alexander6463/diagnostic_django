from django.shortcuts import HttpResponse, render
from django.core.paginator import Paginator

from .forms import UploadFileForm, GetAnswersForm
from .utils.crud import (
    check_questions,
    create_answers,
    create_user,
    get_info,
    select_info,
)
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
    return render(request, "index.html")


def answers_and_users(request):
    if request.method == "GET":
        form = GetAnswersForm(request.GET)
        if form.is_valid():
            try:
                users = select_info(form.cleaned_data)
            except Exception as err:
                return HttpResponse(f"Invalid input data {err}")
            if users:
                request.session["users"] = users
            else:
                return HttpResponse("Users are not found")
        paginator = Paginator(list(request.session.get("users").items()), 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "users.html",
            {"page_obj": page_obj, "index": (page_obj.number - 1) * 10},
        )
    return render(request, "index.html")
