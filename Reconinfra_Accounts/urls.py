


from django.urls import path
from .import views

urlpatterns = [
    path('auth-logout/', views.LogoutView, name="LogoutView" ),
    path('auth-login/', views.LoginView, name="AuthLogin" ),
    path('auth-register/', views.UserRegister, name="Register" ),
    path('referral-link/<str:sponsor_id>', views.ReferralLinkView, name="ReferralLinkView" ),
    path('user-profile/<str:id>/', views.Profile, name="Profile" ),
    path('associate-details/<str:id>/', views.AssociateDetails, name="AssociateDetails" ),
    path('update-bank-details/', views.UpdateBankDetails, name="UpdateBankDetails" ),
    path('change-profile-picture/', views.ChangeProfilePicture, name="ChangeProfilePicture" ),
    path('my-teams/', views.MyTeamsView, name="MyTeamsView" ),
    path('teams-details/<str:account_id>/', views.TeamDetailsView, name="TeamDetailsView" ),
    path('search-team/', views.SearchTeamsView, name="SearchTeamsView" ),
    path('forget-password/', views.ForgetPasswordView, name="ForgetPasswordView" ),
    path('change-password/<token>/', views.ChangePasswordView, name="ChangePasswordView" ),
    path('create-group/', views.CreateGroupView, name="CreateGroupView" ),
    path('group-list/', views.GroupListView, name="GroupListView" ),
    path('assign-group/', views.AssignGroupView, name="AssignGroupView" ),
    path('initialize-group-list/', views.InitializeGroupListView, name="InitializeGroupListView" ),
    path('group-details/<pk>/', views.GroupsAgentListView, name="GroupsAgentListView" ),
    path('edit-facilitator/<str:pk>', views.EditFacilitatorView, name="EditFacilitatorView" ),
    path('get-associate-name/<str:sponsor_id>', views.getAssociateNameBySponsorIdView, name="getAssociateNameBySponsorIdView" ),
    path('export_users_to_csv', views.export_users_to_csv, name="export_users_to_csv" ),
]
