from rest_framework import viewsets
from .models import Node, SubNode, SubNodeParameter
from .serializers import NodeSerializer, SubNodeSerializer, SubNodeParameterSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Flow
from .serializers import FlowSerializer
from django.utils.timezone import now

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class SubNodeViewSet(viewsets.ModelViewSet):
    queryset = SubNode.objects.all()
    serializer_class = SubNodeSerializer


class SubNodeParameterViewSet(viewsets.ModelViewSet):
    queryset = SubNodeParameter.objects.all()
    serializer_class = SubNodeParameterSerializer






class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        flow = self.get_object()
        flow.is_deployed = True
        flow.deployed_at = now()
        flow.save()
        return Response({"status": "deployed", "flow_id": flow.id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def undeploy(self, request, pk=None):
        flow = self.get_object()
        flow.is_deployed = False
        flow.save()
        return Response({"status": "undeployed", "flow_id": flow.id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        flow = self.get_object()
        if not flow.is_deployed:
            return Response({"error": "Flow must be deployed before starting"}, status=status.HTTP_400_BAD_REQUEST)
        flow.is_running = True
        flow.save()
        return Response({"status": "started", "flow_id": flow.id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        flow = self.get_object()
        flow.is_running = False
        flow.save()
        return Response({"status": "stopped", "flow_id": flow.id}, status=status.HTTP_200_OK)
