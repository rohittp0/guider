from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin

from .models import Assessment, FormPage, Options, Question, Response, Answer, Category, Suggestion


class OptionsInline(admin.TabularInline):
    model = Options
    extra = 0


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class SuggestionInline(admin.TabularInline):
    model = Suggestion
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline]
    list_display = ('question_text', 'category')
    list_filter = ['category']
    search_fields = ['question_text']


class FormPageAdmin(StackedInline):
    model = FormPage
    extra = 1


@admin.register(Assessment)
class AssessmentAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
    inlines = [FormPageAdmin, CategoryInline, SuggestionInline]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'current_page')
    list_filter = ['assessment']
    search_fields = ['assessment']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'response', 'answer_text')
    list_filter = ['response']
    search_fields = ['question']
