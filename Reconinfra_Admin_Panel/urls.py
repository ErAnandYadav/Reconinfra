from django.urls import path
from .import views

urlpatterns = [
    path('', views.Admin_Panel_Home, name="admin_dashboard" ),
    path('add-property', views.AddProperties, name="AddProperties" ),
    path('property-list', views.PropertyList, name="PropertyList" ),
    path('delete-plot/<int:pk>', views.DeletePlotView, name="DeletePlotView" ),
    path('add-plot-images', views.AddPlotImages, name="AddPlotImages" ),
    path('add-gallery-images', views.AddGalleryImage, name="AddGalleryImage" ),
    path('list-gallery-images', views.ListGalleryImages, name="ListGalleryImages" ),
    path('delete-gallery-images/<int:pk>', views.DeleteImageView, name="DeleteImageView" ),
    path('add-plot-availability', views.AddPlotAvailability, name="AddPlotAvailability" ),
    
    path('booking-list', views.BookingList, name="BookingList" ),
    path('update-booking-plot/<int:booking_id>', views.UpdateBookingPlot, name="UpdateBookingPlot" ),
    path('get-agent-booked-details/', views.getAgentBookedDetailsView, name="getAgentBookedDetailsView" ),
    path('add-payment', views.AddPaymentView, name="AddPaymentView" ),
    path('payment-history', views.PaymentHistoryView, name="PaymentHistoryView" ),
    path('add-reward', views.AddRewardView, name="AddRewardView" ),
    path('reward-list', views.RewardListView, name="RewardListView" ),
    path('facilitator-list', views.FacilitatorListView, name="FacilitatorListView" ),
    path('transfer-request', views.TransferRequestView, name="TransferRequestView" ),
    path('transfer-request-list', views.TransferRequestListView, name="TransferRequestListView" ),
    path('withdrawals-list', views.WithdrawalsRequestListView, name="WithdrawalsRequestListView" ),
    path('view-withdrawals-details/<int:transfer_request_id>', views.ViewAgentWithrawalsDetailsView, name="ViewAgentWithrawalsDetailsView" ),
    path('activate-id', views.ActivateIdView, name="ActivateIdView" ),
    path('plot-booking', views.PlotBookingView, name="PlotBookingView" ),

]
