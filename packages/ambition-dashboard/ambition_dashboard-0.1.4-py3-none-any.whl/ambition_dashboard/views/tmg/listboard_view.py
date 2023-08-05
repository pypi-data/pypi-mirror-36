import arrow
import re
import six

from ambition_ae.action_items import AE_TMG_ACTION
from ambition_auth import TMG
from copy import copy
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_action_item.model_wrappers import ActionItemModelWrapper as BaseActionItemModelWrapper
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import CLOSED, NEW, OPEN
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin
from django.utils.text import slugify


class ActionItemModelWrapper(BaseActionItemModelWrapper):
    next_url_name = settings.DASHBOARD_URL_NAMES.get('tmg_listboard_url')


class ListboardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    BaseListboardView):

    ae_tmg_model = 'ambition_ae.aetmg'

    listboard_template = 'tmg_listboard_template'
    listboard_url = 'tmg_listboard_url'
    listboard_panel_style = 'warning'
    listboard_fa_icon = "fa-chalkboard-teacher"
    listboard_model = 'edc_action_item.actionitem'
    listboard_panel_title = 'Adverse Event TMG Reports'
    listboard_view_permission_codename = 'edc_dashboard.view_tmg_listboard'

    model_wrapper_cls = ActionItemModelWrapper
    navbar_name = 'ambition_dashboard'
    navbar_selected_item = 'tmg'
    ordering = '-report_datetime'
    paginate_by = 15
    search_form_url = 'tmg_listboard_url'
    action_type_names = [AE_TMG_ACTION]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AE_TMG_ACTION'] = AE_TMG_ACTION
        context['status'] = NEW if self.request.GET.get('status') not in [
            NEW, OPEN, CLOSED] else self.request.GET.get('status')
        results = copy(context['results'])
        context['new_count'] = self.listboard_model_cls.objects.filter(
            action_type__name=AE_TMG_ACTION,
            status=NEW).count()
        context['open_count'] = self.listboard_model_cls.objects.filter(
            action_type__name=AE_TMG_ACTION,
            status=OPEN).count()
        context['closed_count'] = self.listboard_model_cls.objects.filter(
            action_type__name=AE_TMG_ACTION,
            status=CLOSED).count()
        context['results_new'] = [
            r for r in results if r.object.status == NEW]
        context['results_open'] = [
            r for r in results if r.object.status == OPEN]
        context['results_closed'] = [
            r for r in results if r.object.status == CLOSED]
        context['utc_date'] = arrow.now().date()
        return context

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            action_type__name__in=self.action_type_names)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            return qs.order_by(*ordering)
        return qs

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.
        """
        object_list = []
        for obj in queryset:
            model_wrapper = self.model_wrapper_cls(obj)
            model_wrapper = self.update_instance_permissions(model_wrapper)
            object_list.append(model_wrapper)
        return object_list

    def update_instance_permissions(self, model_wrapper):
        model_wrapper.has_reference_obj_permissions = True
        model_wrapper.has_parent_reference_obj_permissions = True
        model_wrapper.has_related_reference_obj_permissions = True
        try:
            self.request.user.groups.get(name=TMG)
        except ObjectDoesNotExist:
            pass
        else:
            if (model_wrapper.reference_obj
                    and model_wrapper.reference_obj._meta.label_lower == self.ae_tmg_model):
                model_wrapper.has_reference_obj_permissions = (
                    model_wrapper.reference_obj.user_created == self.request.user.username)
            if (model_wrapper.parent_reference_obj
                    and model_wrapper.parent_reference_obj._meta.label_lower == self.ae_tmg_model):
                model_wrapper.has_parent_reference_obj_permissions = (
                    model_wrapper.parent_reference_obj.user_created == self.request.user.username)
            if (model_wrapper.related_reference_obj
                    and model_wrapper.related_reference_obj._meta.label_lower == self.ae_tmg_model):
                model_wrapper.has_related_reference_obj_permissions = (
                    model_wrapper.related_reference_obj.user_created == self.request.user.username)
        return model_wrapper

    def get_queryset_for_listboard(self, filter_options=None, exclude_options=None):
        """Returns a queryset after searching against AE TMG.
        """
        if self.search_term and '|' not in self.search_term:
            ae_tmg_model_cls = django_apps.get_model(self.ae_tmg_model)
            search_terms = self.search_term.split('+')
            q = None
            q_objects = []
            for search_term in search_terms:
                q_objects.append(
                    Q(subject_identifier__icontains=slugify(search_term)))
                q_objects.append(
                    Q(action_identifier__icontains=slugify(search_term)))
                q_objects.append(
                    Q(ae_initial__ae_classification__icontains=slugify(search_term)))
                q_objects.append(
                    Q(user_created__iexact=slugify(search_term)))
                q_objects.append(
                    Q(parent_reference_identifier__icontains=slugify(search_term)))
                q_objects.append(
                    Q(related_reference_identifier__icontains=slugify(search_term)))
            for q_object in q_objects:
                if q:
                    q = q | q_object
                else:
                    q = q_object
            tmg_queryset = ae_tmg_model_cls.objects.filter(q or Q())
            queryset = self.listboard_model_cls.objects.filter(
                action_identifier__in=[
                    obj.action_identifier for obj in tmg_queryset],
                **filter_options).exclude(**exclude_options)
        else:
            queryset = super().get_queryset_for_listboard(
                filter_options=filter_options,
                exclude_options=exclude_options)
        return queryset
