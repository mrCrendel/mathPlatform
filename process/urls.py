from django.conf.urls import url
from process import views
from django.contrib.auth import views as auth_views

app_name = 'process'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexTemplateView.as_view(), name='index'),
    # url(r'^login$', auth_views.login, name='login'),
    # url(r'^logout$', auth_views.logout, {'next_page': 'process:index'}, name='logout'),

    url(r'^assignments/$', views.AssignmentListView.as_view(), name='assignment_list'),
    url(r'^assignments/(?P<slug>[\w-]+)/$', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    url(r'^assignments/(?P<slug>[\w-]+)/question/$', views.AssignmentFormView.as_view(), name='assignment_session_form'),
    # url(r'^assignments/(?P<pk>\d+)/$', AssignmentFormView.as_view(), name='assignment_form'),
    # url(r'^assignments/(?P<pk>\d+)/$', AssignmentDetailView.as_view(), name='aAssignmentSessionResulthViewssignment_deteil'),
    url(r'^assignments/(?P<slug>[\w-]+)/final/$', views.AssignmentSessionFinalView.as_view(), name='assignment_seshion_final'),
    # url(r'^assignments/(?P<slug>[\w-]+)/result/$', AssignmentSessionResultView.as_view(), name='assignment_seshion_result'),

    url(r'^assignment-results/$', views.AssignmentResultsListView.as_view(), name='assignment_result_list'),
    url(r'^assignment-results/(?P<pk>\d+)/$', views.AssignmentResultDetailView.as_view(), name='assignment_result_detail'),

    url(r'^assignment-users-results/$', views.CuratorAssignmentList.as_view(), name='supper_assignments_list'),
    url(r'^assignment-users-results/(?P<slug>[\w-]+)/$', views.CuratorAssignmentSessionList.as_view(), name='supper_assignments_session_list'),
    url(r'^assignment-users-results/(?P<slug>[\w-]+)/(?P<pk>\d+)/$', views.CuratorAssignmentUserSessionResult.as_view(), name='supper_sesion_result_detail'),

    url(r'^streams/$', views.StreamListView.as_view(), name='streams_list'),
    url(r'^streams/(?P<slug>[\w-]+)/$', views.StreamDetailView.as_view(), name='stream_detail'),
    url(r'^streams/(?P<slug>[\w-]+)/enroll/$', views.StreamEnrolelView.as_view(), name='stream_enroll'),
    url(r'^streams/(?P<slug>[\w-]+)/unenroll/$', views.StreamUnenrollView.as_view(), name='stream_unenroll'),

    url(r'^subjects/$', views.SubjectListView.as_view(), name='subjects_list'),
    url(r'^subjects/(?P<slug>[\w-]+)/$', views.SubjectDetailView.as_view(), name='subject_detail'),

    url(r'^subjects/(?P<slug>[\w-]+)/topic/(?P<topic_slug>[\w-]+)/$', views.TopicDetailView.as_view(), name='topic_detail'),
    url(r'^subjects/(?P<slug>[\w-]+)/topic/(?P<topic_slug>[\w-]+)/check/$', views.TopicCheckAnswerView.as_view(), name='topic_check'),
    # url(r'^subjects/(?P<slug>[\w-]+)/topic/(?P<topic_slug>[\w-]+)/check_user_answer/$', views.check_user_answer, name='check_user_answer'),
    url(r'^ajax/check_user_answer/$', views.check_user_answer, name='check_user_answer'),
]
