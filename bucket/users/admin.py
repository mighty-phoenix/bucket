from django.contrib import admin
from users.models import BucketUser, FollowUser, Bookmark


admin.site.register(BucketUser)
admin.site.register(FollowUser)
admin.site.register(Bookmark)
