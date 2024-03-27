from outdated.outdated.models import Maintainer


def test_unique_boolean_field(db, maintainer_factory):
    maintainer = maintainer_factory()
    assert Maintainer.objects.count() == 1
    assert maintainer.is_primary

    other_maintainer = maintainer_factory(source=maintainer.source)

    assert Maintainer.objects.count() == 2
    assert not other_maintainer.is_primary

    other_maintainer.is_primary = True
    other_maintainer.save()

    maintainer.refresh_from_db()
    assert other_maintainer.is_primary is True
    assert maintainer.is_primary is False
