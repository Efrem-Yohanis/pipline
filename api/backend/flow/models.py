from django.db import models
import uuid

class ValueType(models.TextChoices):
    STRING = 'string', 'String'
    INTEGER = 'integer', 'Integer'
    BOOLEAN = 'boolean', 'Boolean'
    FLOAT = 'float', 'Float'

class Flow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_running = models.BooleanField(default=False)
    is_deployed = models.BooleanField(default=False)
    deployed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(Flow, related_name="nodes", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

class SubNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node = models.ForeignKey(Node, related_name="subnodes", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deployed = models.BooleanField(default=False)

class SubNodeParameter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subnode = models.ForeignKey(SubNode, related_name="parameters", on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()
    value_type = models.CharField(max_length=20, choices=ValueType.choices)

class Edge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(Flow, related_name="edges", on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    edge_type = models.CharField(max_length=50, default='default')
