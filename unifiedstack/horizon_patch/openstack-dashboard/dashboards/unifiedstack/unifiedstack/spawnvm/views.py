from horizon import views




def get_nova_creds():
    d = {}
    d['username'] = 'admin'
    d['api_key'] = '7dc21602f8fa4aca'
    d['auth_url'] = 'http://10.0.2.15:5000/v2.0/'
    d['project_id'] = 'admin'
    return d

def start_server():
    print "Printing Credentials: "
    print get_nova_creds()
    from novaclient.v1_1 import client
    from credentials import get_nova_creds
    creds = get_nova_creds()
    nova = client.Client(**creds)
    print nova.security_groups.list()
    print nova.floating_ip_pools.list()
    print nova.images.list()
    print nova.flavors.list()
    print nova.networks.list()
    print nova.keypairs.list()
    key_name = "sample_key"
    keypair = None
    try:
        keypair = nova.keypairs.find(name=key_name)
    except Exception:
        keypair = nova.keypairs.create(name=key_name)
    image = nova.images.find(name="cirros")
    flavor = nova.flavors.find(name="m1.tiny")
    network = nova.networks.find(label="private")
    server = nova.servers.create(name = "prakash-server-test",
                                 image = image.id,
                                 flavor = flavor.id,
                                 network = network.id,
                                 key_name = keypair.name)

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'unifiedstack/spawnvm/index.html'
    
    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class ResultView(views.APIView):
    # A very simple class-based view...
    # Run python code

    print "Printing Credentials: "
    print get_nova_creds()
    from novaclient.v1_1 import client
    from credentials import get_nova_creds
    creds = get_nova_creds()
    nova = client.Client(**creds)
    print nova.security_groups.list()
    print nova.floating_ip_pools.list()
    print nova.images.list()
    print nova.flavors.list()
    print nova.networks.list()
    print nova.keypairs.list()
    key_name = "sample_key"
    keypair = None
    try:
        keypair = nova.keypairs.find(name=key_name)
    except Exception:
        keypair = nova.keypairs.create(name=key_name)
    image = nova.images.find(name="cirros")
    flavor = nova.flavors.find(name="m1.tiny")
    network = nova.networks.find(label="private")
    server = nova.servers.create(name = "prakash-server-test",
                                 image = image.id,
                                 flavor = flavor.id,
                                 network = network.id,
                                 key_name = keypair.name)

    template_name = 'unifiedstack/spawnvm/results.html'
    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
    
