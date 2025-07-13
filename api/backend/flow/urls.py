from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NodeViewSet, SubNodeViewSet, SubNodeParameterViewSet, FlowViewSet

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'subnodes', SubNodeViewSet)
router.register(r'parameters', SubNodeParameterViewSet)
router.register(r'flows', FlowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

