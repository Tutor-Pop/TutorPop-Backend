from dataclasses import field
from .models import Courses, OpenRequests
from rest_framework import serializers
from django.utils import timezone


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenRequests
        fields = '__all__'

    def create(self, validated_data):
        validated_data['request_timestamp'] = timezone.now()
        validated_data['request_status'] = 'Pending'
        req = OpenRequests.objects.create(**validated_data)
        return req

    def update(self, instance, validated_data):
        instance.account = validated_data.get('account', instance.account)
        instance.school = validated_data.get('school', instance.school)
        instance.document_url = validated_data(
            'document_url', instance.document_url)
        instance.proof_of_payment_url = validated_data(
            'proof_of_payment_url', instance.proof_of_payment_url)
        instance.request_status = validated_data(
            'requese_status', instance.request_status)
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.type = validated_data.get('type', instance.type)
        instance.course_description = validated_data.get('course_description', instance.course_description)
        instance.reserve_close_date = validated_data.get('reserve_close_date', instance.reserve_close_date)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.course_period = validated_data.get('course_period', instance.course_period)
        instance.course_price = validated_data.get('course_price', instance.course_price)
        instance.maximum_student = validated_data.get('maximum_student', instance.maximum_student)
        instance.reserved_student = validated_data.get('reserved_student', instance.reserved_student)
        instance.payment_method_text = validated_data.get('payment_method_text', instance.payment_method_text)
        instance.payment_method_picture_url = validated_data.get('payment_method_picture_url', instance.payment_method_picture_url)
        instance.save()
        return instance
