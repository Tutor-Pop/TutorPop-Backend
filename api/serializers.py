from dataclasses import field
from .models import OpenRequests, Reservation
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
        instance.request_status = validated_data(
            'requese_status', instance.request_status)
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
