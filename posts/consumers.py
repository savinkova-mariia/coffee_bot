import json
from channels import Group
from .models import Table, Post


def connect_table(message, slug):

    try:
        tables = Table.objects.get(slug=slug)
    except Table.DoesNotExist:
        message.reply_channel.send({
            "text": json.dumps({"error": "bad_slug"}),
            "close": True,
        })
        return
    message.reply_channel.send({"accept": True})
    Group(tables.group_name).add(message.reply_channel)


def disconnect_table(message, slug):
    try:
        tables = Table.objects.get(slug=slug)
    except Table.DoesNotExist:
        return
    Group(tables.group_name).discard(message.reply_channel)

def save_post(message, slug):

    post = json.loads(message['text'])['post']
    tables = Table.objects.get(slug=slug)
    Post.objects.create(tables=tables, body=post)
