from django.contrib import admin
from users.models import BucketUser, Recommendation, Bookmark


admin.site.register(BucketUser)
admin.site.register(Recommendation)
admin.site.register(Bookmark)
