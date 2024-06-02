from django.urls import path
from .views import SignupView, LoginView, SearchUserView, FriendRequestView, ManageFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchUserView.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:id>/<str:action>/', ManageFriendRequestView.as_view(), name='manage-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='pending-requests'),
]
