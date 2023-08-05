# -*- coding: utf-8 -*-
"""
Serializers for enterprise api version 0 endpoint.
"""
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from enterprise_data.models import EnterpriseEnrollment, EnterpriseUser


class EnterpriseEnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for EnterpriseEnrollment model.
    """
    course_api_url = serializers.SerializerMethodField()

    def get_course_api_url(self, obj):
        """Constructs course api url"""
        return '/enterprise/v1/enterprise-catalogs/{enterprise_id}/courses/{course_id}'.format(
            enterprise_id=obj.enterprise_id, course_id=obj.course_id
        )

    class Meta:
        model = EnterpriseEnrollment
        exclude = ('created', )


class EnterpriseUserSerializer(serializers.ModelSerializer):
    """
    Serializer for EnterpriseUser model.
    """

    class Meta:
        model = EnterpriseUser
        exclude = ('created', )


class LearnerCompletedCoursesSerializer(serializers.Serializer):    # pylint: disable=abstract-method
    """
    Serializer for learner's completed courses.
    """
    user_email = serializers.EmailField()
    completed_courses = serializers.IntegerField()
