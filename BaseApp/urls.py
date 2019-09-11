from django.urls import path, include
from WebApp.views import (HomePage,
                          RegisterPage,
                          DilemmaPage,
                          FamilyAuthPage,
                          FamilyMemberPage,
                          ActivationPage,
                          RegisterFamily,
                          CreateDutyPage)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',
         auth_views.LoginView.as_view(template_name='WebApp/Login.html'),
         name='LoginPagePath'),
    path('createduty/', CreateDutyPage.as_view(), name='CreateDutyPagePath'),
    path('home/', HomePage.as_view(), name='HomePagePath'),
    path('register/', include([
         path('', RegisterPage.as_view(), name='RegPagePath'),
         path('registerfamily/',
              RegisterFamily.as_view(),
              name='RegFamilyPage'),
         path('<slug:id>', ActivationPage.as_view(), name='ActivePagePath'),
         ])),
    path('dilemma/', DilemmaPage.as_view(), name='DilemmaPagePath'),
    path('familyauth/', FamilyAuthPage.as_view(), name='FamilyAuthPagePath'),
    path('regfamilymeminfo/',
         FamilyMemberPage.as_view(),
         name='FamilyMemberPagePath'),
    path('activation/<str:id>/',
         ActivationPage.as_view(),
         name='ActivationPagePath'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='WebApp/Logout.html'),
         name='LogoutPagePath'),
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
