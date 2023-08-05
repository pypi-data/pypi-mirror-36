from .command_rest import RESTCommand
from .util.type_util import TypeUtil

from docopt import docopt

class Describe(RESTCommand):
    def usage(self):
        return """
usage: rock describe [-ah] <resource-type> <name> ...

Show details about collections or integrations.

arguments:
    <name>                name of the collection or integration
    <resource-type>       oneof collections or integrations.

Valid resource types:
  * collections (aka 'col')
  * integrations (aka 'int')

options:
    -a, --all           display extended stats
    -h, --help          show this help message and exit"""

    def parse_args(self, args):
        parsed_args = dict(docopt(self.usage(), argv=args))
        if parsed_args['--help']:
            ret = self.usage()
            raise SystemExit(ret.strip())

        resource_type = TypeUtil.parse_resource_type(parsed_args['<resource-type>'])
        if resource_type is None:
            ret = 'Error: invalid resource type "{}"\n'.format(resource_type)
            ret += self.usage()
            raise SystemExit(ret.strip())
        return {"resource": {'type': resource_type, 'name': parsed_args['<name>']}}

    def go(self):
        self.logger.info('describe {}'.format(self.resource))
        if self.resource["type"] == TypeUtil.TYPE_COLLECTION:
            return self.go_collection()
        elif self.resource["type"] == TypeUtil.TYPE_INTEGRATION:
            return self.go_integration()
        else:
            return 1

    def go_collection(self):
        for name in self.resource['name']:
            path = '/orgs/{}/ws/{}/collections/{}'.format(
                'self', 'commons', name
            )
            deets = self.get(path)
            if 'data' in deets and 'sources' in deets['data']:
                nsrcs = []
                for src in deets['data']['sources']:
                    nsrcs.append({k: v for k, v in src.items() if v})
                deets['data']['sources'] = nsrcs
            desc = {}
            if 'data' in deets:
                desc = {k: v for k, v in deets['data'].items() if v}
            self.print_list_yaml(0, [desc])
        return 0

    def go_integration(self):
        for name in self.resource['name']:
            path = '/orgs/{}/integrations/{}'.format(
                'self', name
            )
            response = self.get(path)
            if 'data' in response and 'resources' in response['data']:
                nsrcs = []
                for src in response['data']['resources']:
                    nsrcs.append({k: v for k, v in src.items() if v})
                response['data']['resources'] = nsrcs
            desc = {}
            if 'data' in response:
                desc = {k: v for k, v in response['data'].items() if v}
            self.print_list_yaml(0, [desc])
        return 0
