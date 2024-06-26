from django.urls import path

from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('assessments', views.assessments, name='assessments'),
    path('assessment/<int:assessment_id>/<int:response_id>', views.assessment, name='assessment'),
    path('assessment/<int:assessment_id>/-1', views.assessment, {'response_id': -1}, name='assessment'),
    path('assessment/<int:assessment_id>/guidelines', views.guidelines, name='guidelines'),
    path('result/<int:response_id>/', views.result, name='result'),
    path('result/<int:response_id>/download', views.result_download, name='result_download')
]
