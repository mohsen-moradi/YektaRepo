from django.contrib.auth.models import User
from BaseApp.models import (Duties,
                            FamilyTbl,
                            FamilyMembersTbl,
                            CheckingStatuses)
from django.views.generic import ListView, CreateView, FormView, RedirectView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import (FamilyAuthForm,
                    FamilyMemberForm,
                    FamilyRegisterForm,
                    CreateDutyForm)
from django.http import HttpResponseRedirect, HttpResponse
# from django.shortcuts import get_object_or_404
from django.contrib import messages
# from django.contrib.messages import get_messages
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from base64 import b64encode, b64decode
from random import randrange
from jdatetime import datetime as jd

# def HomePageFunc(request):
#     Context = {'HomeContext': Duties.objects.all()}
#     return render(request, 'WebApp/home.html', Context)


class HomePage(LoginRequiredMixin, ListView):
    """This class used to show Home Page"""

    model = Duties
    template_name = 'WebApp/Home.html'
    context_object_name = 'HomeContext'

    def get_queryset(self):
        return Duties.objects.filter(
            DutyReceiver=self.request.user.familymemberstbl.id
        ).order_by('-CreateDate')


class CreateDutyPage(LoginRequiredMixin, CreateView):
    """This class used to create post page"""
    form_class = CreateDutyForm
    template_name = 'WebApp/CreateDuty.html'

    def get(self, request, *args, **kwargs):
        SenderUserFamilyIDVar = self.request.user.familymemberstbl.FamilyID
        SenderUserFamilyMemIDVar = self.request.user.familymemberstbl.id
        RecieverUsersVar = FamilyMembersTbl.objects.filter(
            FamilyID=SenderUserFamilyIDVar).exclude(
            id=SenderUserFamilyMemIDVar)
        form = self.form_class()
        form.fields['DutyReceiver'].queryset = RecieverUsersVar
        # form.fields['CheckStatus'].queryset = (
        #     CheckingStatuses.objects.filter(id=1))
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = Duties()
            obj.Subject = form.cleaned_data['Subject']
            obj.Content = form.cleaned_data['Content']
            obj.DutySender = self.request.user.familymemberstbl
            obj.DutyReceiver = form.cleaned_data['DutyReceiver']
            obj.Priority = form.cleaned_data['Priority']
            obj.CreateDate = jd.now().strftime("%d-%m-%Y %I:%M")
            obj.DeadLineDate = form.cleaned_data['DeadLineDate']
            obj.CheckStatus = CheckingStatuses.objects.get(id=1)
            obj.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'درخواست جدید با موفقیت درج شد')
        return HttpResponseRedirect('/home/')

        # return HttpResponse(RecieverUsersVar)
# self.form_class(initial={'DutyReceiver':'ali'},instance=dd[0])


class RegisterPage(CreateView):
    """This class used to show Registration page"""
    form_class = UserCreationForm
    template_name = 'WebApp/Registration.html'
    # success_url = '/home/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            UsernameVar = form.cleaned_data['username']
            form.save()
            RegisteredUserVar = User.objects.get(username=UsernameVar)
            User.objects.filter(id=RegisteredUserVar.id).update(is_active=0)
            # import ipdb; ipdb.set_trace()
            request.session['RegisteredUser'] = (
                RegisteredUserVar.id, RegisteredUserVar.username)
            if 'FamilyInfo' in request.session:
                return HttpResponseRedirect('/regfamilymeminfo/')
            else:
                return HttpResponseRedirect('/register/registerfamily/')
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(
                self.request,
                f"""{_('Please')} {_('Of')}
                    {_('UserAccount')}
                    {_('Yourself')}
                    {_('Go out')} """)
            # storage = messages.get_messages(self.request)
            # storage.used = True
            return redirect('LoginPagePath')

        form = self.form_class()
        if 'FamilyInfo' in request.session:
            FamilyInfoVar = request.session['FamilyInfo'][1]
            messages.add_message(self.request, messages.SUCCESS,
                                 f"خانواده محترم  {FamilyInfoVar} خوش آمدید")
        return render(request, self.template_name, {'form': form})


class RegisterFamily(CreateView):
    """This class used to show Family Registration page"""
    form_class = FamilyRegisterForm
    template_name = 'WebApp/RegisterFamily.html'

    def get(self, request, *args, **kwargs):
        if 'RegisteredUser' not in request.session:
            messages.add_message(self.request, messages.INFO,
                                 _('Dear user you should register in Yekta'))
            return HttpResponseRedirect('/register/')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = FamilyTbl()
            obj.title = form.cleaned_data['title']
            FamilyCodeResult = True
            # import ipdb; ipdb.set_trace()
            while FamilyCodeResult:
                GenerateUniqueFamilyCode = str(randrange(1, 999))
                FamilyCodeResult = FamilyTbl.objects.filter(
                    FamilyCode=GenerateUniqueFamilyCode)
            obj.FamilyCode = GenerateUniqueFamilyCode
            obj.save()
            messages.add_message(self.request, messages.INFO,
                                 f"خانواده محترم {obj.title} خوش آمدید")
            FamilyInfoVar = FamilyTbl.objects.get(FamilyCode=obj.FamilyCode)
            request.session['FamilyInfo'] = (
                FamilyInfoVar.id, obj.title)
        return HttpResponseRedirect('/regfamilymeminfo/')


