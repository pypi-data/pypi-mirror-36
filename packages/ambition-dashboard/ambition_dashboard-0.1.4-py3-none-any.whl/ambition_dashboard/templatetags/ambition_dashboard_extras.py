from django import template
from django.conf import settings
from edc_constants.constants import ABNORMAL

register = template.Library()


@register.inclusion_tag(
    f'ambition_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/'
    f'buttons/screening_button.html', takes_context=True)
def screening_button(context, model_wrapper):
    title = ['Edit subject\' screening form.']
    if model_wrapper.object.mental_status == ABNORMAL:
        title.append('(Note: mental status is abnormal)')

    return dict(
        perms=context['perms'],
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag(f'ambition_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/'
                        f'buttons/eligibility_button.html')
def eligibility_button(subject_screening_model_wrapper):
    comment = []
    obj = subject_screening_model_wrapper.object
    tooltip = None
    if not obj.eligible:
        comment = obj.reasons_ineligible.split(',')
    comment = list(set(comment))
    comment.sort()
    return dict(eligible=obj.eligible, comment=comment, tooltip=tooltip)


@register.inclusion_tag(
    f'ambition_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/buttons/consent_button.html',
    takes_context=True)
def consent_button(context, model_wrapper):
    title = ['Consent subject to participate.']
    consent_version = model_wrapper.consent.version
    if model_wrapper.object.mental_status == ABNORMAL:
        title.append('(Note: mental status is abnormal)')
    return dict(
        perms=context['perms'],
        screening_identifier=model_wrapper.object.screening_identifier,
        add_consent_href=model_wrapper.consent.href,
        consent_version=consent_version,
        title=' '.join(title))


@register.inclusion_tag(f'ambition_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/'
                        f'buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag(f'ambition_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/'
                        f'tmg/listboard_result.html', takes_context=True)
def tmg_listboard_results(context, results, empty_message=None):
    context['results'] = results
    context['empty_message'] = empty_message
    return context
