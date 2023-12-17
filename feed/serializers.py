from feed.models import Feed, FeedImage, FeedAction, FeedActionComment
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class FeedSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()
    userBio = SerializerMethodField()
    isLiked = SerializerMethodField()
    likesCount = SerializerMethodField()
    commentsCount = SerializerMethodField()
    sharesCount = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Feed
        fields = ['id', 'subject', 'body', 'user', 'isPublic', 'createdAt', 'updatedAt', 'userName', 'userBio', 'profilePicture', 'isLiked', 'likesCount', 'commentsCount', 'sharesCount', 'images']
        list_fields = fields
        get_fields = fields

    def get_userName(self, obj):
        return (obj.user.firstName or "") + " " + (obj.user.lastName or "")
    
    def get_userBio(self, obj):
        DEPARTMENTS = {
            "1": "Computer Engineering",
            "2": "Mechanical Engineering",
            "3": "Electronics & Telecommunication Engineering",
            "4": "Electrical Engineering",
            "5": "Information Technology",
            "6": "Artificial Intelligence & Data Science",
            "7": "First Year Engineering",
            "8": "MBA"
        }
        if obj.user.bio == '' or obj.user.bio == "" or obj.user.bio == None:
            if obj.user.is_superuser or obj.user.privilege == "Super Admin":
                return "Superuser at MMCOE"
            if obj.user.privilege == "Alumni":
                return "Batch of " + str(obj.user.alumni.batch) + " | " + DEPARTMENTS[obj.user.department]
            elif obj.user.privilege == "Student":
                return "Batch of " + str(obj.user.student.batch) + " | " + DEPARTMENTS[obj.user.department]
            elif obj.user.privilege == "Staff":
                return "Professor at MMCOE | " + obj.user.department
            else:
                return "MMCOE Alumni Portal User"
        else:
            return obj.user.bio
        

    def get_profilePicture(self, obj):
        return obj.user.profilePicture or ""
    
    def get_isLiked(self, obj):
        return obj.actions.filter(action='LIKE', user=self.context['request'].user).exists()
    
    def get_likesCount(self, obj):
        return obj.actions.filter(action='LIKE').count()
    
    def get_commentsCount(self, obj):
        return obj.actions.filter(action='COMMENT').count()
    
    def get_sharesCount(self, obj):
        return obj.actions.filter(action='SHARE').count()
    
    def get_images(self, obj):
        feed = Feed.objects.get(id=obj.id)
        images = feed.images.all()
        return FeedImageSerializer(images, many=True).data


class FeedImageSerializer(ModelSerializer):
    feedName = SerializerMethodField()

    class Meta:
        model = FeedImage
        fields = ['id', 'image', 'coverImage', 'createdAt', 'updatedAt', 'feedName']
        list_fields = ['id', 'image', 'coverImage', 'createdAt', 'updatedAt', 'feedName']
        get_fields = ['id', 'image', 'coverImage', 'createdAt', 'updatedAt', 'feedName']

    def get_feedName(self, obj):
        return obj.feed.subject


class FeedActionSerializer(ModelSerializer):
    feedName = SerializerMethodField()
    userName = SerializerMethodField()

    class Meta:
        model = FeedAction
        fields = ['id', 'feed', 'action', 'user', 'createdAt', 'updatedAt', 'feedName', 'userName']
        list_fields = ['id', 'feed', 'action', 'user', 'createdAt', 'updatedAt', 'feedName', 'userName']
        get_fields = ['id', 'feed', 'action', 'user', 'createdAt', 'updatedAt', 'feedName', 'userName']

    def get_feedName(self, obj):
        return obj.feed.subject

    def get_userName(self, obj):
        return (obj.user.firstName or "") + " " + (obj.user.lastName or "")


class FeedActionCommentSerializer(ModelSerializer):
    feedName = SerializerMethodField()
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()

    class Meta:
        model = FeedActionComment
        fields = ['id', 'feedAction', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']
        list_fields = ['id', 'feedAction', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']
        get_fields = ['id', 'feedAction', 'comment', 'createdAt', 'updatedAt', 'feedName', 'userName', 'profilePicture']

    def get_feedName(self, obj):
        return obj.feedAction.feed.subject

    def get_userName(self, obj):
        return (obj.feedAction.user.firstName or "") + " " + (obj.feedAction.user.lastName or "")

    def get_profilePicture(self, obj):
        return obj.feedAction.user.profilePicture or ""
