from zope.interface import Interface


# Define the valid values for the field.
YES = "yes"
NO = "no"
PARENT = "parent"


class IOptionalHighLightLayer(Interface):
    """Marker interface for plone.browserlayer.
    """
