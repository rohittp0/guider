from django.urls import path

from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('assessments', views.assessment, name='assessments'),
    path('assessment/<int:assessment_id>/<int:response_id>', views.assessment, name='assessment'),
]
