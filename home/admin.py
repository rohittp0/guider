from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Assessment, FormPage, Options, Question, Section


class OptionsInline(admin.TabularInline):
    model = Options
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline]
    list_display = ('question_text', 'category')
    list_filter = ['category']
    search_fields = ['question_text']


class SectionAdmin(NestedStackedInline):
    model = Section
    extra = 1


class FormPageAdmin(NestedStackedInline):
    model = FormPage
    extra = 1
    inlines = [SectionAdmin]


@admin.register(Assessment)
class AssessmentAdmin(NestedModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']
    inlines = [FormPageAdmin]
