from django.contrib import admin
from django import forms
from markdownx.admin import MarkdownxModelAdmin
from process.models import *

admin.site.register(HomePage)
admin.site.register(Stream)

admin.site.register(Topic)
# admin.site.register(UserAnswer)
#
# class UserQuestionsAnswerAdmin(admin.StackedInline):
#     model = admin.StackedInline
    # extra = 1

# @admin.register(Assignment)
# class UserAnswerAdmin(MarkdownxModelAdmin):
#     inlines = [UserQuestionsAnswer]


# class AssignmentTopicForm(forms.ModelForm):
#     class Meta:
#         model = AssignmentTopic
#         widgets = {
#             'new_text': autocomplete.ListSelect2(url='post-new-text', forward=['target_field', 'check_field'])
#         }
#
#         fields = ('__all__')


class AssignmentTopicInline(admin.StackedInline):
    model = AssignmentTopic
    # form = AssignmentTopicForm
    extra = 1

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.3.1.min.js',  # jquery
            # 'admin/js/formset_handlers.js',  # project static folder
            # 'app/js/myscript.js',  # app static folder
        )


@admin.register(Assignment)
class AssignmentAdmin(MarkdownxModelAdmin):
    inlines = [AssignmentTopicInline]
    prepopulated_fields = {'slug': ('title',)}


class TopicAdmin(admin.StackedInline):
    model = Topic
    extra = 1


@admin.register(Subject)
class SubjectAdmin(MarkdownxModelAdmin):
    inlines = [TopicAdmin]


class AssignmentSessionQuestionsAdmin(admin.StackedInline):
    model = AssignmentSessionQuestions
    extra = 0


@admin.register(AssignmentSession)
class AssignmentSessionAdmin(MarkdownxModelAdmin):
    inlines = [AssignmentSessionQuestionsAdmin]

    def is_finished(self, obj):
        return obj.current_index >= obj.questions_amount

