# coding=utf-8
from lawcases.apps.core.models import Case, File, Matter, Client, Entry, Payment,\
    KeyDate
from lawcases.apps.core.forms import FileForm, CaseForm, ClientForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.servers.basehttp import FileWrapper
from django.db.models import Sum   
from django.db.models import Q
from datetime import datetime
import mimetypes
import logging
import re
import os

logger = logging.getLogger('CASES')

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None  # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

# Create your views here.
menu = (
        {'name': 'clients','icon' : 'fa-users'},
        {'name': 'cases','icon' : 'fa-legal'},
        {'name': 'staff','icon' : 'fa-gears'},
        #{'name': 'calendar','icon' : 'fa-calendar'},
            # 'accounts':'accounts',
            # 'tasks':'tasks',
            # 'ledg    er':'ledger'
        )

@login_required(login_url='/login') 
def view_case(request, case_id=None):
    """view a single case"""
    case = None
    template = loader.get_template('index.html')
    user = request.user
    extend = 'cases/case'
    context = RequestContext(request, 
            {'template': extend,
    })
    
    if case_id:
        case = get_object_or_404(Case, pk=case_id)
        files = File.objects.filter(case=case_id)
        
        form = FileForm(initial={'add_user': user.id, 'case':case_id})  # A empty, unbound form
        entries = Entry.objects.filter(case=case_id)
        
        case_total = 0
        time_total = 0
        pay_total = 0
        balance = 0
        
        case_sum = entries.aggregate(Sum('cost'))
        if case_sum['cost__sum']:
            case_total = case_sum['cost__sum']
        
        time_sum = entries.aggregate(Sum('entry_time'))
        if time_sum['entry_time__sum']:
            time_total = time_sum['entry_time__sum']
        
        payments = Payment.objects.filter(case=case_id)
        pay_sum = payments.aggregate(Sum('amount'))
        
        if pay_sum['amount__sum']:
            pay_total = pay_sum['amount__sum']
        
        balance = pay_total - case_total
        #prendo i keydates
        
        keydates = KeyDate.objects.filter(case=case_id)
        
        context = RequestContext(request, {
            'menu': menu,
            'case': case,
            'template': extend,
            'files': files,
            'c_menu': 'cases',
            'entries': entries,
            'payments': payments,
            'keydates': keydates,
            'case_total': case_total,
            'time_total': time_total,
            'pay_total' : pay_total,
            'balance':  balance,
            'form': form,
            'matters': Matter.objects.all(),
            'clients' : Client.objects.all(),
        })
        
    return HttpResponse(template.render(context))

@login_required(login_url='/login') 
def view_client(request, client_id=None):
    """view a single client"""
    client = None
    template = loader.get_template('index.html')
    user = request.user
    extend = 'clients/client'
    context = RequestContext(request, 
            {'template': extend,
    })
    
    if client_id:
        client = get_object_or_404(Client, pk=client_id)
        #files = File.objects.filter(client=client_id)
        #form = FileForm(initial={'add_user': user.id, 'case' : client_id})  # A empty, unbound form
        
        cases_list = Case.objects.filter(client=client_id).select_related().values('id')
        
        count_cases = len(list(cases_list))
        entries = Entry.objects.filter(case=cases_list)
        client_sum = entries.aggregate(Sum('cost'))
        time_sum = entries.aggregate(Sum('entry_time'))
        
        payments = Payment.objects.filter(case=cases_list)
        pay_sum = payments.aggregate(Sum('amount'))
        balance = 0
        try:
            balance = pay_sum['amount__sum'] - client_sum['cost__sum']
        except:
            pass
        
        context = RequestContext(request, {
            'menu': menu,
            'client': client,
            'template': extend,
        #    'files': files,
            'entries': entries,
            'payments': payments,
            'client_sum': client_sum,
            'time_sum': time_sum,
            'pay_sum' : pay_sum,
            'balance':  balance,
         #   'form': form,
            'total':count_cases,
            'cases' : Case.objects.all(),
        })
        
    return HttpResponse(template.render(context))


@login_required(login_url='/login')
def search(request):
    cases = None
    clients = None
    template = loader.get_template('index.html')
    
    if 'q' in request.POST:
        query = request.POST['q']
        entry_query = get_query(query, ['title', ])
        cases = Case.objects.filter(entry_query)
        entry_query = get_query(query, ['name','surname'])
        clients = Client.objects.filter(entry_query)
    
    extend = 'cases/result'
    context = RequestContext(request, {
        'menu': menu,
        'cases': cases,
        'clients': clients,
        'template': extend,
    })
    
    return HttpResponse(template.render(context))


