from dataclasses import field, fields
from statistics import mode
from .models import Account, Courses, OpenRequests, Reservation, School
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenRequests
        fields = "__all__"

    def create(self, validated_data):
        validated_data["request_timestamp"] = timezone.now()
        validated_data["request_status"] = "DocsPending"
        req = OpenRequests.objects.create(**validated_data)
        return req

    def update(self, instance, validated_data):
        instance.document = validated_data.get("document", instance.document)
        instance.payment_pic = validated_data.get("payment_pic", instance.payment_pic)
        instance.request_status = validated_data.get(
            "request_status", instance.request_status
        )
        # instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"

    def create(self, validated_data):
        validated_data["reserved_student"] = 0
        return Courses.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get("course_name", instance.course_name)
        instance.type = validated_data.get("type", instance.type)
        instance.course_description = validated_data.get(
            "course_description", instance.course_description
        )
        instance.reserve_close_date = validated_data.get(
            "reserve_close_date", instance.reserve_close_date
        )
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.course_period = validated_data.get(
            "course_period", instance.course_period
        )
        instance.course_price = validated_data.get(
            "course_price", instance.course_price
        )
        instance.maximum_student = validated_data.get(
            "maximum_student", instance.maximum_student
        )
        instance.reserved_student = validated_data.get(
            "reserved_student", instance.reserved_student
        )
        instance.payment_method_text = validated_data.get(
            "payment_method_text", instance.payment_method_text
        )
        instance.payment_method_pic = validated_data.get(
            "payment_method_pic", instance.payment_method_pic
        )
        instance.course_pic = validated_data.get("course_pic", instance.course_pic)
        instance.save()
        return instance


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        validated_data["reservation_datetime"] = timezone.now()
        validated_data["status"] = "Pending"
        validated_data["expire_datetime"] = timezone.now() + timedelta(1)
        return Reservation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.payment_pic = validated_data.get("payment_pic", instance.payment_pic)
        instance.save()
        return instance


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.owner_id = validated_data.get("owner_id", instance.owner_id)
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.addr_description = validated_data.get(
            "addr_description", instance.addr_description
        )
        # instance.status = validated_data.get(
        #     'status', instance.status)
        instance.sub_district = validated_data.get(
            "sub_district", instance.sub_district
        )
        instance.district = validated_data.get("district", instance.district)
        instance.province = validated_data.get("province", instance.province)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.logo_pic = validated_data.get("logo_pic", instance.logo_pic)
        instance.banner_pic = validated_data.get("banner_pic", instance.banner_pic)
        instance.save()
        return instance

    def create(self, validated_data):
        validated_data["status"] = "Pending"
        reqSchool = School.objects.create(**validated_data)
        return reqSchool


class SchoolStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "account_id",
            "firstname",
            "lastname",
            "email",
            "profile_picture",
            "token_expire",
            "token",
        )

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.year_of_birth = validated_data.get(
            "year_of_birth", instance.year_of_birth
        )
        instance.description = validated_data.get("description", instance.description)
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.token = validated_data.get("token", instance.token)
        instance.token_expire = validated_data.get(
            "token_expire", instance.token_expire
        )
        instance.save()
        return instance
