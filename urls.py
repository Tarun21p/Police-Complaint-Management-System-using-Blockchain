from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
	       path('PoliceLogin.html', views.PoliceLogin, name="PoliceLogin"), 
	       path('PoliceLoginAction', views.PoliceLoginAction, name="PoliceLoginAction"),
	       path('AddNewPolice.html', views.AddNewPolice, name="AddNewPolice"),
	       path('AddNewPoliceAction', views.AddNewPoliceAction, name="AddNewPoliceAction"),
	       path('ViewPolice', views.ViewPolice, name="ViewPolice"),	
	       path('AddFir.html', views.AddFir, name="AddFir"),
	       path('AddFirAction', views.AddFirAction, name="AddFirAction"),
	       path('UpdateInvestigations.html', views.UpdateInvestigations, name="UpdateInvestigations"),
	       path('UpdateInvestigationsAction', views.UpdateInvestigationsAction, name="UpdateInvestigationsAction"),
	       path('DownloadAction', views.DownloadAction, name="DownloadAction"),
	       path('ViewInvestigations', views.ViewInvestigations, name="ViewInvestigations"),
	       path('ViewReports', views.ViewReports, name="ViewReports"),
]