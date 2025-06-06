from django.urls import path
from . import views


urlpatterns = [
    path('classes/',views.StudentClassListView.as_view(),name='all_classes'),
    path('add-class/',views.StudentClassCreateView.as_view(),name='add_class'),
    path('class_detail/<int:pk>/',views.StudentClassDetailView.as_view(),name='class_detail'),
    path('class_update/<int:pk>/',views.StudentClassUpdateView.as_view(),name='class_update'),
    path('class_delete/<int:pk>/',views.StudentClassDeleteView.as_view(),name='class_delete'),
]
