from django.db.models import Sum

from .models import FormPage


def calculate_scores(response):
    pages_scores = []
    for page in FormPage.objects.filter(assessment=response.assessment).exclude(skip_calculation=True):
        questions = page.questions.filter(category__in=['ms', 'ss'])
        total_weight = questions.annotate(total_weight=Sum('options__weight')).aggregate(Sum('total_weight'))[
            'total_weight__sum']

        # Corrected: Calculate response_weight by properly filtering selected options
        response_weight = 0
        for question in questions:
            ids = response.answer_set.get(question=question).answer_text.split(',')
            response_weight += question.options_set.filter(id__in=ids).aggregate(Sum('weight'))['weight__sum'] or 0

        page_score = round((response_weight / total_weight if total_weight else 0) * 100, 2)  # Convert to percentage
        pages_scores.append((page.name, page_score, 100 - page_score))

    return pages_scores


def calculate_overall(page_scores):
    if not page_scores:
        return 0
    total_score = sum([page[1] for page in page_scores])
    overall_score = round(total_score / len(page_scores), 2)  # Average score across all pages
    return overall_score
