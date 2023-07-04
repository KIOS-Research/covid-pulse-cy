from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'pulseapp'

urlpatterns = [
    path('index/', views.index, name='index'),
    path ('sampledata/', views.sampledata, name = 'sampledata'),
    path ('trendsdata/', views.TrendsView, name = 'trendsdata'),
    path ('variantsdata/', views.VariantsView, name = 'variantsdata'),
    path ('viewsampledata/', views.viewsampledata, name = 'viewsampledata'),
    path ('viewwwmeasure/', views.viewwwmeasure, name = 'viewwwmeasure'),
    path ('viewtrends/', views.viewTrendsData, name = 'viewtrends'),
    path ('viewvariants/', views.viewVariantsData, name = 'viewvariants'),
    path ('viewvariantstype/', views.viewVariantsTypeData, name = 'viewvariantstype'),
    path ('addvariantstype/', views.AddVariantsTypeView, name = 'addvariantstype'),
    url (r'^viewsampledataListJson/$', views.viewsampledataListJson.as_view (), name = "viewsampledataListJson"),
    url (r'^viewwwmeasureListJson/$', views.viewwwmeasureListJson.as_view (), name = "viewwwmeasureListJson"),
    url (r'^viewtrendsdataListJson/$', views.viewtrendsdataListJson.as_view (), name = "viewtrendsdataListJson"),
    url (r'^viewvariantsdataListJson/$', views.viewvariantsdataListJson.as_view (), name = "viewvariantsdataListJson"),
    url (r'^viewvariantstypeListJson/$', views.viewvariantstypeListJson.as_view (), name = "viewvariantstypeListJson"),
    path('viewsampledata/export/', views.exportFile, name='exportFile'),
    path('viewwwmeasure/export/', views.exportFile, name='exportFile'),
    path ('viewtrends/export/', views.exportFileTrends, name = 'exportFileTrends'),
    path ('viewvariants/export/', views.exportFileVariants, name = 'exportFileVariants'),

    path ('viewsampledata/delete/', views.deleteEntrySampleData, name = 'deleteEntrySampleData'),
    path ('viewwwmeasure/delete/', views.deleteEntryWWWMeasure, name = 'deleteEntry'),
    path ('viewtrends/delete/', views.deleteEntryTrendsData, name = 'deleteEntryTrendsData'),
    path ('viewvariants/delete/', views.deleteEntryVariantsData, name = 'deleteEntryVariantsData'),
    path ('viewvariantstype/delete/', views.deleteEntryVariantsTypeData, name = 'deleteEntryVariantsTypeData'),
    path ('viewsampledata/edit/<int:pk>/', views.SampleEditView, name = 'sampledataedit'),
    path ('viewwwmeasure/edit/<int:pk>/', views.MeasurementsEditView, name = 'measureedit'),
    path ('viewtrends/edit/<int:pk>/', views.EditTrendsView, name = 'trendsedit'),
    path ('viewvariants/edit/<int:pk>/', views.VariantsEditView, name = 'variantsedit'),
    path ('viewvariantstype/edit/<int:pk>/', views.VariantsTypeEditView, name = 'variantstypeedit'),
    path ('change_password/', views.change_password, name = 'changePass'),

]