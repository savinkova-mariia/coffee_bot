import json
from django.db import models
from django.template.defaultfilters import linebreaks_filter
from django.utils.six import python_2_unicode_compatible
from channels import Group


@python_2_unicode_compatible
class Table(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/tables/%s/" % self.slug

    @property
    def group_name(self):
        return "tables-%s" % self.id


@python_2_unicode_compatible
class Post(models.Model):

    tables = models.ForeignKey(Table, related_name="posts")
    body = models.TextField()
    person = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "#%i: %s" % (self.id, self.body_intro())

    def body_intro(self):
        return self.body[:50], self.person[:50]

    def html_body(self):
        return linebreaks_filter(self.body)

    def html_person(self):
        return linebreaks_filter(self.person)

    def send_notification(self):

        notification = {
            "id": self.id,
            "html": self.html_body(),
            "person":self.html_person(),
        }

        Group(self.tables.group_name).send({
            "text": json.dumps(notification),
        })

    def save(self, *args, **kwargs):
        result = super(Post, self).save(*args, **kwargs)
        self.send_notification()
        return result
