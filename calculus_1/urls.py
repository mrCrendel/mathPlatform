from django.conf.urls import url

from . import views

app_name = 'calculus_1'
urlpatterns = [
    url(r'^generate-expression/([\w|\W|\d|\D]+)$',
        views.generate_example,
        name='generate_expression'),
    url(r'^solve-expression$',
        views.solve_expression,
        name='solve_expression')
]
