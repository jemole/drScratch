#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from app.models import Teacher, Student , Organization, OrganizationHash
from app.models import Project, Attribute, Sprite, Mastery, Dead, Dashboard
from app.models import Duplicate, Comment, Activity, File

admin.site.register(Organization)
admin.site.register(OrganizationHash)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Project)
admin.site.register(Dashboard)
admin.site.register(Attribute)
admin.site.register(Dead)
admin.site.register(Sprite)
admin.site.register(Mastery)
admin.site.register(Duplicate)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Activity)
