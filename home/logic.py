from django.db.models import Sum, Max
from .models import FormPage, Answer


def calculate_scores(response):
    pages_scores = []
    for page in FormPage.objects.filter(assessment=response.assessment).exclude(skip_calculation=True):
        questions = page.questions.all()
        total_weight = questions.annotate(max_weight=Max('options__weight')).aggregate(Sum('max_weight'))[
            'max_weight__sum']
        response_weight = Answer.objects.filter(question__in=questions, response=response).annotate(
            sel_weight=Sum('question__options__weight')).aggregate(Sum('sel_weight'))['sel_weight__sum']
        page_score = (response_weight / total_weight if total_weight else 0) * 100  # Convert to percentage
        pages_scores.append((page.name, page_score, 100 - page_score))

    return pages_scores


def calculate_overall(page_scores):
    total_weight = sum([page[1] for page in page_scores])
    total_score = sum([page[2] for page in page_scores])
    return total_score / total_weight * 100 if total_weight else 0
