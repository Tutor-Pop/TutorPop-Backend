from api.models import Reservation, Courses
import datetime
from django.utils import timezone


def reservation_expire():
    now = timezone.now()
    revs = Reservation.objects.filter(status="Pending", expire_datetime__lte=now)
    expire_rev = ""
    for rev in revs:
        expire_rev += str(rev.id)
        cid = rev.course_id.course_id
        course = Courses.objects.get(course_id=cid)
        course.reserved_student -= 1
        rev.status = "Expired"
        rev.save()
        course.save()

    print(f"Remove expired reservation({expire_rev})")
