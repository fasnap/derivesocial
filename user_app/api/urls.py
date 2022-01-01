from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from user_app.api import views
from rest_framework.routers import DefaultRouter
from user_app.api.views import  ChangePasswordView,UserSearchListView

urlpatterns = [
    path('change_password/<int:pk>/',ChangePasswordView.as_view(),name='change-password'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.user_registration_view.as_view(), name='user-register'),
    path('search/',UserSearchListView.as_view(),name='user-search'),
    # path('profile/',views.profile,name='profile')
    # path('profile/',UserProfileUpdateView.as_view(),name='profile'),
    # path('profile/',views.UserProfileView.as_view(), name='user-profile'),
    # path('logout/', views.APILogoutView.as_view(), name='logout_token'),
    # path("", include(ROUTER.urls)),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
