from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import Assessment, Question, Option, UserAssessment
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone
from .models import CustomUser, Assessment, UserAssessment, SelfCareContent, Challenge, UserChallenge, Assessment, Question, Option, ForumPost, Comment, PostLike, Tag
from .serializers import UserSerializer, UserRegistrationSerializer, AssessmentSerializer, UserAssessmentSerializer, SelfCareContentSerializer, ChallengeSerializer, UserChallengeSerializer,  QuestionSerializer, OptionSerializer, ForumPostSerializer, CommentSerializer, PostLikeSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserRegistrationView(APIView):

    def get(self, request):
        # Render registration HTML form
        return render(request, 'registration.html')

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({
                    'message': 'User registered successfully',
                    # 'user': serializer.data
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'email' in str(e):  # Check if the error is related to email
                    return Response({
                        'email': ['A user with this email already exists.']
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    suggested_username = CustomUser.objects.generate_anon_username()
                    return Response({
                        'error': 'A user with this anon_username already exists.',
                        'suggestion': f"Try this username instead: {suggested_username}"
                    }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        anon_username = request.data.get('anon_username')
        # email = request.data.get('email')
        password = str(request.data.get('password', ''))
        # user = authenticate(anon_username=anon_username, password=password)
        # user = authenticate(email=email, password=password)
        # if user is not None:
        #     serializer = UserSerializer(user)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # if not email or not password:
        if not anon_username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(anon_username=anon_username)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this Username does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):  # Manually check hashed password
            user.last_login = timezone.now()
            user.save()
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({
                'message': 'User logged in successfully',
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # request.user.auth_token.delete()
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        try:
            # Extract refresh token from request data
            # refresh_token = request.data.get('refresh')
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token

            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except TokenError as e:
            # Log the specific token error
            return Response({'error': f'Token error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Invalid token or logout failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            # reset_link = f"http://yourfrontend.com/reset-password/{user.pk}/{token}/"
            # reset_link = f"http://localhost:3000/api/user/reset-password/{user.pk}/{token}/"
            reset_link = f"http://localhost:3000/api/reset-password/{user.pk}/{token}/"

            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@yourapp.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        new_password = request.data.get('new_password')
        try:
            user = CustomUser.objects.get(pk=uid)
            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

class AssessmentListView(APIView):
    def get(self, request):
        assessments = Assessment.objects.all()
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_assessments = UserAssessment.objects.filter(user=request.user)
        serializer = UserAssessmentSerializer(user_assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = UserAssessmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SelfCareContentListView(APIView):
    def get(self, request):
        contents = SelfCareContent.objects.all()
        serializer = SelfCareContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChallengeListView(APIView):
    def get(self, request):
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChallengeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_challenges = UserChallenge.objects.filter(user=request.user)
        serializer = UserChallengeSerializer(user_challenges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = UserChallengeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubmitAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Expects payload:
        {
            "assessment_id": "123",
            "answers": [
                {"question_id": "q1", "option_id": "opt1"},
                {"question_id": "q2", "option_id": "opt5"},
                ...
            ]
        }
        """
        user = request.user
        data = request.data

        assessment_id = data.get("assessment_id")
        answers = data.get("answers", [])

        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

        total_score = 0

        for answer in answers:
            option_id = answer.get("option_id")
            try:
                option = Option.objects.get(id=option_id)
                total_score += option.score  # Add the score of selected option
            except Option.DoesNotExist:
                return Response({"error": f"Option with ID {option_id} not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate feedback based on assessment title and total score   
        # Return total score and feedback
        result = self.get_feedback(assessment.title, total_score)

        # Save UserAssessment result
        user_assessment = UserAssessment.objects.create(
            user=user,
            assessment=assessment,
            total_score=total_score,
            result=result
        )

        
        return Response({
            "message": "Assessment submitted successfully.",
            "total_score": total_score,
            "result": result
        }, status=status.HTTP_201_CREATED)

    def get_feedback(self, assessment_title, score):
        """
        Example logic for feedback based on total score.
        """
        if assessment_title == "PHQ-9 Depression Assessment":
            if score <= 4:
                return "Minimal or no depression."
            elif score <= 9:
                return "Mild depression."
            elif score <= 14:
                return "Moderate depression."
            elif score <= 19:
                return "Moderately severe depression."
            else:
                return "Severe depression."
        elif assessment_title == "GAD-7 Anxiety Assessment":
            if score <= 4:
                return "Minimal anxiety."
            elif score <= 9:
                return "Mild anxiety."
            elif score <= 14:
                return "Moderate anxiety."
            else:
                return "Severe anxiety."
        # Add more assessment-specific logic here...
        return "Assessment completed."

class AssessmentListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        assessments = Assessment.objects.all()
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific assessment
class AssessmentDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return None

    def get(self, request, pk):
        assessment = self.get_object(pk)
        if not assessment:
            return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssessmentSerializer(assessment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        assessment = self.get_object(pk)
        if not assessment:
            return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssessmentSerializer(assessment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        assessment = self.get_object(pk)
        if not assessment:
            return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)
        assessment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# List and Create Forum Posts
class ForumPostListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = ForumPost.objects.all().order_by('-created_at')
        serializer = ForumPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ForumPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Retrieve, Update, Delete Forum Post
class ForumPostDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(ForumPost, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = ForumPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.user != request.user:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ForumPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.user != request.user:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'detail': 'Post deleted'},status=status.HTTP_204_NO_CONTENT)
    
# Like a Post
class ForumPostLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(ForumPost, pk=pk)
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)
    
# Comment on a Post
class ForumPostCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(ForumPost, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and Create Comments
class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        post_id = request.query_params.get('post_id')
        # comments = Comment.objects.all()
        comments = Comment.objects.filter(post_id=post_id) if post_id else Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = CommentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and Create Tags
class TagListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access the dashboard
        
    def get(self, request):
            # Render the dashboard page
        return render(request, 'dashboard.html')
    
