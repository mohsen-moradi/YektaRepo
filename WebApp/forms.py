from django.forms import ModelForm
from BaseApp.models import FamilyTbl, FamilyMembersTbl, Duties
from django.utils.translation import ugettext_lazy as _


class CreateDutyForm(ModelForm):
    """This class used to create CreateDutyForm form"""
    # DeadLineDate = forms.DateField(widget=forms.DateInput(
    #     format='%Y-%m-%d %H:%M'),
    #     input_formats=('%Y-%m-%d %H:%M',))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['DeadLineDate'].widget.attrs.update(
            {'lang': 'en', 'class': 'form-control', 'id': 'exampleInput1'})

    class Meta():
        model = Duties
        fields = ['Subject',
                  'Content',
                  'DutyReceiver',
                  'Priority',
                  'DeadLineDate']
        labels = {
            'Subject': _('Subject'),
            'Content': _('Content'),
            'DutyReceiver': _('DutyReceiver'),
            'Priority': _('Priority'),
            'DeadLineDate': _('DeadLineDate')
        }


class FamilyAuthForm(ModelForm):
    """This class used to create FamilyAuthForm form"""
    class Meta():
        """Meta class used to specify form fields based on specific Model"""
        model = FamilyTbl
        fields = ['FamilyCode']
        labels = {
            "FamilyCode": _('FamilyCode')
        }


class FamilyMemberForm(ModelForm):
    """This class used to create FamilyMemberForm form"""
    class Meta():
        model = FamilyMembersTbl
        fields = ['Fname',
                  'Lname',
                  'MobileNumber',
                  'MemberNationalCode',
                  'Gender',
                  'MemberPositionID',
                  'Email']
        labels = {
            'Fname': 'نام',
            'Lname': 'نام خانوادگی',
            'MobileNumber': 'شماره همراه',
            'MemberNationalCode': 'کد ملی',
            'Gender': 'جنسیت',
            'MemberPositionID': 'جایگاه در خانواده',
            'Email': 'ایمیل'
        }


class FamilyRegisterForm(ModelForm):
    """This class used to create FamilyRegisterForm form"""
    class Meta():
        model = FamilyTbl
        fields = ['title']
        labels = {'title': 'نام خانوادگی محترم خود را ثبت نمایید'}

# class CreateDutyFom(ModelForm):
#     """This class used to create FamilyRegisterForm form"""
#     class Meta():
#         model = Duties
        # fields = ['Subject',
        #           'Content',
        #           'DutySender',
        #           'DutyReceiver'
        #           'Priority',
        #           'CreateDate',
        #           'DeadLineDate',
        #           'CheckStatus']
