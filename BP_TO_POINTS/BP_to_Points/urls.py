"""BP_to_Points URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from POINTS_APP import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.Signup, name='HOME PAGE'),
    path('login/', views.Userlogin, name='UserLogin'),
    path('logout/', views.logoutUser, name='logoutUser'),

###################### U S E R #########################
    path('about/', views.about, name='about'),
    path('userhomescreen/', views.UserHomescreen, name='userhomescreen'),
    path('Rewards/', views.Rewards, name='Rewards'),
    path('RewardsSelection/<str:pk>/', views.Rewards_selection, name='Rewards_selection'),
    path('RewardsHistory/', views.User_Rewards_History, name='User_Rewards_History'),
    path('PDF_Rewards_History/', views.PDF_User_Rewards_History, name='PDF_Rewards_History'),
    path('TransactionHistory/', views.User_Transaction_History, name='User_Transaction_History'),
    path('PDFTransactionHistory/', views.PDF_User_Transaction_History, name='PDF_User_Transaction_History'),
    # path('verify/<str:pk>/', views.verify, name='verify'),

###################### A D M I N #########################
    path('AdminPage/', views.Admin_Page, name='Admin_Page'),
    path('PDFAdminPage/', views.PDF_Admin_Page, name='PDF_Admin_Page'),
    path('AdminRewardsHistory/', views.Admin_Rewards_History, name='Admin_Rewards_History'),
    path('PDFAdminRewardsHistory/', views.PDF_Admin_Rewards_History, name='Pdf_Admin_Rewards_History'),
    path('delete1/<str:pk>/', views.delete1, name='delete_1'), #Rewards Delete#
    path('delete2/<str:pk>/', views.delete2, name='delete_2'), #Transaction Delete#
    path('Notifdelete/<str:pk>/', views.Notification_Deletes, name='Notification_Delete'), #Notification Delete#


#ADMIN REWARDS QUEUE
    path('AdminRewardsQueue/', views.Admin_Rewards_Queue1, name='Admin_Rewards_Queue'),
    path('delete/<str:pk>/', views.delete, name='delete'),

#ADMIN SETTINGS
    path('AdminSettings/', views.Admin_Settings, name='Admin_Settings'),
    path('AdminRewardsSettings/', views.Admin_Rewards_Settings, name='Admin_Rewards_Settings'),
    path('deletes/<str:pk>/', views.Rewards_Settings_delete, name='deletes'),
    path('AdminAddRewardsSettings/', views.Rewards_Settings_add, name='Rewards_Settings_add'),
    path('updates/<str:pk>/', views.Rewards_Settings_update, name='updates'),

#KIOSK MACHINE
    path('PaperExchange/', views.Paper_Exchange, name='Paperexchange'),
    path('BottleExchange/', views.Bottle_Exchange, name='Bottleexchange'),
    path('Kiosk_Homescreen/', views.Kiosk_Home, name='Kiosk_Homescreen'),
    path('kioskfirstpage/', views.Kiosk_First_Page, name='Kiosk_First_Page'),
    path('Kiosk_login/', views.Kiosk_Login, name='Kiosk_Login1'),
    path('kiosklogout/', views.kiosklogoutUser, name='kiosklogoutuser'),
    path('kioskpapernote/', views.Kiosk_Paper_Note, name='Kiosk_papernote'),
    path('kioskbottlenote/', views.Kiosk_Bottle_Note, name='Kiosk_bottlenote'),
    path('kioskabout/', views.kiosk_about, name='Kiosk_about'),
    path('BottleAuth/', views.Bottle_Auth, name='Bottleauth'),
    # path('PaperDone/', views.Paper_Done, name='Paper_Done'),

    # Orig Paper Exchange 
    path('PaperExchangeorig/', views.Paper_Exchange_Orig, name='PaperexchangeOrig'),

]
