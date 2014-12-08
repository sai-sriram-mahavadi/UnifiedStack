from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.unifiedstack import dashboard


class Spawnvm(horizon.Panel):
    name = _("Spawn VM")
    slug = "spawnvm"


dashboard.Unifiedstack.register(Spawnvm)
