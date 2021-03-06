from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'date_joined', 'first_name', 'last_name', 'email')


class ClubSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.Club
        fields = ('id', 'name', 'description')


class ClubRoleSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = models.ClubRole
        fields = ('id', 'name', 'description', 'club', 'privilege', 'members')


class ClubDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = models.Club
        fields = ('id', 'name', 'description', 'members')

    def get_members(self, obj):
        queryset = models.User.objects.filter(clubrole__club=obj)
        serializer = UserSerializer(instance=queryset, many=True)
        return serializer.data


class ProjectSerializer(serializers.ModelSerializer):
    started = serializers.ReadOnlyField()

    class Meta:
        model = models.Project
        fields = ('id', 'name', 'description', 'started', 'closed', 'leader', 'members', 'clubs')


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = ('id', 'name', 'description', 'club')


class PostSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = models.Post
        fields = ('id', 'content', 'created', 'channel')


class ConversationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    created = serializers.ReadOnlyField()

    class Meta:
        model = models.Conversation
        fields = ('id', 'content', 'created', 'channel', 'author', 'parent')


class FeedbackSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = models.Feedback
        fields = ('id', 'content', 'created', 'club', 'author')


class FeedbackReplySerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = models.FeedbackReply
        fields = ('id', 'content', 'created', 'parent')
