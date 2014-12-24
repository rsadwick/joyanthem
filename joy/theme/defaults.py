from mezzanine.conf import register_setting


register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description="Sequence of setting names available within templates.",
    editable=False,

    default=("AFFILIATE_AMAZON_ID", "AFFILIATE_ITUNES_ID"),
    append=True,
)

register_setting(
    name="AFFILIATE_AMAZON_ID",
    description="Affiliate id for amazon.",
    editable=True,
    label="Amazon ID",
    default=("000"),
)

register_setting(
    name="AFFILIATE_ITUNES_ID",
    description="Affiliate id for itunes.",
    editable=True,
    label="iTunes ID",
    default=("000"),
)