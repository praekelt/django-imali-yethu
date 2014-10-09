""" Helpers for toilet issue tests. """

from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


def create_issue(value, **translations):
    """ Create a toilet issue with translations. """
    issue = ToiletIssue.objects.create(value=value)
    for language, description in translations.items():
        issue.translations.add(
            ToiletIssueTranslation(language=language, description=description))
    return issue


def serialize_issue(*args):
    """ Hand-serialize an issue for comparison with the real thing. """
    if len(args) == 1:
        issue = args[0]
        return {
            'id': issue.pk,
            'value': issue.value,
            'translations': serialize_translation(*issue.translations.all())
        }
    else:
        return [serialize_issue(i) for i in sorted(args, key=lambda x: x.pk)]


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
        return [serialize_translation(t)
                for t in sorted(args, key=lambda x: x.pk)]
