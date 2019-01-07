from django.contrib import admin
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

class AssignmentTopicInline(admin.StackedInline):
    model = AssignmentTopic
    extra = 1

@admin.register(Assignment)
class AssignmentAdmin(MarkdownxModelAdmin):
    inlines = [AssignmentTopicInline]

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
