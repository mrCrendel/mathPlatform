from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # previous login view
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^/$', views.dashboard, name='dashboard'),

    # login / logout urls
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    # url(r'^/$', views.dashboard, name='dashboard'),

    # change password urls
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # restore password urls
    # url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #
    # url(r'^password-reset/$',
    #     'django.contrib.auth.views.password_reset',
    #     name='password_reset'),
    # url(r'^password-reset/done/$',
    #     'django.contrib.auth.views.password_reset_done',
    #     name='password_reset_done'),
    # url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
    #     'django.contrib.auth.views.password_reset_confirm',
    #     name='password_reset_confirm'),
    # url(r'^password-reset/complete/$',
    #     'django.contrib.auth.views.password_reset_complete',
    #     name='password_reset_complete'),

    # register url
    url(r'^register/$', views.register, name='register'),

    # user edit url
    url(r'^edit/$', views.edit, name='edit'),


]
