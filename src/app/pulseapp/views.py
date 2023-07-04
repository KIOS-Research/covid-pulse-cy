import datetime
import json

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from . import forms
from . import models
from django.db import models as model1

from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect
from django.db import connection
import xlwt
from .decorators import allowed_users
import csv


def runquery(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchall()
    return row


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, ' Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def index(request):
    return render(request, 'pulseapp/index.html', {'tab': 'home'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin'])
def sampledata(request):
    sampleForm = forms.SampleDataForm(request.POST or None)
    typec = models.covtype.objects.values_list('type', flat=True).distinct()
    types = models.covtype.objects.all().order_by("pk")
    formset = formset_factory(forms.WWWmeasureDataFormSet, extra=0)
    cov_formset = formset(request.POST or None, initial=[{'covtype': t, 'type': t, 'unit': t.units} for t in types])

    if request.method == 'POST':
        if sampleForm.is_valid() and cov_formset.is_valid():
            s_form = sampleForm.save(commit=False)
            sampleid = f"{s_form.location.init}_{s_form.dateend.strftime('%d%m%Y')}"
            if models.sampledata.objects.filter(sampleid=sampleid).exists():
                s_form = models.sampledata.objects.filter(sampleid=sampleid).first()
            s_form.loginname = request.user
            s_form.sampleid = sampleid
            s_form.save()
            analysis_date = sampleForm.cleaned_data['analysis_date']
            for form in cov_formset:
                if form.is_valid():
                    n = f"{form.cleaned_data['type']}_notes"
                    note = request.POST.get(n)
                    f = form.save(commit=False)
                    if f.value is not None:
                        f.loginame = request.user
                        f.sampleid = s_form
                        f.analysisdate = analysis_date
                        f.reportdate = analysis_date
                        f.notes = note
                        f.wwmeasureid = f"{s_form.sampleid}_{f.covtype.type}_{f.covtype.units}"
                        f.save()
            messages.success(request, 'Sample data submitted successfully')
            return HttpResponseRedirect(reverse('pulseapp:viewsampledata'))
        else:
            messages.error(request, 'Sample data submitted fail')
            print(cov_formset.errors)

    context = {
        'cov_formset': cov_formset,
        'types': typec,
        'sampleform': sampleForm,
        'tab': 'sampling'
    }
    return render(request, 'pulseapp/sampledata.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin', 'trends'])
def TrendsView(request):
    form = forms.TrendsForm(request.POST or None)
    zones = models.uwtp.objects.all().order_by()
    formset = formset_factory(forms.TrendsFormSet, extra=0)
    trends_formset = formset(request.POST or None,
                             initial=[{'station': z.uwwName, 'samplestationid': z} for z in zones])

    if request.method == 'POST':
        if form.is_valid() and trends_formset.is_valid():
            n_form = form.save(commit=False)
            for trend_form in trends_formset:
                if trend_form.is_valid():
                    t_form = trend_form.save(commit=False)
                    if t_form.value is not None:
                        t_form.fromdate = n_form.fromdate
                        t_form.todate = n_form.todate
                        t_form.loginname = request.user
                        t_form.save()
            messages.success(request, 'Trends data submitted successfully')
            return HttpResponseRedirect(reverse('pulseapp:viewtrends'))
        else:
            messages.error(request, 'Trends data submitted fail')

    context = {
        'form': form,
        'formset': trends_formset,
        'tab': 'trends'
    }

    return render(request, 'pulseapp/trends.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def VariantsView(request):
    form = forms.VariantsForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            v_form = form.save(commit=False)
            v_form.datestart = v_form.dateend + datetime.timedelta(days=-1)
            v_form.sampleid = f"{v_form.location.init}_{v_form.dateend.strftime('%d%m%Y')}"
            v_form.loginname = request.user
            v_form.save()
            messages.success(request, 'Variants data submitted successfully')
            return HttpResponseRedirect(reverse('pulseapp:viewvariants'))
        else:
            messages.error(request, 'Sample data submitted fail')

    context = {
        'form': form,
        'tab': 'variants'
    }

    return render(request, 'pulseapp/variants.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def AddVariantsTypeView(request):
    form = forms.VariantsTypeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            v_form = form.save()
            messages.success(request, 'Variant Type data submitted successfully')
            return HttpResponseRedirect(reverse('pulseapp:viewvariantstype'))
        else:
            messages.error(request, 'Variant Type data submitted fail')

    context = {
        'form': form,
        'tab': 'variants'
    }

    return render(request, 'pulseapp/variantsType.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin'])
def SampleEditView(request, pk=None):
    if pk:
        sample = models.sampledata.objects.filter(pk=pk)
        typec = models.covtype.objects.values_list('type', flat=True).distinct()
        types = models.covtype.objects.all().order_by("pk")
        formset_dictionary = [{'covtype': t, 'type': t, 'unit': t.units, 'value': None, 'pk': None} for t in types]
        measurements = models.wwmeasure.objects.filter(sampleid=pk)
        types_dict = {}
        for t in typec:
            types_dict[t] = ''
        for m in measurements:
            for d in formset_dictionary:
                if d['type'] == m.covtype and d['unit'] == m.covtype.units:
                    d['pk'] = m.pk
                    d['value'] = float(m.value)
            # for t in typec:
            #     if t == m.covtype.type:
            #         types_dict[t] = m.notes
            types_dict[m.covtype.type] = m.notes

        print(formset_dictionary)
        sample_form = forms.SampleDataForm(request.POST or None, instance=sample[0],
                                           initial={'analysis_date': measurements[0].analysisdate})
        formset = formset_factory(forms.WWWmeasureDataFormSet, extra=0)
        cov_formset = formset(request.POST or None, initial=formset_dictionary)
        print("FORMSET")
        print(cov_formset)
        if request.method == 'POST':
            if sample_form.is_valid() and cov_formset.is_valid():
                s_form = sample_form.save(commit=False)
                s_form.loginname = request.user
                s_form.sampleid = f"{s_form.location.init}_{s_form.dateend.strftime('%d%m%Y')}"
                s_form.save()
                analysis_date = sample_form.cleaned_data['analysis_date']
                measurements.delete()
                for form in cov_formset:
                    if form.is_valid():
                        n = f"{form.cleaned_data['type']}_notes"
                        note = request.POST.get(n)
                        f = form.save(commit=False)
                        if f.value is not None:
                            measurement = models.wwmeasure.objects.create(value=f.value, covtype=f.covtype,
                                                                          sampleid=s_form, analysisdate=analysis_date,
                                                                          reportdate=analysis_date, notes=note,
                                                                          wwmeasureid=f"{s_form.sampleid}_{f.covtype.type}_{f.covtype.units}")
                            measurement.save()
                messages.success(request, 'Sample data submitted successfully')
                return HttpResponseRedirect(reverse('pulseapp:viewsampledata'))
            else:
                messages.error(request, 'Sample data submitted fail')
    context = {
        'cov_formset': cov_formset,
        'types': typec,
        'sampleform': sample_form,
        'types_dict': types_dict,
        'tab': 'sampling'
    }
    return render(request, 'pulseapp/editsampledata.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin'])
def MeasurementsEditView(request, pk=None):
    if pk:
        measure = models.wwmeasure.objects.filter(pk=pk)
        sample = measure[0].sampleid
        typec = models.covtype.objects.values_list('type', flat=True).distinct()
        types = models.covtype.objects.all().order_by("pk")
        formset_dictionary = [{'covtype': t, 'type': t, 'unit': t.units, 'value': None, 'pk': None} for t in types]
        measurements = models.wwmeasure.objects.filter(sampleid=sample)
        types_dict = {}
        for m in measurements:
            for d in formset_dictionary:
                if d['type'] == m.covtype and d['unit'] == m.covtype.units:
                    d['pk'] = m.pk
                    d['value'] = float(m.value)
            for t in typec:
                if t == m.covtype.type:
                    types_dict[t] = m.notes
        sample_form = forms.SampleDataForm(request.POST or None, instance=sample,
                                           initial={'analysis_date': measurements[0].analysisdate})
        formset = formset_factory(forms.WWWmeasureDataFormSet, extra=0)
        cov_formset = formset(request.POST or None, initial=formset_dictionary)

        if request.method == 'POST':
            if sample_form.is_valid() and cov_formset.is_valid():
                s_form = sample_form.save(commit=False)
                s_form.loginname = request.user
                s_form.sampleid = f"{s_form.location.init}_{s_form.dateend.strftime('%d%m%Y')}"
                s_form.save()
                analysis_date = sample_form.cleaned_data['analysis_date']
                measurements.delete()
                for form in cov_formset:
                    if form.is_valid():
                        n = f"{form.cleaned_data['type']}_notes"
                        note = request.POST.get(n)
                        f = form.save(commit=False)
                        if f.value is not None:
                            measurement = models.wwmeasure.objects.create(value=f.value, covtype=f.covtype,
                                                                          sampleid=s_form, analysisdate=analysis_date,
                                                                          reportdate=analysis_date, notes=note,
                                                                          wwmeasureid=f"{s_form.sampleid}_{f.covtype.type}_{f.covtype.units}")
                            measurement.save()
                messages.success(request, 'Sample data submitted successfully')
                return HttpResponseRedirect(reverse('pulseapp:viewwwmeasure'))
            else:
                messages.error(request, 'Sample data submitted fail')
    context = {
        'cov_formset': cov_formset,
        'types': typec,
        'sampleform': sample_form,
        'types_dict': types_dict,
        'tab': 'sampling'
    }
    return render(request, 'pulseapp/editsampledata.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin', 'trends'])
def EditTrendsView(request, pk=None):
    if pk:
        trends = models.trends.objects.filter(pk=pk)
        form = forms.TrendsEditForm(request.POST or None, instance=trends[0])

        if request.method == 'POST':
            if form.is_valid():
                n_form = form.save(commit=False)
                n_form.loginname = request.user
                n_form.save()

                messages.success(request, 'Trends data submitted successfully')
                return HttpResponseRedirect(reverse('pulseapp:viewtrends'))
            else:
                messages.error(request, 'Trends data submitted fail')

    context = {
        'form': form,
        'tab': 'trends'
    }

    return render(request, 'pulseapp/edittrends.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def VariantsEditView(request, pk=None):
    if pk:
        variant = models.variants.objects.filter(pk=pk)
        variant_form = forms.VariantsForm(request.POST or None, instance=variant[0])
        if request.method == 'POST':
            if variant_form.is_valid():
                v_form = variant_form.save(commit=False)
                v_form.datestart = v_form.dateend + datetime.timedelta(days=-1)
                v_form.sampleid = f"{v_form.location.init}_{v_form.dateend.strftime('%d%m%Y')}"
                v_form.loginname = request.user
                v_form.save()
                messages.success(request, 'Variants data submitted successfully')
                return HttpResponseRedirect(reverse('pulseapp:viewvariants'))
            else:
                messages.error(request, 'Sample data submitted fail')
    context = {
        'form': variant_form,
        'tab': 'variants'
    }

    return render(request, 'pulseapp/variants.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def VariantsTypeEditView(request, pk=None):
    if pk:
        variant_type = models.variantType.objects.filter(pk=pk)
        form = forms.VariantsTypeForm(request.POST or None, instance=variant_type[0])

        if request.method == 'POST':
            if form.is_valid():
                v_form = form.save()
                messages.success(request, 'Variant Type data edited successfully')
                return HttpResponseRedirect(reverse('pulseapp:viewvariantstype'))
            else:
                messages.error(request, 'Variant Type data edit fail')

    context = {
        'form': form,
        'tab': 'variants'
    }

    return render(request, 'pulseapp/variantsType.html', context)


@login_required(login_url='/')
@allowed_users(['admin'])
def viewsampledata(request):
    context = {'tab': 'sampling'}
    return render(request, 'pulseapp/viewsampledata.html', context)


@login_required(login_url='/')
@allowed_users(['admin'])
def viewwwmeasure(request):
    context = {'tab': 'sampling'}
    return render(request, 'pulseapp/viewwwmeasure.html', context)


@login_required(login_url='/')
@allowed_users(['admin', 'trends'])
def viewTrendsData(request):
    context = {'tab': 'trends'}
    return render(request, 'pulseapp/viewtrendsdata.html', context)


@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def viewVariantsData(request):
    context = {'tab': 'variants'}
    return render(request, 'pulseapp/viewvariantsdata.html', context)


@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def viewVariantsTypeData(request):
    context = {'tab': 'variants'}
    return render(request, 'pulseapp/viewvariantstype.html', context)


class viewsampledataListJson(BaseDatatableView):
    model = models.sampledata
    columns = ['id', 'location', 'datestart', 'dateend',
               'notes', 'loginname', 'submited_datetime']
    order_columns = ['id', 'location', 'datestart', 'dateend',
                     'notes', 'loginname', 'submited_datetime']

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(notes__istartswith=search) | Q(submited_datetime__istartswith=search) \
                | Q(loginname__username__istartswith=search) | Q(datestart__istartswith=search) \
                | Q(dateend__istartswith=search) | Q(location__uwwName__istartswith=search) | Q(
                sampleid__istartswith=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'submited_datetime':
            return ('{0}'.format(row.submited_datetime.strftime('%Y-%m-%d %H:%M')))
        else:
            return super(viewsampledataListJson, self).render_column(row, column)


class viewwwmeasureListJson(BaseDatatableView):
    model = models.wwmeasure

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(notes__istartswith=search) | Q(submited_datetime__istartswith=search) \
                | Q(wwmeasureid__istartswith=search) | Q(covtype__type__istartswith=search) \
                | Q(analysisdate__istartswith=search) | Q(value__istartswith=search) | Q(
                sampleid__loginname__username__istartswith=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'sampleid__loginname':
            if row.sampleid.loginname is not None:
                return ('{0}'.format(row.sampleid.loginname))
            else:
                return ("")
        elif column == 'submited_datetime' and row.submited_datetime is not None:

            return ('{0}'.format(row.submited_datetime.strftime('%Y-%m-%d %H:%M')))
        else:
            return super(viewwwmeasureListJson, self).render_column(row, column)


class viewtrendsdataListJson(BaseDatatableView):
    model = models.trends

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(value__istartswith=search) | Q(submited_datetime__istartswith=search) | Q(
                loginname__username__istartswith=search) | Q(fromdate__istartswith=search) | Q(
                todate__istartswith=search) | Q(samplestationid__uwwName__istartswith=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'submited_datetime':
            if row.submited_datetime is not None:
                return ('{0}'.format(row.submited_datetime.strftime('%Y-%m-%d %H:%M')))
            else:
                return super(viewtrendsdataListJson, self).render_column(row, column)
        else:
            return super(viewtrendsdataListJson, self).render_column(row, column)


class viewvariantsdataListJson(BaseDatatableView):
    model = models.variants

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(comment__istartswith=search) | Q(Lineage__istartswith=search) | Q(
                submited_datetime__istartswith=search) | Q(
                loginname__username__istartswith=search) | Q(datestart__istartswith=search) | Q(
                dateend__istartswith=search) | Q(location__uwwName__istartswith=search) | Q(
                VariantType__name__istartswith=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'submited_datetime':
            if row.submited_datetime is not None:
                return ('{0}'.format(row.submited_datetime.strftime('%Y-%m-%d %H:%M')))
            else:
                return super(viewvariantsdataListJson, self).render_column(row, column)
        else:
            return super(viewvariantsdataListJson, self).render_column(row, column)


class viewvariantstypeListJson(BaseDatatableView):
    model = models.variantType

    def filter_queryset(self, qs):
        qs = qs.order_by('pk')
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(name__istartswith=search)
            qs = qs.filter(q)
        return qs


@login_required(login_url='/')
@allowed_users(['admin'])
def exportFile(request):
    columnames = [f.name for f in models.sampledata._meta.get_fields() if not isinstance(f, model1.ManyToOneRel)]

    columnames2 = [f.name for f in models.wwmeasure._meta.get_fields() if not isinstance(f, model1.ManyToOneRel)]

    resp = HttpResponse(content_type='text/csv;charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename=pulse_data.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('samples')
    ws2 = wb.add_sheet('wwmeasure')
    #
    # Sheet header, first row
    row_num = 0
    #
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columnames)):
        ws.write(row_num, col_num, columnames[col_num], font_style)

    for col_num in range(len(columnames2)):
        ws2.write(row_num, col_num, columnames2[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')
    datetime_style = xlwt.easyxf(num_format_str='DD/MM/YYYY HH:MM')
    #
    samples = models.sampledata.objects.all().values_list('id', 'sampleid', 'location__uwwName', 'submited_datetime',
                                                          'datestart', 'dateend', 'notes', 'type', 'collection',
                                                          'loginname__username')
    #

    for row_num, row in enumerate(samples, 1):
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                ws.write(row_num, col_num, row[col_num], datetime_style)
            elif isinstance(row[col_num], datetime.date):
                ws.write(row_num, col_num, row[col_num], date_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wwwmeasures = models.wwmeasure.objects.all().values_list('id', 'wwmeasureid', 'sampleid__sampleid',
                                                             'submited_datetime', 'analysisdate', 'reportdate',
                                                             'fractionAnalyzed', 'covtype__type', 'value', 'notes')
    for row_num, row in enumerate(wwwmeasures, 1):
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                ws2.write(row_num, col_num, row[col_num], datetime_style)
            elif isinstance(row[col_num], datetime.date):
                ws2.write(row_num, col_num, row[col_num], date_style)
            else:
                ws2.write(row_num, col_num, row[col_num], font_style)
    #
    wb.save(resp)

    # export csv
    # writer = csv.writer(resp)
    # writer.writerow(columnames)
    #
    # samples = models.sampledata.objects.all().values_list()
    #
    # for sample in samples:
    #     writer.writerow(sample)
    # writer.writerow([user.username, user.first_name, user.last_name, user.email, ])

    return resp


@login_required(login_url='/')
@allowed_users(['admin', 'trends'])
def exportFileTrends(request):
    columnames = [f.name for f in models.trends._meta.get_fields() if not isinstance(f, model1.ManyToOneRel)]

    resp = HttpResponse(content_type='text/csv;charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename=trends.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('trends')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, colname in enumerate(columnames):
        ws.write(row_num, col_num, colname, font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')
    datetime_style = xlwt.easyxf(num_format_str='DD/MM/YYYY HH:MM')

    trends = models.trends.objects.all().values_list('id', 'submited_datetime', 'fromdate', 'todate',
                                                     'loginname__username', 'samplestationid__uwwName', 'value')

    for row_num, row in enumerate(trends, 1):
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                ws.write(row_num, col_num, row[col_num], datetime_style)
            elif isinstance(row[col_num], datetime.date):
                ws.write(row_num, col_num, row[col_num], date_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(resp)

    return resp


@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def exportFileVariants(request):
    columnames = [f.name for f in models.variants._meta.get_fields() if not isinstance(f, model1.ManyToOneRel)]

    resp = HttpResponse(content_type='text/csv;charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename=variants.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('variants')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, colname in enumerate(columnames):
        ws.write(row_num, col_num, colname, font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')
    datetime_style = xlwt.easyxf(num_format_str='DD/MM/YYYY HH:MM')

    variants = models.variants.objects.all().values_list('id', 'location__uwwName', 'sampleid', 'Lineage',
                                                         'VariantType__name', 'comment', 'submited_datetime',
                                                         'datestart', 'dateend', 'loginname__username')

    for row_num, row in enumerate(variants, 1):
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                ws.write(row_num, col_num, row[col_num], datetime_style)
            elif isinstance(row[col_num], datetime.date):
                ws.write(row_num, col_num, row[col_num], date_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(resp)

    return resp


@login_required(login_url='/')
@allowed_users(['admin'])
def deleteEntrySampleData(request):
    try:
        sample = models.sampledata.objects.filter(pk=request.GET['id'])
        measurements = models.wwmeasure.objects.filter(sampleid=sample[0])
        measurements.delete()
        sample[0].delete()
        success = True
    except Exception as error:
        success = False
    # to redirect ginetai apo to html ajax sto success
    data = {}
    data['success'] = success
    return JsonResponse(data)


@login_required(login_url='/')
@allowed_users(['admin'])
def deleteEntryWWWMeasure(request):
    try:
        measure = models.wwmeasure.objects.filter(pk=request.GET['id'])
        measures = models.wwmeasure.objects.filter(sampleid=measure[0].sampleid)
        if len(measures) == 1:
            sample = models.sampledata.objects.filter(pk=measure[0].sampleid.pk)
            sample[0].delete()
        measure[0].delete()
        success = True
    except Exception as error:
        success = False

    # to redirect ginetai apo to html ajax sto success
    data = {}
    data['success'] = success
    return JsonResponse(data)


@login_required(login_url='/')
@allowed_users(['admin', 'trends'])
def deleteEntryTrendsData(request):
    try:
        trend = models.trends.objects.filter(pk=request.GET['id'])
        trend[0].delete()
        success = True
    except Exception as error:
        success = False
    # to redirect ginetai apo to html ajax sto success
    data = {}
    data['success'] = success
    return JsonResponse(data)


@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def deleteEntryVariantsData(request):
    try:
        variant = models.variants.objects.filter(pk=request.GET['id'])
        variant[0].delete()
        success = True
    except Exception as error:
        success = False
    # to redirect ginetai apo to html ajax sto success
    data = {}
    data['success'] = success
    return JsonResponse(data)


@login_required(login_url='/')
@allowed_users(['admin', 'variants'])
def deleteEntryVariantsTypeData(request):
    try:
        variant_type = models.variantType.objects.filter(pk=request.GET['id'])
        variant_type[0].delete()
        success = True
    except Exception as error:
        success = False
    # to redirect ginetai apo to html ajax sto success
    data = {}
    data['success'] = success
    return JsonResponse(data)


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password Changed successfully')
            return redirect('pulseapp:changePass')
        else:
            messages.error(request, 'Change Password change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'pulseapp/change_password.html', {
        'form': form
    })


def addGroups():
    Group.objects.update_or_create(name='admin')
    Group.objects.update_or_create(name='trends')
    Group.objects.update_or_create(name='variants')

    user = User.objects.create_user(password="pc123456", username="mkiria01", email="mkiria01@ucy.ac.cy",
                                    is_superuser=True)
    user.groups.add(1)

    user = User.objects.create_user(password="pc123456", username="pkaraolia", email="karaolia.parthenopi@ucy.ac.cy")
    user.groups.add(1)

    user = User.objects.create_user(password="pc123456", username="ppavlos", email="pavlou.v.pavlos@ucy.ac.cy")
    user.groups.add(1)


def addSiteData():
    filepath = 'pulseapp/data_files/' + "site_data.json"
    f = open(filepath, "r")
    data = json.loads(f.read())
    for i in data['site']:
        polygon = models.polygon.objects.filter(polygonid=i['polygonID'])
        models.site.objects.update_or_create(siteID=i['siteID'], name=i['name'], description=i['description']
                                             , publicHealthDepartment=i['publicHealthDepartment'],
                                             healthRegion=i['healthRegion']
                                             , type=i['type'], geoLat=i['geoLat'], geoLong=i['geoLong'],
                                             polygonID=polygon[0], link=i['link'], notes=i['notes'])


def adduwtp():
    filepath = 'pulseapp/data_files/' + "uwtp_data.json"
    f = open(filepath, "r")
    data = json.loads(f.read())
    for i in data['uwtp']:
        site = models.site.objects.filter(siteID=i['station_id'])
        models.uwtp.objects.update_or_create(uwwName=i['uwwName'], station=i['station'], agg_name=i['agg_name']
                                             , station_id=site[0], uwwLatitud=i['uwwLatitud']
                                             , uwwLongitu=i['uwwLongitu'], agg_type=i['agg_type'], init=i['init'])


def addSampleData():
    filepath = 'pulseapp/data_files/' + "sample_data.json"
    f = open(filepath, "r")
    data = json.loads(f.read())
    for i in data['pulseapp_sampledata']:
        location = models.uwtp.objects.filter(uwwName=i['location'])
        user = models.User.objects.filter(username=i['loginname'])
        datestart = i['datetimestart'].split(' ')
        dateend = i['datetimeend'].split(' ')
        datestart = datetime.datetime.strptime(datestart[0], '%Y-%m-%d').date()
        dateend = datetime.datetime.strptime(dateend[0], '%Y-%m-%d').date()
        try:
            models.sampledata.objects.update_or_create(location=location[0], submited_datetime=i['datetime'],
                                                       datestart=datestart
                                                       , dateend=dateend, notes=i['notes']
                                                       , sampleid=i['sampleid'], type=i['type'],
                                                       collection=i['collection'], loginname=user[0])
        except:
            models.sampledata.objects.update_or_create(location=location[0], submited_datetime=i['datetime'],
                                                       datestart=datestart
                                                       , dateend=dateend, notes=i['notes']
                                                       , sampleid=i['sampleid'], type=i['type'],
                                                       collection=i['collection'])


def addMeasureData():
    filepath = 'pulseapp/data_files/' + "measure_data.csv"
    f = open(filepath, "r")
    csvreader = csv.reader(f)
    header = next(csvreader)
    for row in csvreader:
        if row[6] == "":
            s_datetime = None
        else:
            s_datetime = row[6]
        sample = models.sampledata.objects.filter(sampleid=row[3])
        covtype = models.covtype.objects.filter(type=row[10], units=row[12])
        try:
            models.wwmeasure.objects.update_or_create(wwmeasureid=row[1], sampleid=sample[0],
                                                      submited_datetime=s_datetime
                                                      , analysisdate=row[7], reportdate=row[8]
                                                      , fractionAnalyzed=row[9], covtype=covtype[0], value=row[11],
                                                      notes=row[23])
        except:
            continue
    f.close()


def addTrendsData():
    filepath = 'pulseapp/data_files/' + "trends_data.json"
    f = open(filepath, "r")
    data = json.loads(f.read())
    for i in data['pulseapp_trends']:
        user = models.User.objects.filter(username=i['loginname'])
        datestart = i['fromdate'].split(' ')
        dateend = i['todate'].split(' ')
        datestart = datetime.datetime.strptime(datestart[0], '%Y-%m-%d').date()
        dateend = datetime.datetime.strptime(dateend[0], '%Y-%m-%d').date()
        try:
            models.trends.objects.update_or_create(submited_datetime=i['datetime'], fromdate=datestart, todate=dateend
                                                   , samplestationid_id=i['samplestationid'], value=i['value'],
                                                   loginname=user[0])
        except:
            models.trends.objects.update_or_create(submited_datetime=i['datetime'], fromdate=datestart, todate=dateend
                                                   , samplestationid_id=i['samplestationid'], value=i['value'])


def addVariantsData():
    filepath = 'pulseapp/data_files/' + "variants_data.json"
    f = open(filepath, "r")
    data = json.loads(f.read())
    for i in data['pulseapp_variants']:
        obj, created = models.variantType.objects.get_or_create(
            name=i['VariantType']
        )
        user = models.User.objects.filter(username=i['loginname'])
        datestart = i['datetimestart'].split(' ')
        dateend = i['datetimeend'].split(' ')
        datestart = datetime.datetime.strptime(datestart[0], '%Y-%m-%d').date()
        dateend = datetime.datetime.strptime(dateend[0], '%Y-%m-%d').date()
        location = models.uwtp.objects.filter(uwwName=i['siteName'])

        try:
            models.variants.objects.update_or_create(location=location[0], sampleid=i['sampleID'], Lineage=i['Lineage'],
                                                     VariantType=obj
                                                     , comment=i['comment'], submited_datetime=i['datetime'],
                                                     datestart=datestart, dateend=dateend, loginname=user[0])
        except:
            models.variants.objects.update_or_create(location=location[0], sampleid=i['sampleID'], Lineage=i['Lineage'],
                                                     VariantType=obj
                                                     , comment=i['comment'], submited_datetime=i['datetime'],
                                                     datestart=datestart, dateend=dateend)
