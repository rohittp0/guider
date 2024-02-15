from django.contrib import admin

from .models import Assessment, FormPage, Options, Question, Category, Suggestion, Result, ResultPage


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


class FormPageAdmin(admin.StackedInline):
    model = FormPage
    extra = 1


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
    inlines = [FormPageAdmin, CategoryInline]


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'url', 'category')
    list_filter = ['category']
    search_fields = ['title', 'caption']


class ResultPageAdmin(admin.TabularInline):
    model = ResultPage
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('response', 'category')
    list_filter = ['response']
    inlines = [ResultPageAdmin]
    readonly_fields = ['score', 'response', 'category', 'pages']
