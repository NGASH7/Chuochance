from django.urls import path
from .views import (
    period_and_level_settings,
    ApplicationsListView, RecommendedListView, SuccessfulListView,
    ApplicationView, ApplicationDetailView,
    load_wards, approve_applications,
    LevelUpdateView, LevelDeleteView,
    AnalyticsView, search_application_by_id
)

urlpatterns = [
    path('settings/', period_and_level_settings, name='settings'),
    path('applications-list/', ApplicationsListView.as_view(),
         name='applications-list'),
    path('recommended/', RecommendedListView.as_view(), name='recommended-list'),
    path('successful/', SuccessfulListView.as_view(), name='successful-list'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-details'),
    path('apply/', ApplicationView.as_view(), name='apply'),

    path('ajax/load-wards/', load_wards, name='ajax_load_wards'),
    path('ajax/approve-applications/', approve_applications,
         name='ajax_approve_applications'),

    path('level/<int:pk>/update/', LevelUpdateView.as_view(), name='update-level'),
    path('level/<int:pk>/delete/', LevelDeleteView.as_view(), name='delete-level'),

    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('search/', search_application_by_id, name='search-application')
]
