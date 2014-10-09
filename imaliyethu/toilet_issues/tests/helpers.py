""" Helpers for toilet issue tests. """

from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


def create_issue(value, **translations):
    """ Create a toilet issue with translations. """
    issue = ToiletIssue.objects.create(value=value)
    for language, description in translations.items():
        issue.translations.add(
            ToiletIssueTranslation(language=language, description=description))
    return issue


def canonicalize_issue(data):
    """ Sort the translations listed in an issue for ease of comparison """
    if isinstance(data, dict):
        if 'translations' in data:
            data['translations'].sort(key=lambda x: x['id'])
        return data
    return [canonicalize_issue(i) for i in sorted(data, key=lambda x: x['id'])]


def serialize_issue(*args):
    """ Hand-serialize an issue for comparison with the real thing. """
    if len(args) == 1:
        issue = args[0]
        return canonicalize_issue({
            'id': issue.pk,
            'value': issue.value,
            'translations': serialize_translation(*issue.translations.all())
        })
    else:
        return canonicalize_issue([serialize_issue(i) for i in args])


def serialize_translation(*args):
    """ Hand-serialize a translation for comparison with the real thing. """
    if len(args) == 1:
        trans = args[0]
        return {
            'id': trans.pk,
            'issue': trans.issue.pk,
            'language': trans.language,
            'description': trans.description,
        }
    else:
        return [serialize_translation(t) for t in args]
