from django.db import models
from jdatetime import datetime as jd
from django.contrib.auth.models import User


class FamilyTbl(models.Model):
    """The class used to create Family table"""
    title = models.CharField(max_length=250)
    FamilyCode = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):

        return f'{self.title}'


class MemberPositionTbl(models.Model):
    """The class used to create Member Position table"""
    Title = models.CharField(max_length=50)

    def __str__(self):

        return f'{self.Title}'


class MemberGenderTbl(models.Model):
    """The class used to create Member gender table"""
    Title = models.CharField(max_length=10)

    def __str__(self):

        return f'{self.Title}'


class MemberStatus(models.Model):
    """The class used to create Member status table"""
    Title = models.CharField(max_length=15)

    def __str__(self):

        return f'{self.Title}'


class FamilyMembersTbl(models.Model):
    """The class used to create Family members table"""
    UserMember = models.OneToOneField(User,
                                      on_delete=models.CASCADE,
                                      blank=True)
    FamilyID = models.ForeignKey(FamilyTbl,
                                 on_delete=models.CASCADE,
                                 blank=True)
    Fname = models.CharField(max_length=200)
    Lname = models.CharField(max_length=250)
    MobileNumber = models.CharField(max_length=11)
    MemberNationalCode = models.CharField(max_length=10)
    Gender = models.ForeignKey(MemberGenderTbl,
                               on_delete=models.SET_NULL,
                               null=True)
    IsActive = models.ForeignKey(MemberStatus,
                                 on_delete=models.SET_NULL,
                                 default=2,
                                 editable=False,
                                 blank=True,
                                 null=True)
    MemberPositionID = models.ForeignKey(MemberPositionTbl,
                                         on_delete=models.SET_NULL,
                                         null=True)
    Email = models.EmailField(max_length=250)
    Image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return '{}{}{}'.format(self.Fname,
                               ' ',
                               self.FamilyID.title)


class CheckingStatuses(models.Model):
    """The class used to create duties statuses table"""
    Title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.Title}'


class Priorities(models.Model):
    """The class used to create priority table"""
    Title = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.Title}'


class Duties(models.Model):
    """The class used to create duties table"""

    def jCreateDate(self):
        return jd.fromgregorian(
            year=self.CreateDate.year,
            month=self.CreateDate.month,
            day=self.CreateDate.day,
            hour=self.CreateDate.hour,
            minute=self.CreateDate.minute
        ).strftime("%H:%M %d-%m-%Y")

    def jDeadLineDate(self):
        return self.DeadLineDate.strftime("%H:%M %d-%m-%Y")

    Subject = models.CharField(max_length=250)
    Content = models.TextField()
    DutySender = models.ForeignKey(FamilyMembersTbl,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='Duty_Sender_Relation')
    DutyReceiver = models.ForeignKey(FamilyMembersTbl,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='Duty_Receiver_Relation')
    Priority = models.ForeignKey(Priorities,
                                 on_delete=models.SET_NULL,
                                 null=True)
    CreateDate = models.DateTimeField(auto_now_add=True)
    DeadLineDate = models.DateTimeField()
    CheckStatus = models.ForeignKey(CheckingStatuses,
                                    on_delete=models.SET_NULL,
                                    null=True)

    def __str__(self):
        return '{} {} {}'.format(self.DutySender,
                                 self.DutyReceiver,
                                 self.Subject)


def get_upload_path(instance, filename):
    return f'duty_images/{instance.DutyID.Subject}/{filename}'


class DutyImages(models.Model):
    """The class used to create duty images table"""

    DutyID = models.ForeignKey(Duties,
                               on_delete=models.CASCADE)
    Images = models.ImageField(
        upload_to=get_upload_path)

    def __str__(self):
        return f"{self.Images}"
