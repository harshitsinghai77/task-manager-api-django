from datetime import datetime

from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):

    valid_status_choices = tuple(choice[0] for choice in Task.STATUS_CHOICES)

    status = serializers.ChoiceField(
        choices=valid_status_choices,
        error_messages={
            'invalid_choice': f"Invalid status. Valid choices are: {valid_status_choices}"
        },
        default='pending',
        required=False
    )

    class Meta:
        model = Task
        fields = ['task_id', 'title', 'description', 'due_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['task_id', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        # value will be a string in the format "YYYY-MM-DD"
        if value < datetime.today().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        return super().create(validated_data)

    # def validate_status(self, value):
    #     if value.lower() not in self.valid_status_choices:
    #         raise serializers.ValidationError(f"Invalid status: {value}. Valid choices are: {self.valid_status_choices}")
    #     return value

    def update(self, instance, validated_data):
        if set(validated_data.keys()) != {'status'}:
            raise serializers.ValidationError("Only status can be updated")
        return super().update(instance, validated_data)