from django.urls import path
from .views import MyProfileView, PublicProfileView, AvatarUploadView, AvailabilityToggleView, PresenceHeartbeatView

urlpatterns = [
    path('', MyProfileView.as_view()),
    path('avatar/', AvatarUploadView.as_view()),
    path('availability/', AvailabilityToggleView.as_view()),
    path('presence/', PresenceHeartbeatView.as_view()),
    path('<uuid:user_id>/', PublicProfileView.as_view()),
]

from .views import MentorListView, MentorOrgListView

urlpatterns += [
    path('mentors/', MentorListView.as_view()),
    path('mentors/organizations/', MentorOrgListView.as_view()),
]
