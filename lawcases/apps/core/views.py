from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from lawcases.apps.core.forms import CaseForm, EntryForm, ClientForm, KeydateForm
from lawcases.apps.core.forms import PaymentForm, UserForm, GroupForm, FileForm
from django.contrib.auth.decorators import login_required
from lawcases.apps.core.models import Case, File, Matter, Client, Entry, Payment, \
    KeyDate

import json

# Create your views here.


@login_required(login_url='/login')
def add_keydate(request, case_id=0, keydate_id=None):
    user = request.user
    keydate = None
    client_id = None

    if keydate_id:
        keydate = get_object_or_404(KeyDate, pk=keydate_id)

    if request.method == "POST":
        if 'keydate_id' in request.POST:
            keydate_id = request.POST['keydate_id']
            keydate = get_object_or_404(KeyDate, pk=keydate_id)

        form = KeydateForm(request.POST, instance=keydate)
        message = 'something wrong!'
        error = True
        if form.is_valid():
            form.save()
            error = False
            message = 'Success'
        else:
            error = True
            message = json.dumps(form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        if keydate:
            case_id = keydate.case
            client_id = keydate.case.client
        elif case_id:
            case = get_object_or_404(Case, pk=case_id)
            client_id = case.client.id
        payment_form = KeydateForm(initial={'add_user': user.id, 'client': client_id, 'case': case_id},
                                   instance=keydate)

    return render_to_response(
        'cases/keydate_add.html',
        {
            'form': payment_form,
            'keydate_id': keydate_id,
        },
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def add_file(request, model_id=0):
    user = request.user
    model = None
    model_form = None

    if model_id:
        model = get_object_or_404(File, pk=model_id)

    if request.method == "POST":
        if 'file_id' in request.POST:
            case_id = request.POST['file_id']
            model = get_object_or_404(File, pk=case_id)

        form = FileForm(request.POST, request.FILES, instance=model)
        message = 'something wrong!'
        error = True
        if (form.is_valid()):
            error = False
            message = request.POST['name']
            form.save()
        else:
            error = True
            message = json.dumps(form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        # model_form = CaseForm(initial={'add_user': user.id, 'status':1})
        model_form = FileForm(initial={'add_user': user.id, 'case': model_id}, instance=model)

    return render_to_response(
        'cases/file_add.html',

        {'form': model_form,
         'file_id': model_id},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def add_case(request, model_id=0):
    user = request.user
    model = None
    model_form = None

    if model_id:
        model = get_object_or_404(Case, pk=model_id)

    if request.method == "POST":
        if 'case_id' in request.POST:
            case_id = request.POST['case_id']
            model = get_object_or_404(Case, pk=case_id)

        form = CaseForm(request.POST, instance=model)
        message = 'something wrong!'
        error = True
        if (form.is_valid()):
            error = False
            message = request.POST['title']
            form.save()
        else:
            error = True
            message = json.dumps(form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        # model_form = CaseForm(initial={'add_user': user.id, 'status':1})
        model_form = CaseForm(initial={'add_user': user.id, 'case': model_id}, instance=model)

    return render_to_response(
        'cases/add_case.html',

        {'form': model_form,
         'case_id': model_id},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def add_payment(request, case_id=0, payment_id=None):
    user = request.user
    payment = None
    client_id = None

    if payment_id:
        payment = get_object_or_404(Payment, pk=payment_id)

    if request.method == "POST":
        if 'payment_id' in request.POST:
            payment_id = request.POST['payment_id']
            payment = get_object_or_404(Payment, pk=payment_id)

        form = PaymentForm(request.POST, instance=payment)
        message = 'something wrong!'
        error = True
        if form.is_valid():
            form.save()
            error = False
            message = 'Success'
        else:
            error = True
            message = json.dumps(form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        if payment:
            case_id = payment.case
            client_id = payment.case.client
        elif case_id:
            case = get_object_or_404(Case, pk=case_id)
            client_id = case.client.id
        payment_form = PaymentForm(initial={'add_user': user.id, 'client': client_id, 'case': case_id},
                                   instance=payment)

    return render_to_response(
        'payments/add_payment.html',
        {
            'form': payment_form,
            'payment_id': payment_id,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_entry(request, case_id=0, entry_id=None):
    user = request.user
    entry = None
    if entry_id:
        entry = get_object_or_404(Entry, pk=entry_id)

    if request.method == "POST":
        if 'entry_id' in request.POST:
            entry_id = request.POST['entry_id']
            entry = get_object_or_404(Entry, pk=entry_id)

        form = EntryForm(request.POST, instance=entry)
        message = 'something wrong!'
        error = True
        if form.is_valid():
            form.save()
            error = False
            message = 'Success'
        else:
            error = True
            message = json.dumps(form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        if entry:
            case_id = entry.case

        entry_form = EntryForm(initial={'add_user': user.id, 'case': case_id}, instance=entry)

    return render_to_response(
        'entries/add_entry.html',
        {'form': entry_form, 'entry_id': entry_id},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_staff(request, user_id=None):
    user_form = None
    if request.method == "POST":
        user_form = UserForm(request.POST)
        message = 'something wrong!'
        error = True
        if (user_form.is_valid()):
            error = False
            message = request.POST['title']
            user_form.save()
        else:
            error = True
            message = json.dumps(user_form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        user_form = UserForm()

    return render_to_response(
        'staff/add_staff.html',
        {'form': user_form},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_group(request):
    group_form = None
    if request.method == "POST":
        group_form = GroupForm(request.POST)
        message = 'something wrong!'
        error = True
        if (group_form.is_valid()):
            error = False
            message = request.POST['title']
            group_form.save()
        else:
            error = True
            message = json.dumps(group_form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        group_form = GroupForm()

    return render_to_response(
        'staff/add_group.html',
        {'form': group_form},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_client(request, client_id=None):
    user = request.user
    client = None
    client_form = None
    if client_id:
        client = get_object_or_404(Client, pk=client_id)

    if request.method == "POST":
        if 'client_id' in request.POST:
            client_id = request.POST['client_id']
            client = get_object_or_404(Client, pk=client_id)

        form = ClientForm(request.POST, instance=client)
        message = 'something wrong!'
        error = True
        if form.is_valid():
            form.save()
            error = False
            message = 'Success'
        else:
            error = True
            message = json.dumps(form.errors)
        return HttpResponse(json.dumps({'message': message, 'error': error}))
    else:
        client_form = ClientForm(initial={'add_user': user.id, 'client': client_id}, instance=client)

    return render_to_response(
        'clients/add_client.html',
        {
            'form': client_form,
            'client_id': client_id,
        },
        context_instance=RequestContext(request)
    )
    
