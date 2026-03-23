from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict_view, name='predict'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path("feedback/", views.feedback_view, name="feedback"),
    path(
    "prediction/pdf/<int:prediction_id>/",
    views.download_prediction_pdf,
    name="download_prediction_pdf"),
    path('design/', views.design, name='design'),
    path("contact/", views.contact, name="contact"),
    path("result/", views.result, name="result"),
    path("history/", views.history, name="history"),
    path("prediction/<int:pk>/", views.prediction_detail, name="prediction_detail"),

    # Password reset
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
