from django.contrib.auth.views import password_change, password_reset, password_reset_confirm, password_reset_complete
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic import UpdateView
from esmiapp.models import EsmiIndexLevel2, EsmiNews, EsmiEditionNames, EsmiEditionTypes, Users, EsmiIssues, \
    EsmiIsLikedIssue, EsmiIsPayedIssue, EsmiIssueprices, EsmiAuthors
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from .forms import MyUserCreationForm
from datetime import date


# ------------------------------------------------------------------------------------------
# авторизация
def login_view(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            args['login error'] = "User not found"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


# ------------------------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('/')


# ------------------------------------------------------------------------------------------
# регистрация нового пользователя
def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = MyUserCreationForm()
    if request.POST:
        newuser_form = MyUserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = authenticate(username=newuser_form.cleaned_data['username'],
                                   password=newuser_form.cleaned_data['password2'],)
            login(request, newuser)
            return redirect('/')
        else:
            print(newuser_form.errors)
            args['form'] = newuser_form
    return render_to_response('register.html', args)


# ------------------------------------------------------------------------------------------
# смена пароля
def change_password(request):
    template_response = password_change(request, template_name='registration/password_change_form.html',
                                        post_change_redirect='profile')
    return template_response


# ------------------------------------------------------------------------------------------
# восстановление пароля
def reset_password(request):
    template_response = password_reset(request, template_name='registration/password_reset_form.html',
                                       post_reset_redirect='password_reset_done')
    return template_response


class PasswordResetDone(TemplateView):
    template_name = 'registration/password_reset_done.html'


def reset_password_confirm(request):
    template_response = password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
                                               post_reset_redirect='password_reset_complete')
    return template_response


def reset_password_complete(request):
    template_response = password_reset_complete(request, template_name='registration/password_reset_complete.html')
    return template_response


# ------------------------------------------------------------------------------------------
# личный кабинет
class Profile(DetailView):
    model = Users
    template_name = 'account/account.html'

    def get_object(self, queryset=None):
        return self.request.user


# ------------------------------------------------------------------------------------------
class My_issues(TemplateView):
    template_name = 'account/my_issues.html'


# ------------------------------------------------------------------------------------------
class Liked_issues(TemplateView):
    template_name = 'account/liked_issues.html'
    model = EsmiIsLikedIssue

    def get_context_data(self, **kwargs):
        iduser = self.request.user.id
        context = super(Liked_issues, self).get_context_data(**kwargs)
        context['likedissues'] = EsmiIsLikedIssue.objects.filter(iduser=iduser)
        return context


# ------------------------------------------------------------------------------------------
# платежи (оплаченные издания)
class Payments(DetailView):
    template_name = 'account/payments.html'
    model = EsmiIsPayedIssue

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        iduser = self.request.user.id
        context = super(Payments, self).get_context_data(**kwargs)
        context['payedissues'] = EsmiIsPayedIssue.objects.filter(iduser=iduser)
        return context


# ------------------------------------------------------------------------------------------
# изменение данных пользователя
class UsersUpdate(UpdateView):
    model = Users
    fields = ['last_name', 'first_name', 'middle_name', 'email', 'birthday', 'phonenumber', 'gender', 'country',
              'index', 'city', 'street', 'house', 'apartment']
    template_name = 'account/users_update_form.html'

    def get_success_url(self):
        return reverse_lazy('profile')


# ------------------------------------------------------------------------------------------
# домашняя страница
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_simple_data(self, newsset):

        if len(newsset) > 4:
            newsset = newsset[0:3]
        news_dict = dict()
        news_all = dict()
        i = 0
        for news in newsset:
            i += 1
            news_dict = dict()
            news_dict['id'] = news.id
            news_dict['header'] = news.header
            news_dict['image'] = news.picture
            news_dict['body'] = '{}{}'.format(news.body_free[0:300], '...')
            news_all['news{}'.format(i)] = news_dict
        return news_all


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        EsmiIndexLevel2s = EsmiIndexLevel2.objects.all()
        indexlevel2_dict = dict()
        for IndexLevel2 in EsmiIndexLevel2s:
            news = EsmiNews.objects.filter(idindexlevel2=IndexLevel2.id).order_by('data_publication')
            indexlevel2_dict[IndexLevel2] = self.get_simple_data(news)

        context['indexlevel2s_list'] = indexlevel2_dict
        return context


