import logging
import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation


def fix_marks(name):
    school_kid = find_school_kid(name)
    marks = Mark.objects.filter(schoolkid=school_kid, points__in=[2, 3])
    for mark in marks:
        mark.points = random.randint(4, 5)
        mark.save()


def find_school_kid(name):
    try:
        school_kid = Schoolkid.objects.get(full_name__contains=name)
        return school_kid
    except ObjectDoesNotExist:
        logging.warning('Не было найдено ученика с таким именем')
    except MultipleObjectsReturned:
        logging.warning('Было найдено несколько учеников с таким именем')


def delete_chastisements(name):
    school_kid = find_school_kid(name)
    chastisements = Chastisement.objects.filter(schoolkid=school_kid)
    chastisements.delete()


def create_commendation(name, subject_name, date=None):
    school_kid = find_school_kid(name)
    year_of_study = school_kid.year_of_study
    group_letter = school_kid.group_letter
    subject = Subject.objects.get(title__contains=subject_name, year_of_study=year_of_study)
    if date:
        try:
            lesson = Lesson.objects.get(year_of_study=year_of_study, group_letter=group_letter, subject=subject, date=date)
        except ObjectDoesNotExist:
            logging.warning('У этого ученика не было этого предмета в эту дату')
            return
    else:
        commendations = Commendation.objects.filter(schoolkid=school_kid, subject=subject)
        commendations_dates = []
        for commendation in commendations:
            commendations_dates.append(commendation.created)
        lessons = Lesson.objects.filter(
            year_of_study=year_of_study,
            group_letter=group_letter,
            subject=subject,
        ).exclude(date__in=commendations_dates)
        lesson = random.choice(lessons)
    teacher_name = lesson.teacher
    commendation_texts = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]
    Commendation.objects.create(
        text=random.choice(commendation_texts),
        created=lesson.date,
        schoolkid=school_kid,
        subject=subject,
        teacher=teacher_name
    )


