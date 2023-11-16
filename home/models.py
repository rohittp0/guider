from django.db import models

question_categories = (
    ('ss', 'Single Select'),
    ('ms', 'Multiple Select'),
    ('tf', 'True or False'),
    ('sa', 'Short Answer'),
    ('la', 'Long Answer'),
)


class Options(models.Model):
    option_text = models.CharField(max_length=200)
    weight = models.IntegerField(default=0)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.option_text


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=question_categories)

    def __str__(self):
        return self.question_text


class FormPage(models.Model):
    name = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField(Question, blank=True)
    assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE)
    skip_calculation = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.name:
            self.name = self.title[:30]
        super().save(force_insert, force_update, using, update_fields)


class Assessment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField()

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
            return self.assessment.name + ' - ' + 'Finished'

        return self.assessment.name + ' - ' + self.current_page.title
