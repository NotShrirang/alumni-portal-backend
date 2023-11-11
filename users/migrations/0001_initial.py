# Generated by Django 4.2.7 on 2023-11-11 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("csc", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlumniPortalUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=60, unique=True, verbose_name="email"),
                ),
                ("firstName", models.CharField(max_length=255)),
                ("lastName", models.CharField(max_length=255)),
                (
                    "department",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "Computer Engineering"),
                            ("2", "Mechanical Engineering"),
                            ("3", "Electronics & Telecommunication Engineering"),
                            ("4", "Electrical Engineering"),
                            ("5", "Information Technology"),
                            ("6", "Artificial Intelligence & Data Science"),
                            ("7", "First Year Engineering"),
                            ("8", "MBA"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "privilege",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "Super Admin"),
                            ("2", "Staff"),
                            ("3", "Alumni"),
                            ("4", "Student"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("resume", models.URLField(blank=True, max_length=255, null=True)),
                (
                    "profilePicture",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "phoneNumber",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="csc.city",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "db_table": "alumni_portal_user",
            },
        ),
        migrations.CreateModel(
            name="SuperAdmin",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="superAdmin",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Super Admin",
                "verbose_name_plural": "Super Admins",
                "db_table": "super_admin",
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("batch", models.IntegerField()),
                ("enrollmentYear", models.DateTimeField()),
                ("passingOutYear", models.DateTimeField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Student",
                "verbose_name_plural": "Students",
                "db_table": "student",
            },
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("college", models.CharField(max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staff",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Faculty",
                "verbose_name_plural": "Faculty",
                "db_table": "faculty",
            },
        ),
        migrations.CreateModel(
            name="Alumni",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("batch", models.IntegerField()),
                ("enrollmentYear", models.DateTimeField()),
                ("passingOutYear", models.DateTimeField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alumni",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Alumni",
                "verbose_name_plural": "Alumni",
                "db_table": "alumni",
            },
        ),
    ]
