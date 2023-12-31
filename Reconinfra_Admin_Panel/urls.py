from django.urls import path
from .import views

urlpatterns = [
    path('', views.Admin_Panel_Home, name="admin_dashboard" ),
    path('add-property', views.AddProperties, name="AddProperties" ),
    path('property-list', views.PropertyList, name="PropertyList" ),
    path('edit-property/<int:pk>', views.UpdatePropertiesView, name="UpdatePropertiesView" ),
    path('delete-plot/<int:pk>', views.DeletePlotView, name="DeletePlotView" ),
    path('add-plot-images', views.AddPlotImages, name="AddPlotImages" ),
    path('plot-image-list', views.PlotImagesList, name="PlotImagesList" ),
    path('delete-plot-image/<int:pk>', views.DeletePlotImage, name="DeletePlotImage" ),
    path('update-plot-image/<int:pk>', views.UpdatePlotImage, name="UpdatePlotImage" ),
    path('add-gallery-images', views.AddGalleryImage, name="AddGalleryImage" ),
    path('list-gallery-images', views.ListGalleryImages, name="ListGalleryImages" ),
    path('delete-gallery-images/<int:pk>', views.DeleteImageView, name="DeleteImageView" ),
    path('add-plot-availability', views.AddPlotAvailability, name="AddPlotAvailability" ),
    path('my-orders', views.MyOrdersView, name="MyOrdersView" ),
    path('get-agent-booked-details/', views.getAgentBookedDetailsView, name="getAgentBookedDetailsView" ),
    path('booking-history', views.BookingHistoryView, name="BookingHistoryView" ),
    path('add-reward', views.AddRewardView, name="AddRewardView" ),
    path('reward-list', views.RewardListView, name="RewardListView" ),
    path('update-reward/<int:pk>', views.UpdateRewardView, name="UpdateRewardView" ),
    path('delete-reward/<int:pk>', views.DeleteRewardView, name="DeleteRewardView" ),
    path('facilitator-list', views.FacilitatorListView, name="FacilitatorListView" ),
    path('transfer-request', views.TransferRequestView, name="TransferRequestView" ),
    path('transfer-request-list', views.TransferRequestListView, name="TransferRequestListView" ),
    path('withdrawals-list', views.WithdrawalsRequestListView, name="WithdrawalsRequestListView" ),
    path('view-withdrawals-details/<int:transfer_request_id>', views.ViewAgentWithrawalsDetailsView, name="ViewAgentWithrawalsDetailsView" ),
    path('activate-id', views.ActivateIdView, name="ActivateIdView" ),
    path('plot-booking', views.PlotBookingView, name="PlotBookingView" ),
    path('update-booking-plot/<int:booking_id>', views.UpdateBookingPlot, name="UpdateBookingPlot" ),
    path('delete-booking-plot/<int:booking_id>', views.DeleteBookingView, name="DeleteBookingView" ),
    path('my-team-tree', views.MyTreeTeamView, name="MyTreeTeamView" ),
    path('get-teams', views.GetAllUsersView, name="GetAllUsersView" ),
    path('emi-history', views.EMIHistoryView, name="EMIHistoryView" ),
    path('pay-emi', views.PayEMIView, name="PayEMIView" ),
    path('my-wallet', views.MyWalletView, name="MyWalletView" ),
]
