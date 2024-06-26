# Generated by Django 4.2.7 on 2023-12-30 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('title', models.CharField(db_column='title', max_length=200, verbose_name='Title')),
                ('content', models.TextField(db_column='content', verbose_name='Content')),
                ('keywords', models.CharField(db_column='keywords', max_length=200, null=True, verbose_name='Keywords')),
                ('image', models.URLField(db_column='image', null=True, verbose_name='Image')),
                ('isPublic', models.BooleanField(db_column='is_public', default=True, verbose_name='Is Public')),
                ('isDrafted', models.BooleanField(db_column='is_drafted', default=False, verbose_name='Is Drafted')),
                ('author', models.ForeignKey(db_column='author_id', on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
                'db_table': 'blog',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BlogAction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('action', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('comment', 'comment'), ('report', 'report')], db_column='action', max_length=10, verbose_name='Action')),
                ('blog', models.ForeignKey(db_column='blog_id', on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='blog.blog', verbose_name='Blog')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='user_blog_actions', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Blog Action',
                'verbose_name_plural': 'Blog Actions',
                'db_table': 'blog_action',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('comment', models.TextField(db_column='content', verbose_name='Content')),
                ('action', models.ForeignKey(db_column='blog_action_id', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.blogaction', verbose_name='action')),
                ('user', models.ForeignKey(db_column='author_id', on_delete=django.db.models.deletion.CASCADE, related_name='user_blog_comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Blog Comment',
                'verbose_name_plural': 'Blog Comments',
                'db_table': 'blog_comment',
                'managed': True,
            },
        ),
    ]
