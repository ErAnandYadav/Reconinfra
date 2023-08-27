


from django.urls import path
from .import views

urlpatterns = [
    path('', views.Home, name="Home" ),
    path('about-company/',views.ReconinfraAboutUs, name="ReconinfraAboutUs"),
    path('legal-documents/',views.LegalsDocuments, name="LegalsDocuments"),
    path('golden-city-plot-availability/',views.GoldenCityPlotAvailability, name="GoldenCityPlotAvailability"),
    path('green-valley-plot-availability/',views.GreenValleyPlotAvailability, name="GreenValleyPlotAvailability"),
    path('contact-us/', views.ReconinfraContactUs, name="ReconinfraContactUs"),
    path('company-mission-and-vision/', views.MissionandVision, name="MissionandVision"),
    path('property-details/<str:slug>/', views.PropertiesDetailsView, name="PropertyDetails"),
    path('media-canter/', views.ReconinfraImageGallery, name="ReconinfraImageGallery"),
    path('terms-and-conditions/', views.ReconinfraTermsAndConditions, name="ReconinfraTermsAndConditions"),
    path('privacy-policy/', views.ReconinfraPrivacyPolicy, name="ReconinfraPrivacyPolicy"),
    path('disclaimer/', views.ReconinfraDisclaimer, name="ReconinfraDisclaimer"),
    path('customer-login/', views.CustomerLogin, name="CustomerLogin"),
    path('customer-profile/', views.CustomerProfile, name="CustomerProfile"),
]