# class DilemmaPage(TemplateView):


class DilemmaPage(View):
    """This class uset to show Dilemma page"""
    template_name = 'WebApp/Dilemma.html'

    def get(self, request, *args, **kwargs):
        # del request.session['FamilyInfo']
        # del request.session['RegisteredUser']
        if self.request.user.is_authenticated:
            messages.error(request,
                           f"""{_('Please')} {_('Of')}
                    {_('UserAccount')}
                    {_('Yourself')}
                    {_('Go out')} """)

            # storage = messages.get_messages(self.request)
            # storage.used = True
            return redirect('LoginPagePath')
        return render(request, self.template_name)


class FamilyAuthPage(FormView):
    """This class used to show FamilyAuth page"""
    template_name = 'WebApp/FamilyAuth.html'
    form_class = FamilyAuthForm
    # success_url = '/home/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            FamilyCodeVar = form.cleaned_data['FamilyCode']
            try:
                FamilyInfoVar = FamilyTbl.objects.get(
                    FamilyCode=FamilyCodeVar)
                request.session['FamilyInfo'] = (
                    FamilyInfoVar.id, FamilyInfoVar.title)
                print(request.session['FamilyInfo'][0])
                return redirect('RegPagePath')
            except ObjectDoesNotExist:
                messages.error(
                    self.request,
                    'شناسه خانوادگی یافت نشد')
                return redirect('FamilyAuthPagePath')

            # obj = get_object_or_404(FamilyTbl, FamilyCode=FamilyCodeVar)
            # print(obj.id)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                                 f"""{_('Please')} {_('Of')}
                                 {_('UserAccount')}
                                 {_('Yourself')}
                                 {_('Go out')} """)
            return redirect('LoginPagePath')
        return render(request, self.template_name, {'form': form})


class FamilyMemberPage(View):
    """This class used to show FamilyMemberPage"""
    # model = FamilyMembersTbl
    template_name = 'WebApp/RegFamilyMemInfo.html'
    form_class = FamilyMemberForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        RegisteredUserVar = User.objects.get(
            id=request.session['RegisteredUser'][0])
        FamilyInfoVar = FamilyTbl.objects.get(
            id=request.session['FamilyInfo'][0])
        if form.is_valid():
            obj = FamilyMembersTbl()
            obj.UserMember = RegisteredUserVar
            obj.FamilyID = FamilyInfoVar
            obj.Fname = form.cleaned_data['Fname']
            obj.Lname = form.cleaned_data['Lname']
            obj.MobileNumber = form.cleaned_data['MobileNumber']
            obj.MemberNationalCode = form.cleaned_data['MemberNationalCode']
            obj.Gender = form.cleaned_data['Gender']
            obj.MemberPositionID = form.cleaned_data['MemberPositionID']
            obj.Email = form.cleaned_data['Email']
            obj.save()
            # bStr = bytes(str(request.session['RegisteredUser'][0]), 'utf-8')
            IdToStr = str(request.session['RegisteredUser'][0]).encode('utf-8')
            EncodedUserId = str(b64encode(IdToStr), 'utf-8')
            MessageBody = f"""{_('To active your account click here')}
            <a href="{request.build_absolute_uri('/activation/')}
            {EncodedUserId}">Yekta.com</a>"""
            send_mail(_('Activation link from Yekta'),
                      '',
                      settings.EMAIL_HOST_USER,
                      [obj.Email],
                      html_message=MessageBody)
            messages.add_message(request,
                                 messages.SUCCESS,
                                 f"""{obj.Fname}
                        {_('Dear user we will send you an activation email')}
                        """)
            return redirect('LoginPagePath')
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        if 'FamilyInfo' not in request.session:
            messages.add_message(
                self.request, messages.ERROR,
                f"{_('FamilyCode not found')}")
            return redirect('LoginPagePath')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ActivationPage(RedirectView):
    """This class used to activation FamilyMember user"""

    def get(self, request, *args, **kwargs):
        try:
            UserMemberId = int(b64decode(self.kwargs['id']))
        except __import__('binascii').Error:
            messages.add_message(request,
                                 messages.ERROR,
                                 _('Activation link is not valid'))
        else:
            ExistUser = User.objects.filter(
                id=UserMemberId)
            if not ExistUser:
                messages.add_message(request,
                                     messages.ERROR,
                                     _('User not found for activation'))
            else:
                ExistUser.update(is_active=1)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('Your account has been actived successfully'))
        return redirect("LoginPagePath")

# def CheckUser(slf, rqst):
#     self = slf
#     request = rqst
#     if rqst.user.is_authenticated:
#         messages.error(
#             self.request,
#             f"""{_('Please')} {_('Of')}
#                 {_('UserAccount')}
#                 {_('Yourself')}
#                 {_('Go out')} """)
#         return True
#     else:
#         return False
