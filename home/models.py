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


class Section(models.Model):
    title = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question)
    page = models.ForeignKey('FormPage', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class FormPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField(Question)
    assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Assessment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