@login_required(login_url='/login')      
def view_staff(request, page=1):
    """view staff"""
    template = loader.get_template('index.html')
    users = User.objects.all()
    paginator = Paginator(users, 2)
    try:
        page = int(page)
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages) 
    extend = 'staff/staff'      
    
    context = RequestContext(request, {
        'menu': menu,
        'users': users,
        'template': extend,
    })
    
    return HttpResponse(template.render(context))


@login_required(login_url='/login')      
def view_cases(request, page=1):
    user = request.user
    template = loader.get_template('index.html')
    
    if 'sort' in request.GET:
        request.session['sort'] = request.GET['sort']
        
    if 'sort' not in request.session:
        #default order
        request.session['sort'] = 'due_date'
        
        
    sort = request.session.get('sort')
    
    cases = Case.objects.all().order_by(sort)
    
    paginator = Paginator(cases, 3)
    try:
        page = int(page)
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages) 
    extend = 'cases/cases'      
    
    
    #cases_table = CasesTable(Case.objects.all())
    
    #cases_table.paginate(page=request.GET.get('page', 1), per_page=2)
    
    case_form = CaseForm(initial={'add_user': user.id})
    context = RequestContext(request, {
        'menu': menu,
        'c_menu': 'cases',
        'cases': cases,
        'template': extend,
        'case_form': case_form,
        'matters': Matter.objects.all(),
        'clients' : Client.objects.all(),
        'sort': sort,
    })
    
    return HttpResponse(template.render(context))


@login_required(login_url='/login')      
def view_clients(request, page=1):
    template = loader.get_template('index.html')
    clients = Client.objects.all()
    paginator = Paginator(clients, 2)
    try:
        page = int(page)
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages) 
    extend = 'clients/clients'      
    form = ClientForm()
    context = RequestContext(request, {
        'menu': menu,
        'cases': Case.objects.all(),
        'template': extend,
        'form': form,
        'matters': Matter.objects.all(),
        'clients' : clients,
    })
    
    return HttpResponse(template.render(context))


@login_required(login_url='/login') 
def client_form(request):
    """Insert data into db"""
    if request.method == 'POST': # If the form has been submitted...
        form = ClientForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ClientForm() # An unbound form

    return render(request, 'index.html', {'form': form,})

@login_required(login_url='/login')  
def download(request, path):
    """download a given file"""
    the_file = 'documents'+ path
    filename = os.path.basename(the_file)
    
    response = HttpResponse(FileWrapper(open(the_file, 'rb')),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required(login_url='/login')  
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
             
            # Redirect to the document list after POST
    return HttpResponseRedirect(request.GET['next'])

@login_required(login_url='/login')
def dashboard(request):
    template = loader.get_template('index.html')
    extend = 'dashboard/index'            
    
    entries = Entry.objects.all()
    
    case_sum = entries.aggregate(Sum('cost'))
    time_sum = entries.aggregate(Sum('entry_time'))
    cases = Case.objects.all().order_by('-add_date')[:3]
    payments = Payment.objects.all()
    pay_sum = payments.aggregate(Sum('amount'))
    
    clients = Case.objects.all().order_by('add_date')[:2]
    entries = Entry.objects.all().order_by('add_date')[:2]
    balance = 0
    
    #filtra solo le future
    today = datetime.now()
    keydates = KeyDate.objects.filter(date__gte=today, completed=False).order_by('date')[:10]
    
    try:
        balance = pay_sum['amount__sum'] - case_sum['cost__sum']
    except:
        pass
    context = RequestContext(request, {
        'menu': menu,
        'template': extend,
        'case_sum': case_sum,
        'time_sum': time_sum,
        'cases':cases,
        'clients': clients,
        'entries': entries,
        'pay_sum' : pay_sum,
        'balance':  balance,
        'keydates': keydates,
    })
    return HttpResponse(template.render(context))
    
def index(request):
    user = request.user
    template = loader.get_template('index.html')
    extend = 'index/welcome' 
    if user.is_authenticated():
        return dashboard(request)
                                        
    context = RequestContext(request, {
        'menu': menu,
        'template': extend,
        'next' : './#',
    })
    return HttpResponse(template.render(context))
    
@login_required(login_url='/login')
def calendar(request):
    template = loader.get_template('index.html')
    extend = 'dashboard/calendar' 
    context = RequestContext(request, {
        'menu': menu,
        'template': extend,
        'next' : './#',
    })
    return HttpResponse(template.render(context))
    

