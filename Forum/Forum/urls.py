from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAuthenticated
from Brico_depot import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin


# Initialize the router and register your viewsets
router = DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'follows', views.FollowViewSet)
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'messages', views.PrivateMessageViewSet)

from rest_framework.views import APIView
from rest_framework.response import Response

class MaVueProtegee(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Cette vue est protégée. Vous êtes authentifié !"})
    
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="BricoDepot API",
      default_version='v1',
      description="API pour le forum de bricolage",
   ),
   public=True,
   permission_classes=(AllowAny,),
)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vue_protegee(request):
    return Response({"message": "Accès restreint aux utilisateurs authentifiés."})



# Combine all URL patterns into a single list
urlpatterns = [
    path('admin/', admin.site.urls),  # Chemin pour l'administration
    path('api/register/', views.register_view, name='register'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('vue_protegee/', vue_protegee, name='vue_protegee'),
    path('mavueprotegee/', MaVueProtegee.as_view(), name='mavueprotegee'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
]

