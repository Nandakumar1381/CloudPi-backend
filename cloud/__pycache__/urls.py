from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='documents'

urlpatterns=[
    path('upload/',views.document_view_upload,name='document_list'),
    path('<int:pk>/delete/',views.document_delete,name='document_delete'),
    path('<int:pk>/add_to_starred/',views.add_to_starred,name='add-to-starred'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)