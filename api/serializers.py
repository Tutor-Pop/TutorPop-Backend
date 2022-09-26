from dataclasses import field, fields
from statistics import mode
from .models import Account, Courses, OpenRequests, Reservation, School
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta


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
        #instance.request_status = validated_data('requese_status', instance.request_status)
        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get(
            'course_name', instance.course_name)
        instance.type = validated_data.get('type', instance.type)
        instance.course_description = validated_data.get(
            'course_description', instance.course_description)
        instance.reserve_close_date = validated_data.get(
            'reserve_close_date', instance.reserve_close_date)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.course_period = validated_data.get(
            'course_period', instance.course_period)
        instance.course_price = validated_data.get(
            'course_price', instance.course_price)
        instance.maximum_student = validated_data.get(
            'maximum_student', instance.maximum_student)
        instance.reserved_student = validated_data.get(
            'reserved_student', instance.reserved_student)
        instance.payment_method_text = validated_data.get(
            'payment_method_text', instance.payment_method_text)
        instance.payment_method_picture_url = validated_data.get(
            'payment_method_picture_url', instance.payment_method_picture_url)
        instance.save()
        return instance


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        validated_data['reservation_datetime'] = timezone.now()
        validated_data['status'] = 'Pending'
        validated_data['expire_datetime'] = timezone.now()+timedelta(1)
        return Reservation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.owner = validated_data.get(
            'owner', instance.owner)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.address = validated_data.get(
            'address', instance.address)
        # instance.status = validated_data.get(
        #     'status', instance.status)
        instance.logo_url = validated_data.get(
            'logo_url', instance.logo_url)
        instance.banner_url = validated_data.get(
            'banner_url', instance.banner_url)
        instance.save()
        return instance

    def create(self, validated_data):
        validated_data['status'] = 'Pending'
        reqSchool = School.objects.create(**validated_data)
        return reqSchool

class SchoolStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = validated_data.get(
            'status', instance.status)
        instance.save()
        return instance

class AccountSerializer(serializers.ModelSerializer): # NOT DONE YET!
    class Meta:
        model = Account
        fields = '__all__'
    
    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account