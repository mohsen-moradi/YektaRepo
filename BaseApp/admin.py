from django.contrib import admin
from .models import (FamilyTbl,
                     FamilyMembersTbl,
                     MemberGenderTbl,
                     MemberPositionTbl,
                     MemberStatus,
                     CheckingStatuses,
                     Priorities,
                     Duties,
                     DutyImages)

admin.site.register(FamilyTbl)
admin.site.register(FamilyMembersTbl)
admin.site.register(MemberGenderTbl)
admin.site.register(MemberPositionTbl)
admin.site.register(MemberStatus)
admin.site.register(CheckingStatuses)
admin.site.register(Priorities)
admin.site.register(Duties)
admin.site.register(DutyImages)
