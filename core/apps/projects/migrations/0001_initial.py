# Generated by Django 3.1.7 on 2021-03-12 10:15

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Epic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
            ],
            options={
                'verbose_name': 'epic',
                'verbose_name_plural': 'epics',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_features_as_owner', related_query_name='projects_feature_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'feature',
                'verbose_name_plural': 'features',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.TextField(help_text='As a "who", I want to "what" so that "why".', verbose_name='title')),
                ('label', models.CharField(choices=[('STORY', 'Story'), ('BUG', 'Bug')], default='STORY', max_length=10, verbose_name='label')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('READY', 'Ready'), ('TO_DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('IN_REVIEW', 'In Review'), ('DONE', 'Done'), ('BLOCKED', 'Blocked'), ('CANCELLED', 'Cancelled')], default='DRAFT', max_length=16, verbose_name='status')),
                ('points', models.FloatField(blank=True, choices=[(None, '?'), (0.0, '0'), (0.5, '1/2'), (1.0, '1'), (2.0, '2'), (3.0, '3'), (5.0, '5'), (8.0, '8'), (13.0, '13'), (20.0, '20'), (40.0, '40'), (100.0, '100')], default=None, null=True, verbose_name='story points')),
                ('trust', models.SmallIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, verbose_name='trust level')),
                ('assignee', models.ForeignKey(blank=True, help_text='Who works on this very story?', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_issues', related_query_name='projects_issue', to=settings.AUTH_USER_MODEL, verbose_name='assignee')),
                ('epic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', related_query_name='issue', to='projects.epic', verbose_name='epic')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', related_query_name='issue', to='projects.feature', verbose_name='feature')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_issues_as_owner', related_query_name='projects_issue_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'issue',
                'verbose_name_plural': 'issues',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_products_as_owner', related_query_name='projects_product_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['-changed_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('done', models.BooleanField(default=False, verbose_name='done')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', related_query_name='task', to='projects.issue', verbose_name='issue')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_tasks_as_owner', related_query_name='projects_task_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('started_at', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('finished_at', models.DateField(blank=True, null=True, verbose_name='finished date')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_sprints_as_owner', related_query_name='projects_sprint_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', related_query_name='sprint', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'sprint',
                'verbose_name_plural': 'sprints',
                'ordering': ['started_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_skills_as_owner', related_query_name='projects_skill_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', related_query_name='skill', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'skill',
                'verbose_name_plural': 'skills',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='issue',
            name='skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', related_query_name='issue', to='projects.skill', verbose_name='required skill'),
        ),
        migrations.AddField(
            model_name='issue',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', related_query_name='issue', to='projects.sprint', verbose_name='sprint'),
        ),
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_initiatives_as_owner', related_query_name='projects_initiative_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiatives', related_query_name='initiative', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'initiative',
                'verbose_name_plural': 'initiatives',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalTask',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('done', models.BooleanField(default=False, verbose_name='done')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='task', to='projects.issue', verbose_name='issue')),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_task_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical task',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSprint',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('started_at', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('finished_at', models.DateField(blank=True, null=True, verbose_name='finished date')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_sprint_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='sprint', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'historical sprint',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSkill',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_skill_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='skill', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'historical skill',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_product_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical product',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalIssue',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.TextField(help_text='As a "who", I want to "what" so that "why".', verbose_name='title')),
                ('label', models.CharField(choices=[('STORY', 'Story'), ('BUG', 'Bug')], default='STORY', max_length=10, verbose_name='label')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('READY', 'Ready'), ('TO_DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('IN_REVIEW', 'In Review'), ('DONE', 'Done'), ('BLOCKED', 'Blocked'), ('CANCELLED', 'Cancelled')], default='DRAFT', max_length=16, verbose_name='status')),
                ('points', models.FloatField(blank=True, choices=[(None, '?'), (0.0, '0'), (0.5, '1/2'), (1.0, '1'), (2.0, '2'), (3.0, '3'), (5.0, '5'), (8.0, '8'), (13.0, '13'), (20.0, '20'), (40.0, '40'), (100.0, '100')], default=None, null=True, verbose_name='story points')),
                ('trust', models.SmallIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, verbose_name='trust level')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assignee', models.ForeignKey(blank=True, db_constraint=False, help_text='Who works on this very story?', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_issue', to=settings.AUTH_USER_MODEL, verbose_name='assignee')),
                ('epic', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='issue', to='projects.epic', verbose_name='epic')),
                ('feature', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='issue', to='projects.feature', verbose_name='feature')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_issue_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('skill', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='issue', to='projects.skill', verbose_name='required skill')),
                ('sprint', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='issue', to='projects.sprint', verbose_name='sprint')),
            ],
            options={
                'verbose_name': 'historical issue',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInitiative',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_initiative_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='initiative', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'historical initiative',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFeature',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_feature_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='feature', to='projects.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'historical feature',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEpic',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('feature', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='epic', to='projects.feature', verbose_name='feature')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('initiative', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='epic', to='projects.initiative', verbose_name='initiative')),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_epic_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical epic',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAcceptanceCriterion',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(blank=True, editable=False, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('done', models.BooleanField(default=False, verbose_name='done')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='acceptance_criterion', to='projects.issue', verbose_name='issue')),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, help_text='Owner of this very object.', limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', related_query_name='projects_acceptancecriterion_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'historical acceptance criterion',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='feature',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', related_query_name='feature', to='projects.product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='epic',
            name='feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='epics', related_query_name='epic', to='projects.feature', verbose_name='feature'),
        ),
        migrations.AddField(
            model_name='epic',
            name='initiative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epics', related_query_name='epic', to='projects.initiative', verbose_name='initiative'),
        ),
        migrations.AddField(
            model_name='epic',
            name='owner',
            field=models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_epics_as_owner', related_query_name='projects_epic_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.CreateModel(
            name='AcceptanceCriterion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text="Tip: You can use Markdown's syntax!", verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('done', models.BooleanField(default=False, verbose_name='done')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acceptance_criteria', related_query_name='acceptance_criterion', to='projects.issue', verbose_name='issue')),
                ('owner', models.ForeignKey(help_text='Owner of this very object.', limit_choices_to={'is_active': True}, on_delete=models.SET(accounts.models.get_sentinel_user), related_name='projects_acceptancecriterions_as_owner', related_query_name='projects_acceptancecriterion_as_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'acceptance criterion',
                'verbose_name_plural': 'acceptance criteria',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='sprint',
            constraint=models.UniqueConstraint(fields=('title', 'product'), name='sprint_title_unique_per_product'),
        ),
        migrations.AddConstraint(
            model_name='skill',
            constraint=models.UniqueConstraint(fields=('title', 'product'), name='skill_title_unique_per_product'),
        ),
        migrations.AddConstraint(
            model_name='initiative',
            constraint=models.UniqueConstraint(fields=('title', 'product'), name='initiative_title_unique_per_product'),
        ),
        migrations.AddConstraint(
            model_name='feature',
            constraint=models.UniqueConstraint(fields=('title', 'product'), name='feature_title_unique_per_product'),
        ),
        migrations.AddConstraint(
            model_name='epic',
            constraint=models.UniqueConstraint(fields=('title', 'initiative'), name='epic_title_unique_per_initiative'),
        ),
    ]