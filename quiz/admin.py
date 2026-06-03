from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'chapter', 'difficulty', 'is_original')
    list_filter = ('chapter', 'difficulty', 'is_original')
    search_fields = ('text', 'explanation')
    inlines = [ChoiceInline]

    def short_text(self, obj):
        return obj.text[:40]
    short_text.short_description = '題目'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__text')
