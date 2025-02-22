from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Assessment, UserAssessment, SelfCareContent, Challenge, UserChallenge, Question, Option, ForumPost, Comment, PostLike, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['id', 'anon_username', 'email', 'is_active', 'date_joined']
        fields = [
            'id', 'anon_username', 'email', 'total_score', 'streak',
            'level', 'is_active', 'is_staff', 'date_joined', 'last_login'
        ]

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['anon_username', 'email', 'password']

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return CustomUser.objects.create(**validated_data)

# - - - - - - - - - - - - - - - - - - - - - -   actual
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)

#     class Meta:
#         model = CustomUser
#         # fields = ['anon_username', 'email', 'password']
#         fields = ['email', 'password']
        # - - - - - - - - - - - - - - - - - - - actual

class UserRegistrationSerializer(serializers.ModelSerializer):
    anon_username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)
    suggestion = serializers.CharField(read_only=True)  # New field for suggestion

    class Meta:
        model = CustomUser
        fields = ['anon_username', 'email', 'password', 'suggestion']

    # def validate_anon_username(self, value):
    #     if value and CustomUser.objects.filter(anon_username=value).exists():
    #         suggested_username = CustomUser.objects.generate_anon_username()
    #         self._suggested_username = suggested_username  # Store it for later use
    #     return value

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Add suggestion to response if it exists
    #     if hasattr(self, '_suggested_username'):
    #         data['suggestion'] = f"Username already taken. Suggested: {self._suggested_username}"
    #     return data

    def validate_email(self, value):
        if value:
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        anon_username = validated_data.pop('anon_username', None) or CustomUser.objects.generate_anon_username()
        user = CustomUser.objects.create_user(
            anon_username=anon_username,
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        return user


# -----------------------------------------------
    # def create(self, validated_data):
    #     user = CustomUser(
    #         anon_username=validated_data['anon_username'],
    #         email=validated_data['email']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    # ----------------------------------------------------------------
    # - - -  - - - - - - - - - - - - - - - -actual
    # def validate_email(self, value):
    #     if CustomUser.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("A user with this email already exists.")
    #     return value
    
    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #         # anon_username=validated_data['anon_username'],
    #         email=validated_data['email'],
    #         password=str(validated_data['password'])
    #     )
    #     return user
    # - - - - - - - - - - - - - - - - - - -actual

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'anon_username', 'total_score', 'streak', 'level']



class UserAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssessment
        fields = ['id', 'user', 'assessment', 'score', 'completed_at']

class SelfCareContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfCareContent
        fields = ['id', 'title', 'content_type', 'content_url', 'description', 'created_at']

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'points', 'created_at']

class UserChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChallenge
        fields = ['id', 'user', 'challenge', 'completed_at', 'points_earned']

# Option Serializer
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'text', 'score']

# Question Serializer
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'assessment', 'text', 'options']

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'created_at', 'questions']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show user's anon_username

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class ForumPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)


    class Meta:
        model = ForumPost
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'comments', 'likes_count', 'tags', 'tag_names']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def create(self, validated_data):
        # Extract tag_names from the request
        # tag_names = validated_data.pop('tag_names', [])
        tags_data = self.context['request'].data.get('tags', [])
        # post = ForumPost.objects.create(**validated_data)
        post = ForumPost.objects.create(
        user=self.context['request'].user,
        title=validated_data.get('title'),
        content=validated_data.get('content')
    )
        # Handle tags: link existing or create new
        # for tag_name in tag_names:
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            post.tags.add(tag)

        return post
    
    def update(self, instance, validated_data):
        # Allow updating tags if provided
        tag_names = validated_data.pop('tag_names', None)

        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_names is not None:
            # Clear existing tags and add new ones
            instance.tags.clear()
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                instance.tags.add(tag)

        return instance

class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'created_at']
