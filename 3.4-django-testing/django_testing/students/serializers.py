from rest_framework import serializers
from django.conf import settings
from rest_framework.exceptions import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def create(self, validated_data):
        students = validated_data.pop('students', [])

        if len(students) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError("The maximum number of students per course has been reached.")

        course = Course.objects.create(**validated_data)
        course.students.set(students)

        return course

    def update(self, instance, validated_data):
        students = validated_data.get('students')

        if students:
            total_students_after_update = len(set(list(instance.students.all()) + students))

            if total_students_after_update > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError("The maximum number of students per course has been reached.")
                
            instance.students.set(students)
            validated_data.pop('students')

        return super().update(instance, validated_data)