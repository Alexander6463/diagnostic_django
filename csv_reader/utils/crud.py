import tempfile
from csv import reader
from typing import List

from django.db.models import QuerySet

from .configure_logging import configure_logging
from .coding import choices_db
from csv_reader.forms import UploadFileForm
from csv_reader.models import Answers, Question, User

logger = configure_logging(__file__)


def get_info(form: UploadFileForm) -> reader:
    tmp_file = tempfile.mktemp("upload.csv")
    with open(tmp_file, "w") as f:
        f.write(form.files["file"].read().decode("utf-8"))
    with open(tmp_file, "r") as f:
        csv_reader = reader(f, delimiter=",")
        questions = next(csv_reader)[20:]
        result = []
        for row in csv_reader:
            result.append({"user": row[:20], "answers": row[20:]})
    return questions, result


def check_questions(questions: List[str]) -> QuerySet[Question]:
    q_db = Question.objects.all()
    for question in questions:
        if not q_db.filter(text_question=question):
            logger.info("Question %s has been added", question)
            q = Question(text_question=question)
            q.save()
    return q_db


def create_user(info: List[str]) -> User:
    user = User(
        user_id=int(info[0]),
        time_create=info[1],
        time_changed=info[2],
        name=info[3],
        group=info[4],
        member_gz_2021_2022=choices_db.get("yes_no_choices").get(info[5]),
        sex=choices_db.get("sex_choices").get(info[6]),
        age=bin(int(info[7]))[2:],
        marital_status=choices_db.get("martial_status_choices").get(info[8]),
        living=choices_db.get("living_choices").get(info[9]),
        children=choices_db.get("children_choices").get(info[10]),
        work_status=choices_db.get("work_status_choices").get(info[11]),
        working_in_fishing_or_shipping=choices_db.get("yes_no_choices").get(info[12]),
        working_maritime=choices_db.get("yes_no_choices").get(info[13]),
        working_fishing_industry=choices_db.get("yes_no_choices").get(info[14]),
        working_fishing_technology=choices_db.get("yes_no_choices").get(info[15]),
        working_aquaculture=choices_db.get("yes_no_choices").get(info[16]),
        working_economic=choices_db.get("yes_no_choices").get(info[17]),
        working_it=choices_db.get("yes_no_choices").get(info[18]),
        working_other=choices_db.get("yes_no_choices").get(info[19]),
    )
    user.save()
    logger.info("User %s successfully saved", info[3])
    return user


def create_answers(
    user: User, questions: QuerySet[Question], answers: List[str]
) -> None:
    for answer, question in zip(answers, questions):
        ans = Answers(
            user=user,
            question=question,
            answer=answer,
            answer_bin=choices_db.get("answer_choices").get(answer),
        )
        ans.save()
    logger.info("Answers for user %s successfully saved", user.name)