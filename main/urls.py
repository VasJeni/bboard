from django.urls import path
from .views import index, other_page, BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPasswordChangeView, \
    RegisterUserView, RegisterDoneView, user_activate, DeleteUserView, BBPasswordResetView, BBPasswordResetConfirmView, \
    BBPasswordResetDoneView, BBPasswordResetCompleteView, by_rubric, detail

app_name = "main"
urlpatterns = [
    path('', index, name='index'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name="password_change"),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/active/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/password/reset/done/', BBPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='delete_profile'),
    path('accounts/profile/password/reset', BBPasswordResetView.as_view(), name='reset_password'),
    path('accounts/password/confirm/<uidb64>/<token>/', BBPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/password/confirm/complete/', BBPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
