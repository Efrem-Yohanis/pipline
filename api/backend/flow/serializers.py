from rest_framework import serializers
from .models import Flow, Node, SubNode, SubNodeParameter, Edge

class SubNodeParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubNodeParameter
        fields = ['id', 'subnode', 'key', 'value', 'value_type']

class SubNodeSerializer(serializers.ModelSerializer):
    parameters = SubNodeParameterSerializer(many=True)

    class Meta:
        model = SubNode
        fields = ['id', 'name', 'is_active', 'is_deployed', 'parameters']

    def create(self, validated_data):
        params_data = validated_data.pop('parameters')
        subnode = SubNode.objects.create(**validated_data)
        for param in params_data:
            SubNodeParameter.objects.create(subnode=subnode, **param)
        return subnode

    def update(self, instance, validated_data):
        params_data = validated_data.pop('parameters')
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_deployed = validated_data.get('is_deployed', instance.is_deployed)
        instance.save()

        # Update parameters: delete all and recreate
        instance.parameters.all().delete()
        for param in params_data:
            SubNodeParameter.objects.create(subnode=instance, **param)
        return instance

class NodeSerializer(serializers.ModelSerializer):
    subnodes = SubNodeSerializer(many=True)

    class Meta:
        model = Node
        fields = ['id', 'name', 'subnodes']

    def create(self, validated_data):
        subnodes_data = validated_data.pop('subnodes')
        node = Node.objects.create(**validated_data)
        for subnode_data in subnodes_data:
            parameters_data = subnode_data.pop('parameters')
            subnode = SubNode.objects.create(node=node, **subnode_data)
            for param_data in parameters_data:
                SubNodeParameter.objects.create(subnode=subnode, **param_data)
        return node

    def update(self, instance, validated_data):
        subnodes_data = validated_data.pop('subnodes')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # update subnodes: delete all and recreate
        instance.subnodes.all().delete()
        for subnode_data in subnodes_data:
            parameters_data = subnode_data.pop('parameters')
            subnode = SubNode.objects.create(node=instance, **subnode_data)
            for param_data in parameters_data:
                SubNodeParameter.objects.create(subnode=subnode, **param_data)
        return instance

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['id', 'source', 'target', 'edge_type']

class FlowSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True)
    edges = EdgeSerializer(many=True)

    class Meta:
        model = Flow
        fields = ['id', 'name', 'is_running', 'is_deployed', 'deployed_at', 'created_at', 'nodes', 'edges']

    def create(self, validated_data):
        nodes_data = validated_data.pop('nodes')
        edges_data = validated_data.pop('edges')
        flow = Flow.objects.create(**validated_data)
        for node_data in nodes_data:
            subnodes_data = node_data.pop('subnodes')
            node = Node.objects.create(flow=flow, **node_data)
            for subnode_data in subnodes_data:
                params_data = subnode_data.pop('parameters')
                subnode = SubNode.objects.create(node=node, **subnode_data)
                for param_data in params_data:
                    SubNodeParameter.objects.create(subnode=subnode, **param_data)
        for edge_data in edges_data:
            Edge.objects.create(flow=flow, **edge_data)
        return flow

    def update(self, instance, validated_data):
        nodes_data = validated_data.pop('nodes')
        edges_data = validated_data.pop('edges')

        instance.name = validated_data.get('name', instance.name)
        instance.is_running = validated_data.get('is_running', instance.is_running)
        instance.is_deployed = validated_data.get('is_deployed', instance.is_deployed)
        instance.deployed_at = validated_data.get('deployed_at', instance.deployed_at)
        instance.save()

        # Delete all existing nodes and edges and recreate (simplest way)
        instance.nodes.all().delete()
        instance.edges.all().delete()

        for node_data in nodes_data:
            subnodes_data = node_data.pop('subnodes')
            node = Node.objects.create(flow=instance, **node_data)
            for subnode_data in subnodes_data:
                params_data = subnode_data.pop('parameters')
                subnode = SubNode.objects.create(node=node, **subnode_data)
                for param_data in params_data:
                    SubNodeParameter.objects.create(subnode=subnode, **param_data)
        for edge_data in edges_data:
            Edge.objects.create(flow=instance, **edge_data)

        return instance
