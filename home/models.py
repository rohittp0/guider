from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Max, Sum
from mdeditor.fields import MDTextField

question_categories = (
    ('ss', 'Single Select'),
    ('ms', 'Multiple Select'),
    ('tf', 'True or False'),
    ('sa', 'Short Answer'),
    ('la', 'Long Answer'),
)

suggest_categories = (
    ('guide', 'Guide'),
    ('tool', 'Tool'),
    ('resource', 'Resource'),
    ('article', 'Article'),
    ('video', 'Video'),
    ('course', 'Course'),
    ('other', 'Other'),
)


class Options(models.Model):
    option_text = models.CharField(max_length=500)
    weight = models.IntegerField(default=0)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    suggestions = models.ManyToManyField('Suggestion', blank=True)

    def __str__(self):
        return self.option_text


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    info = models.TextField(help_text="Additional information about the question", blank=True, null=True)
    category = models.CharField(max_length=2, choices=question_categories)
    question_number = models.IntegerField()

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['question_number']


class Suggestion(models.Model):
    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=1000)
    url = models.CharField(max_length=500)
    category = models.TextField(choices=suggest_categories, default='other')

    def __str__(self):
        return self.title


class FormPage(models.Model):
    name = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=100)
    description = models.TextField()
    result_description = models.TextField()
    questions = models.ManyToManyField(Question, blank=True)
    assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE)
    skip_calculation = models.BooleanField(default=False)
    page_number = models.IntegerField()

    class Meta:
        ordering = ['page_number']

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.name:
            self.name = self.title[:30]
        super().save(force_insert, force_update, using, update_fields)


class Category(models.Model):
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=500)
    points = models.IntegerField()
    assessment = models.ForeignKey(to="Assessment", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Assessment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField()
    guidelines = MDTextField(null=True, blank=True)
    consents = ArrayField(models.CharField(max_length=200, help_text="Comma seperated list of consents"), default=list)
    result_guidelines = models.TextField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    response = models.ForeignKey('Response', on_delete=models.CASCADE)
    answer_text = models.TextField()


class Response(models.Model):
    current_page = models.ForeignKey('FormPage', on_delete=models.CASCADE, blank=True, null=True)
    assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.current_page is None:
            return self.assessment.name + ' - ' + self.date.strftime('%Y-%m-%d %H:%M')

        return self.assessment.name + ' - ' + self.current_page.title


class ResultPage(models.Model):
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
    page = models.ForeignKey('FormPage', on_delete=models.CASCADE)
    score = models.FloatField()
    suggestions = models.ManyToManyField(Suggestion, blank=True)


class Result(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    pages = models.ManyToManyField(FormPage, through=ResultPage)
    score = models.FloatField(default=-1)

    def __str__(self):
        return self.response.assessment.name

    def calculate_scores(self):
        self.score = 0
        page_scores = []

        for page in self.response.assessment.formpage_set.exclude(skip_calculation=True):
            questions = page.questions.filter(category__in=['ms', 'ss'])
            total_weight = questions.filter(category='ss').annotate(max_weight=Max('options__weight')).aggregate(
                Sum('max_weight'))['max_weight__sum'] or 0
            total_weight += questions.filter(category='ms').aggregate(Sum('options__weight'))['options__weight__sum'] or 0

            response_weight = 0
            suggestions = []

            for question in questions:
                try:
                    ids = self.response.answer_set.get(question=question).answer_text.split(',')
                    options = question.options_set.filter(id__in=ids)
                    suggestions += options.values_list('suggestions', flat=True)
                    response_weight += options.aggregate(Sum('weight'))['weight__sum'] or 0
                except Answer.DoesNotExist:
                    continue

            page_score = (response_weight / total_weight if total_weight else 0) * 100
            self.score += page_score

            page_scores.append((page, page_score, suggestions))

        self.score /= self.response.assessment.formpage_set.exclude(skip_calculation=True).count()
        self.category = (self.response.assessment.category_set.order_by("points")
                         .filter(points__gte=self.score).first())

        return page_scores

    def update_all(self):
        page_scores = self.calculate_scores()

        self.save()

        self.pages.clear()
        for page, score, suggestions in page_scores:
            result_page = ResultPage.objects.create(result=self, page=page, score=score)
            result_page.suggestions.set(filter(lambda x: x, suggestions))
            result_page.save()
