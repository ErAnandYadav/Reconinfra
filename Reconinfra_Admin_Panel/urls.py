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
    path('add-reward', views.AddRewardView, name="AddRewardView" ),
    path('reward-list', views.RewardListView, name="RewardListView" ),
    path('associate-reward-list', views.AssociateRewardListView, name="AssociateRewardListView" ),
    path('update-reward/<int:pk>', views.UpdateRewardView, name="UpdateRewardView" ),
    path('delete-reward/<int:pk>', views.DeleteRewardView, name="DeleteRewardView" ),
    path('facilitator-list', views.FacilitatorListView, name="FacilitatorListView" ),
    path('transfer-request', views.TransferRequestView, name="TransferRequestView" ),
    path('transfer-request-list', views.TransferRequestListView, name="TransferRequestListView" ),
    path('payout-transfer', views.PayoutTransferView, name="PayoutTransferView" ),
    path('view-withdrawals-details/<int:transfer_request_id>', views.ViewAgentWithrawalsDetailsView, name="ViewAgentWithrawalsDetailsView" ),
    path('activate-id', views.ActivateIdView, name="ActivateIdView" ),
    path('plot-booking', views.PlotBookingView, name="PlotBookingView" ),
    path('booking-history', views.BookingHistoryView, name="BookingHistoryView" ),
    path('saved-booking-form', views.SavedBookingFormView, name="SavedBookingFormView" ),
    path('add-payment/<str:booking_id>', views.AddPaymentView, name="AddPaymentView" ),
    path('view-booking-history/<int:booking_id>', views.ViewBookingHistory, name="ViewBookingHistory" ),
    path('update-saved-form/<int:booking_id>', views.UpdateSavedForm, name="UpdateSavedForm" ),
    path('delete-saved-form/<int:booking_id>', views.DeleteSavedFormView, name="DeleteSavedFormView" ),
    path('team-tree-view', views.TreeTeamView, name="TreeTeamView" ),
    path('get-teams', views.GetAllUsersView, name="GetAllUsersView" ),
    path('emi-history', views.EMIHistoryView, name="EMIHistoryView" ),
    # path('pay-emi', views.PayEMIView, name="PayEMIView" ),
    path('emi-pay/<int:pk>', views.EMIPay, name="EMIPay" ),
    path('my-wallet', views.MyWalletView, name="MyWalletView" ),
    path('my-team-size', views.TeamsSizeView, name="TeamsSizeView" ),
    path('choose-plot', views.ChoosePlot, name="ChoosePlot" ),
    path('update-plot-availability/<int:plot_id>', views.UpdatePlotAvailability, name="UpdatePlotAvailability" ),
    path('test-api', views.TestAllInOneAPI, name="TestAllInOneAPI" ),
]