# ------------------------------------------------------------------------------------------
class NewsFeed(TemplateView):
    template_name = 'news/newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeed, self).get_context_data(**kwargs)
        indexlevel2 = EsmiIndexLevel2.objects.get(indexlevel2en=kwargs['indexlevel2'])
        context['h1'] = indexlevel2
        context['news_list'] = EsmiNews.objects.all().filter(idindexlevel2_id=indexlevel2.id)
        return context


# ------------------------------------------------------------------------------------------
class News(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super(News, self).get_context_data(**kwargs)
        news = EsmiNews.objects.get(id=kwargs['idnews'])
        issue = EsmiIssues.objects.get(pk=news.idissue_id)
        context['author'] = EsmiAuthors.objects.get(pk=news.idauthor_id)
        ename = EsmiEditionNames.objects.get(pk=issue.idnameedition_id)
        context['etype'] = EsmiEditionTypes.objects.get(pk=ename.ideditiontype_id)
        context['ename'] = ename
        context['issue_id'] = issue.throughnumber
        context['issue'] = '{}'.format(issue.__str__())
        context['same_news'] = EsmiNews.objects.all().order_by('data_publication').exclude(pk=kwargs['idnews'])[0:3]
        context['news'] = EsmiNews.objects.get(id=kwargs['idnews'])
        return context


# ------------------------------------------------------------------------------------------
def get_latest_by_indexlevel2(indexlevel2s, etype=None):
    dict_indexlevel2 = dict()

    for indexlevel2 in indexlevel2s:
        editionNames = EsmiEditionNames.objects.filter(idindexlevel2=indexlevel2.id, ideditiontype=etype.id)
        issues = EsmiIssues.objects.filter(idnameedition__in=editionNames.values('id'))
        if issues.exists():
            issues = issues.latest('dateload')
        dict_indexlevel2[indexlevel2] = issues
    return dict_indexlevel2


# ------------------------------------------------------------------------------------------
def get_by_etypes(etypes):
    dict_objs = dict()
    indexlevel2s = EsmiIndexLevel2.objects.all()
    for etype in etypes:
        dict_indexlevel2 = get_latest_by_indexlevel2(indexlevel2s, etype=etype)
        dict_objs[etype] = dict_indexlevel2
    return dict_objs


# ------------------------------------------------------------------------------------------
class Etype(TemplateView):
    template_name = 'catalog/etype.html'

    def get_context_data(self, **kwargs):
        context = super(Etype, self).get_context_data(**kwargs)
        etype = EsmiEditionTypes.objects.filter(editiontype_en=kwargs['etype'])
        context['etype'] = etype.get()
        context['data'] = get_by_etypes(etype)[etype.get()]
        return context


# ------------------------------------------------------------------------------------------
class IndexLevel2(TemplateView):
    template_name = 'catalog/topic.html' # as defaulte

    def engine_indexlevel2(self):
        pass

    def engine_issues(self, **kwargs):
        dict_obj = dict()
        issues = EsmiIssues.objects.filter(editionname_url=kwargs['param1'])
        dict_obj['issues'] = issues
        enames_id = issues.get(1).idnameedition
        ename = EsmiEditionNames.objects.filter(idnameedition=enames_id)
        dict_obj['ename'] = ename
        return dict_obj

    def get_context_data(self, **kwargs):
        context = super(IndexLevel2, self).get_context_data(**kwargs)
        etype = EsmiEditionTypes.objects.filter(editiontype_en=kwargs['etype'])
        indexlevel2 = EsmiIndexLevel2.objects.filter(indexlevel2en=kwargs['param1'])

        if len(indexlevel2) == 0:
            self.template_name = 'catalog/issues.html'
            context['indexlevel2'] = None
            dict_issues = self.engine_issues(kwargs)
            context['issues'] = dict_issues['issues']
            context['ename'] = dict_issues['ename']
        else:
            template_name = 'catalog/topic.html'
            enames = EsmiEditionNames.objects.filter(ideditiontype=etype.get().id, idindexlevel2=indexlevel2.get().id)
            dict_ename = dict()
            for ename in enames:
                issues = EsmiIssues.objects.filter(idnameedition=ename.id)
                if issues.exists():
                    issues = issues.latest('dateload')
                dict_ename[ename] = issues
                context['indexlevel2'] = indexlevel2.get()
                context['enames'] = dict_ename

        context['etype'] = etype.get()
        return context


# ------------------------------------------------------------------------------------------
class BaseIssue(TemplateView):

    def check_user(self, user_id, issue):
        result = False
        try:
            usr = Users.objects.get(pk=user_id)
            obj = EsmiIsPayedIssue.objects.get(idissue=issue.get(), iduser=usr)
        except ObjectDoesNotExist:
            obj = False

        if obj:
            result = True
        return result

    def get_context_data(self, **kwargs):
        context = super(BaseIssue, self).get_context_data(**kwargs)
        issue = EsmiIssues.objects.filter(throughnumber=kwargs['issue'])
        ename = EsmiEditionNames.objects.get(pk=issue.get().idnameedition_id)
        etype = EsmiEditionTypes.objects.get(pk=ename.ideditiontype_id)
        issue_price = EsmiIssueprices.objects.get(idissue=issue.get().id)
        context['issues'] = EsmiIssues.objects.filter(idnameedition=ename.id).exclude(throughnumber=kwargs['issue'])\
            .order_by('-throughnumber')
        context['current_issue'] = issue.get()
        context['ename'] = ename
        context['etype'] = etype
        context['issue_price'] = issue_price
        context['cheek_user'] = self.check_user(self.request.user.id, issue)
        return context


# ------------------------------------------------------------------------------------------
class Issues(BaseIssue):
    template_name = 'catalog/issue.html'

    def get_context_data(self, **kwargs):
        context = super(Issues, self).get_context_data(**kwargs)
        return context


# ------------------------------------------------------------------------------------------
class Buy(BaseIssue):
    template_name = 'sale/buy.html'

    def get_context_data(self, **kwargs):
        context = super(Buy, self).get_context_data(**kwargs)
        if self.request.user.id is None:
            self.template_name = 'demand.html'
        return context


# ------------------------------------------------------------------------------------------
# страница каталога
class Catalog(TemplateView):
    template_name = 'catalog/catalog.html'

    def get_context_data(self, **kwargs):
        context = super(Catalog, self).get_context_data(**kwargs)
        etypes = EsmiEditionTypes.objects.all()
        context['etype_list'] = get_by_etypes(etypes)
        return context


# ------------------------------------------------------------------------------------------
class Success(BaseIssue):
    template_name = 'sale/success.html'

    def get_context_data(self, **kwargs):
        context = super(Success, self).get_context_data(**kwargs)
        if self.request.user.id == None:
            self.template_name = 'demand.html'
        else:
            ename = EsmiEditionNames.objects.filter(editionname_url=kwargs['ename'])
            issue = EsmiIssues.objects.filter(idnameedition=ename.get().id, throughnumber=kwargs['issue'])
            issueprice = EsmiIssueprices.objects.get(idissue=issue)
            usr = Users.objects.get(pk=self.request.user.id)
            payed_obj = EsmiIsPayedIssue(iduser=usr, idissue=issue.get(), amount=issueprice.price, date=date.today())
            payed_obj.save()
        return context
