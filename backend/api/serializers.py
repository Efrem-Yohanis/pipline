from rest_framework import serializers
from .models import Member, Staff, GymClass, Payment, InventoryItem, CheckIn, MembershipPlan

class SimpleMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email']

class MembershipPlanSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = MembershipPlan
        fields = '__all__'

    def get_member_count(self, obj):
        return obj.member_set.count()

class MemberSerializer(serializers.ModelSerializer):
    membership_plan = MembershipPlanSerializer(read_only=True)
    membership_plan_id = serializers.PrimaryKeyRelatedField(
        queryset=MembershipPlan.objects.all(), source='membership_plan', write_only=True, required=True
    )
    class Meta:
        model = Member
        fields = '__all__'

    def validate(self, data):
        if not data.get('membership_plan'):
            raise serializers.ValidationError({
                'membership_plan_id': 'This field is required.'
            })
        return data

    def create(self, validated_data):
        # membership_plan is set by the PrimaryKeyRelatedField above
        return Member.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class StaffSerializer(serializers.ModelSerializer):
    specialization_list = serializers.SerializerMethodField()
    class Meta:
        model = Staff
        fields = '__all__'

    def get_specialization_list(self, obj):
        return obj.get_specialization_list()

class GymClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymClass
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'