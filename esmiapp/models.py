from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from transliterate import translit
from datetime import date
from esmiproject.settings import FILES_ISSUES


ADRESS_TYPE = {'ua': 'юридический адрес', 'pa': 'почтовый адрес', 'am': 'адрес местонахождения'}
GENDERS = {'man': 'man', 'woman': 'woman'}


class Users(AbstractUser):
    class Meta:
        db_table = 'users'

    middle_name = models.CharField(max_length=250)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=5, choices=GENDERS.items(), help_text='Выберите пол')
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=6, null=True, blank=True)
    apartment = models.CharField(max_length=6, null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'middle_name']


#  logic of content
class EsmiIndexLevel1(models.Model):
    class Meta:
        db_table = 'esmi_IndexLevel1'
        verbose_name = 'Index 1'
        verbose_name_plural = 'Index 1'

    indexlevel1 = models.CharField(max_length=256)

    def __str__(self):
        return self.indexlevel1


class EsmiIndexLevel2(models.Model):
    class Meta:
        db_table = 'esmi_IndexLevel2'
        verbose_name = 'Index 2'
        verbose_name_plural = 'Index 2'

    indexlevel1 = models.ForeignKey(EsmiIndexLevel1)
    indexlevel2ru = models.CharField(max_length=256)
    indexlevel2en = models.CharField(max_length=256)
    indexlevel2url = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.indexlevel2ru

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.indexlevel2url = slugify(translit(self.indexlevel2ru, 'ru', reversed=True))
        super(EsmiIndexLevel2, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class EsmiPublishers(models.Model):
    class Meta:
        db_table = 'esmi_publishers'

    publisher = models.CharField(max_length=256)
    def __str__(self):
        return self.publisher


class EsmiEditionTypes(models.Model):
    class Meta:
        db_table = 'esmi_editiontypes'
        verbose_name = 'edition type'
        verbose_name_plural = 'edition type'

    editiontype_ru = models.CharField(max_length=256, null=True)
    editiontype_en = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.editiontype_ru


class EsmiEditionNames(models.Model):
    class Meta:
        db_table = 'esmi_editionnames'
        verbose_name = 'edition name'
        verbose_name_plural = 'edition name'

    ideditiontype = models.ForeignKey(EsmiEditionTypes)
    idpublisher = models.ForeignKey(EsmiPublishers, on_delete=models.CASCADE, null=True)
    idindexlevel2 = models.ForeignKey(EsmiIndexLevel2, null=True)
    editionname_ru = models.CharField(max_length=256, null=True)
    editionname_en = models.CharField(max_length=256, null=True)
    editionname_url = models.CharField(max_length=256, null=True, blank=True, unique=True)

    def __str__(self):
        return self.editionname_ru

    def save(self, force_insert=False, force_update=False, using=None,
              update_fields=None):
        self.editionname_url = slugify(translit(self.editionname_ru, 'ru', reversed=True))
        super(EsmiEditionNames, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class EsmiIssues(models.Model):
    class Meta:
        db_table = 'esmi_issues'
        verbose_name = 'issues'
        verbose_name_plural = 'issues'

    def get_saving_path(self, filename):
        return '{}/{}/{}'.format(FILES_ISSUES, self.dateissues.year, filename)

    idnameedition = models.ForeignKey(EsmiEditionNames, null=True)
    number = models.IntegerField()
    throughnumber = models.IntegerField()
    dateissues = models.DateField()
    dateload = models.DateTimeField(null=True)
    filefree = models.FileField(upload_to=get_saving_path, null=True)
    fileprivate = models.FileField(upload_to=get_saving_path, null=True)
    previewissue = models.ImageField(upload_to=get_saving_path, null=True)

    def __str__(self):
        return '{} №{} ({}) {}'.format(self.idnameedition, self.number, self.throughnumber, self.dateissues)


class EsmiIssueprices(models.Model):
    class Meta:
        db_table = 'esmi_issueprices'
        verbose_name = 'esmi_issueprices'
        verbose_name_plural = 'esmi_issueprices'

    idissue = models.ForeignKey(EsmiIssues)
    price = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return '{} - {}'.format(self.idissue, self.price)


class EsmiTags(models.Model):
    class Meta:
        db_table = 'esmi_tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tag'

    tag = models.CharField(max_length=256, unique=True)
    tag_url = models.CharField(max_length=256, unique=True, null=True)

    def __str__(self):
        return self.tag

    def save(self, force_insert=False, force_update=False, using=None,
              update_fields=None):
        self.tag_url = slugify(translit(self.tag, 'ru', reversed=True))
        super(EsmiTags, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class EsmiNewsTypes(models.Model):
    class Meta:
        db_table = 'esmi_newstype'

    newstype = models.CharField(max_length=256)

    def __str__(self):
        return self.newstype

class EsmiAuthors(models.Model):
    class Meta:
        db_table = 'esmi_authors'
        verbose_name = 'authors'
        verbose_name_plural = 'authors'

    author = models.CharField(max_length=256)

    def __str__(self):
        return self.author

TYPESARTICAL = {'f': 'free', 'c': 'close'}
class EsmiNews(models.Model):
    class Meta:
        db_table = 'esmi_news'
        verbose_name = 'News'
        verbose_name_plural = 'News'

    newstype = models.ForeignKey(EsmiNewsTypes, blank=True)
    idauthor = models.ForeignKey(EsmiAuthors, blank=True, verbose_name='author')
    idissue = models.ForeignKey(EsmiIssues, blank=True)
    idindexlevel2 = models.ForeignKey(EsmiIndexLevel2)
    tags = models.ManyToManyField(EsmiTags, blank=True)
    meta_tags = models.CharField(max_length=256, blank=True)
    meta_description = models.CharField(max_length=256, blank=True)
    header = models.CharField(max_length=256, blank=True)
    picture = models.ImageField(max_length=256, blank=True)
    pct_description = models.CharField(max_length=256, blank=True)
    alt = models.CharField(max_length=256, blank=True)
    description = RichTextUploadingField(blank=True)
    body_free = RichTextUploadingField(blank=True)
    body_close = RichTextUploadingField(blank=True)
    data_create = models.DateTimeField(blank=True)
    data_publication = models.DateTimeField(blank=True)
    typeartical = models.CharField(max_length=1, choices=TYPESARTICAL.items(), help_text='Тип материала')


class EsmiIsPayedIssue(models.Model):
    class Meta:
        db_table = 'esmi_payedissue'
    iduser = models.ForeignKey(Users)
    idissue = models.ForeignKey(EsmiIssues)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField(default=date.today, blank=True)


class EsmiIsLikedIssue(models.Model):
    class Meta:
        db_table = 'esmi_likedissue'
    iduser = models.ForeignKey(Users)
    idissue = models.ForeignKey(EsmiIssues)
