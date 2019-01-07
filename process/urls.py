from django.conf.urls import url
from process.views import *
from django.contrib.auth import views as auth_views

app_name = 'process'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', IndexTemplateView.as_view(), name='index'),
    # url(r'^login$', auth_views.login, name='login'),
    # url(r'^logout$', auth_views.logout, {'next_page': 'process:index'}, name='logout'),

    url(r'^assignments/$', AssignmentListView.as_view(), name='assignment_list'),
    url(r'^assignments/(?P<slug>[\w-]+)/$', AssignmentDetailView.as_view(), name='assignment_detail'),
    url(r'^assignments/(?P<slug>[\w-]+)/question/$', AssignmentFormView.as_view(), name='assignment_session_form'),
    # url(r'^assignments/(?P<pk>\d+)/$', AssignmentFormView.as_view(), name='assignment_form'),
    # url(r'^assignments/(?P<pk>\d+)/$', AssignmentDetailView.as_view(), name='aAssignmentSessionResulthViewssignment_deteil'),
    url(r'^assignments/(?P<slug>[\w-]+)/final/$', AssignmentSessionFinalView.as_view(), name='assignment_seshion_final'),
    # url(r'^assignments/(?P<slug>[\w-]+)/result/$', AssignmentSessionResultView.as_view(), name='assignment_seshion_result'),

    url(r'^assignment-results/$', AssignmentResultsListView.as_view(), name='assignment_result_list'),
    url(r'^assignment-results/(?P<pk>\d+)/$', AssignmentResultDetailView.as_view(), name='assignment_result_detail'),

    url(r'^assignment-users-results/$', CuratorAssignmentList.as_view(), name='supper_assignments_list'),
    url(r'^assignment-users-results/(?P<slug>[\w-]+)/$', CuratorAssignmentSessionList.as_view(), name='supper_assignments_session_list'),
    url(r'^assignment-users-results/(?P<slug>[\w-]+)/(?P<pk>\d+)/$', CuratorAssignmentUserSessionResult.as_view(), name='supper_sesion_result_detail'),

    url(r'^streams/$', StreamListView.as_view(), name='streams_list'),
    url(r'^streams/(?P<slug>[\w-]+)/$', StreamDetailView.as_view(), name='stream_detail'),
    url(r'^streams/(?P<slug>[\w-]+)/enroll/$', StreamEnrolelView.as_view(), name='stream_enroll'),
    url(r'^streams/(?P<slug>[\w-]+)/unenroll/$', StreamUnenrollView.as_view(), name='stream_unenroll'),

    url(r'^subjects/$', SubjectListView.as_view(), name='subjects_list'),
    url(r'^subjects/(?P<slug>[\w-]+)/$', SubjectDetailView.as_view(), name='subject_detail'),

    url(r'^subjects/(?P<slug>[\w-]+)/topic/(?P<topic_slug>[\w-]+)/$', TopicDetailView.as_view(), name='topic_detail'),
    url(r'^subjects/(?P<slug>[\w-]+)/topic/(?P<topic_slug>[\w-]+)/check/$', TopicCheckAnswerView.as_view(), name='topic_check'),
]
