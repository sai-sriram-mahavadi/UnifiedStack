from django.utils.translation import ugettext_lazy as _

import horizon

class SpawnVMGroup(horizon.PanelGroup):
    slug = "spawnvmgroup"
    name = _("Spawn VM Group")
    panels = ('spawnvm',)


class Unifiedstack(horizon.Dashboard):
    name = _("Unifiedstack")
    slug = "unifiedstack"
    panels = (SpawnVMGroup,)  # Add your panels here.
    default_panel = 'spawnvm'  # Specify the slug of the dashboard's default panel.

horizon.register(Unifiedstack)
