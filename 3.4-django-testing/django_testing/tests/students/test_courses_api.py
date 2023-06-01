import random

import pytest
from model_bakery import baker
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve_course(client, student_factory, course_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=1)
    courses[0].students.set([student.id for student in students])

    response = client.get(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 200
    assert response.data['name'] == courses[0].name
    assert len(response.data['students']) == 10
    for student in students:
        assert student.id in response.data['students']


@pytest.mark.django_db
def test_list_course(client, course_factory):
    quantity = 3
    courses = course_factory(_quantity=quantity)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    assert len(response.data) == len(courses)


@pytest.mark.django_db
def test_filter_by_id_course(client, course_factory):
    quantity = 10
    courses = course_factory(_quantity=quantity)
    existing_id = courses[random.randrange(quantity)].id
    while True:
        missing_id = random.randint(1, 999)
        if missing_id not in [course.id for course in courses]:
            break

    response_success = client.get(f'/api/v1/courses/?id={existing_id}')
    response_failure = client.get(f'/api/v1/courses/?id={missing_id}')

    assert response_success.status_code == 200
    assert len(response_success.data) == 1
    assert response_success.data[0]['name'] == Course.objects.get(id=existing_id).name

    assert response_failure.status_code == 400
    assert response_failure.data['id'][0].code == 'invalid_choice'


@pytest.mark.django_db
def test_filter_by_name_course(client, course_factory):
    quantity = 10
    courses = course_factory(_quantity=quantity)
    existing_name = courses[random.randrange(quantity)].name
    homonyms_num = Course.objects.filter(name=existing_name).count()
    missing_name = 'test_name'
    if missing_name in [course.name for course in courses]:
        raise ValueError(f"The name: {missing_name} is one of the test objects' names.")

    response_success = client.get(f'/api/v1/courses/?name={existing_name}')
    response_failure = client.get(f'/api/v1/courses/?name={missing_name}')

    assert response_success.status_code == 200
    assert len(response_success.data) == homonyms_num
    for course in response_success.data:
        assert course['id'] in [course.id for course in Course.objects.filter(name=existing_name)]
    
    assert response_failure.status_code == 200
    assert len(response_failure.data) == 0



@pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'Test course name'}
    courses_count = Course.objects.count()

    response = client.post('/api/v1/courses/', data=data)

    assert response.status_code == 201
    assert Course.objects.count() == courses_count + 1
    assert Course.objects.filter(name=data['name']).exists()


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=1)
    data = {'name': 'Updated test name'}
    id_ = courses[0].id
    courses_count = Course.objects.count()

    response = client.patch(f'/api/v1/courses/{id_}/', data=data)
    
    assert response.status_code == 200
    assert Course.objects.get(id=id_).name == data['name']
    assert Course.objects.count() == courses_count


@pytest.mark.django_db
def test_destroy_course(client, course_factory):
    courses = course_factory(_quantity=1)
    id_ = courses[0].id
    name = Course.objects.get(id=id_).name
    courses_count = Course.objects.count()

    response = client.delete(f'/api/v1/courses/{id_}/')
    
    assert response.status_code == 204
    assert Course.objects.count() == courses_count -1
    assert not Course.objects.filter(name=name).exists()


@pytest.mark.django_db
def test_max_students(client, course_factory, student_factory, settings):
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    quantity = 3
    students = student_factory(_quantity=quantity)
    settings.MAX_STUDENTS_PER_COURSE = quantity - 1

    data_failure = {
        'students': [student.id for student in students]
    }

    data_success = {
        'students': [student.id for student in students[:settings.MAX_STUDENTS_PER_COURSE]]
    }

    response_failure = client.patch(f'/api/v1/courses/{course_id}/', data=data_failure)
    response_success = client.patch(f'/api/v1/courses/{course_id}/', data=data_success)

    assert response_failure.status_code == 400
    assert 'The maximum number of students per course has been reached.' in response_failure.json()

    assert response_success.status_code == 200
    assert Course.objects.get(id=course_id).students.count() == settings.MAX_STUDENTS_PER_COURSE


