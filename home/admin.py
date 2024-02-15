from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin

from .models import Assessment, FormPage, Options, Question, Category, Suggestion, Result


class OptionsInline(admin.TabularInline):
    model = Options
    extra = 0


class CategoryInline(admin.TabularInline):
    model = Category
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
    inlines = [FormPageAdmin, CategoryInline]


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'url', 'category')
    list_filter = ['category']
    search_fields = ['title', 'caption']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
