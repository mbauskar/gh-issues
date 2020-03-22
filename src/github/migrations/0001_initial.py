# Generated by Django 3.0.4 on 2020-03-22 18:24

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('github_username', models.CharField(max_length=255, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'GitHubUser',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Label',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('title', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('html_url', models.TextField()),
                ('opened_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('draft', models.BooleanField(default=False)),
                ('merged_at', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pr_author', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(to='github.Label')),
            ],
            options={
                'db_table': 'PullRequest',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Team',
            },
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('full_name', models.CharField(max_length=255, unique=True)),
                ('private', models.BooleanField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github.Organization')),
            ],
            options={
                'db_table': 'Repo',
            },
        ),
        migrations.CreateModel(
            name='PullRequestReviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=255)),
                ('submitted_at', models.DateTimeField()),
                ('pull_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github.PullRequest')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PullRequestReviewer',
            },
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='reviewers',
            field=models.ManyToManyField(through='github.PullRequestReviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('title', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('html_url', models.TextField()),
                ('opened_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(to='github.Label')),
                ('pull_requests', models.ManyToManyField(to='github.PullRequest')),
            ],
            options={
                'db_table': 'Issue',
            },
        ),
        migrations.AddIndex(
            model_name='pullrequest',
            index=models.Index(fields=['number'], name='PullRequest_number_80a585_idx'),
        ),
        migrations.AddIndex(
            model_name='pullrequest',
            index=models.Index(fields=['status'], name='PullRequest_status_c93eb7_idx'),
        ),
        migrations.AddIndex(
            model_name='pullrequest',
            index=models.Index(fields=['author'], name='PullRequest_author__3dfa5b_idx'),
        ),
        migrations.AddIndex(
            model_name='pullrequest',
            index=models.Index(fields=['author', 'status'], name='PullRequest_author__743f8e_idx'),
        ),
        migrations.AddIndex(
            model_name='issue',
            index=models.Index(fields=['number'], name='Issue_number_0c4df3_idx'),
        ),
        migrations.AddIndex(
            model_name='issue',
            index=models.Index(fields=['status'], name='Issue_status_aaa4d6_idx'),
        ),
        migrations.AddIndex(
            model_name='issue',
            index=models.Index(fields=['author'], name='Issue_author__a79bac_idx'),
        ),
        migrations.AddIndex(
            model_name='issue',
            index=models.Index(fields=['assigned_to'], name='Issue_assigne_3e18d5_idx'),
        ),
        migrations.AddIndex(
            model_name='issue',
            index=models.Index(fields=['author', 'status'], name='Issue_author__5e0ce2_idx'),
        ),
    ]
