import jinja2

OVERWRITES = {
    "trim_blocks": True,
    "lstrip_blocks": True,
}


def environment(**options):
    return jinja2.Environment(
        **{
            **options,
            **OVERWRITES,
        }
    )
