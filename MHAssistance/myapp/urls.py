from django.contrib import admin
from django.urls import path
from myapp import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('assessments/', views.AssessmentListCreateView.as_view(), name='assessment-list-create'),
    # path('assessments/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment-detail'),
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/',views.UserProfileView.as_view(), name='user-profile'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<int:uid>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    path('assessments/', views.AssessmentListView.as_view(), name='assessments-list'),
    path('user-assessments/', views.UserAssessmentView.as_view(), name='user-assessments'),
    path('self-care-content/', views.SelfCareContentListView.as_view(), name='self-care-content'),
    path('challenges/', views.ChallengeListView.as_view(), name='challenges-list'),
    path('user-challenges/', views.UserChallengeView.as_view(), name='user-challenges'),
    path('submit-assessment/', views.SubmitAssessmentView.as_view(), name='submit-assessment'),

    path('assessments/manage/', views.AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('assessments/manage/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment-detail'),
    path('posts/', views.ForumPostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<uuid:pk>/', views.ForumPostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<uuid:pk>/like/', views.ForumPostLikeAPIView.as_view(), name='post-like'),
    path('posts/<uuid:pk>/comment/', views.ForumPostCommentAPIView.as_view(), name='post-comment'),

    path('comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('tags/', views.TagListCreateAPIView.as_view(), name='tag-list-create'),



    # path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    # path('login/', views.UserLoginView.as_view(), name='user-login'),
]