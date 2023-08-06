# -*- coding: utf-8 -*-
from functools import update_wrapper

from django.contrib import admin
from django.shortcuts import render
from django.contrib.admin.options import csrf_protect_m
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.encoding import force_text
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.utils.translation import ugettext

from sneak.admin import SneakAdmin

from admincommand.query import CommandQuerySet
from admincommand.models import AdminCommand as AdminCommandModel
from admincommand import core


class AdminCommandAdmin(SneakAdmin):
    list_display = ("command_name",)

    def get_queryset(self, request):
        # user current user to construct the queryset
        # so that only commands the user can execute
        # will be visible
        return CommandQuerySet(request.user)

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        urlpatterns = [url(r"^run/([\w_]+)", wrap(self.run_command_view))]
        return urlpatterns + super(AdminCommandAdmin, self).get_urls()

    def run_command_view(self, request, url_name):
        admin_command = core.get_admin_commands()[url_name]

        full_permission_codename = "admincommand.%s" % admin_command.permission_codename()
        if not request.user.has_perm(full_permission_codename):
            return HttpResponseForbidden()
        # original needed ``change_form`` context variables
        opts = self.model._meta
        app_label = opts.app_label

        help = admin_command.get_help()

        ctx = {
            # original needed ``change_form.html`` context variables
            "module_name": force_text(opts.verbose_name_plural),
            "title": admin_command.name(),
            "is_popup": False,
            "root_path": None,
            "app_label": app_label,
            # ``run.html`` context
            "command_name": admin_command.name,
            "help": help,
        }

        if request.method == "POST":
            form = admin_command.form(request.POST, command=admin_command)
            if form.is_valid():
                coreponse = core.run_command(admin_command, form.cleaned_data, request.user)
                if not admin_command.asynchronous:
                    ctx["output"] = coreponse
                    return render(request, "admincommand/output.html", ctx)
                else:
                    msg = "Task is set to run in the next 5 minutes or less"
                    msg += " if by any luck, the task went with a duck"
                    msg += " and did not achieve it's duty, ask for help"
                    msg = ugettext(msg)
                    messages.info(request, msg)
                path = reverse("admin:admincommand_admincommand_changelist")
                return HttpResponseRedirect(path)
            else:
                ctx["form"] = form
        else:
            ctx["form"] = admin_command.form(command=admin_command)
        ctx["media"] = mark_safe(ctx["form"].media.render())
        return render(request, "admincommand/run.html", ctx)

    def command_name(self, obj):
        """Used to populate admin change list row with a link to
        the form that of the command"""
        path = reverse("admin:admincommand_admincommand_changelist")
        return '<a href="%srun/%s">%s: %s</a>' % (path, obj.url_name(), obj.name(), obj.get_help())

    command_name.allow_tags = True

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        extra_context = {"title": u"Selectionner une commande à lancer"}
        return super(AdminCommandAdmin, self).changelist_view(request, extra_context)


admin.site.register(AdminCommandModel, AdminCommandAdmin)
