from django.urls import path,include
from ADRF.views import employee,login,PersonAPI,PeopleViewSet,RegisterAPI,LoginAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginAPI.as_view()),
    path('employee/',employee),
    path('register/',RegisterAPI.as_view()),
    path('login/',login),
    path('persons/',PersonAPI.as_view())
]
