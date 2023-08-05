from .command_auth import AuthCommand
from datetime import timedelta
from docopt import docopt


class Create(AuthCommand):
    def usage(self, subcommand=None):
        usage = """
usage:
  rock create --help
  rock create collection --help
  rock create integration --help
  rock create [-h] --file=YAMLFILE
  rock create collection <name> [-h] [options] [<data_source_url> ...]
  rock create integration <name> --type=INTEGRATION_TYPE [-h] [options]


commands:
  collection          create a new collection.
                      you can optionally specify data sources to automatically
                      feed into the collection such as AWS S3.

  integration         create a new integration.
                      an integration object can store access details and 
                      credentials of an external account (eg: an AWS account) 
                      and can be used at collection creation time to access
                      one or more data sources.
                      integration objects allows you to securely store access
                      credentials and share across the team without actually 
                      exposing the access credentials and secrets.

options for `rock create`:
  -d TEXT, --desc=TEXT        human readable description of the new resource
  -f FILE, --file=FILE        create all resources specified in the YAML file,
                              run `rock -o yaml describe <collection>` on an
                              existing collection to see the YAML format
  -h, --help                  show this help message and exit
        """
        usage_subcommand = {
            "collection":
                """
arguments for `rock create collection`:
  <name>              name of the new collection you wish to create
  <data_source_url>   specify the data source to auto ingest in order to
                      populate the collection
                      eg: s3://my-precious-s3-bucket
                          s3://my-precious-s3-bucket/data/path/prefix

options for `rock create collection`:
  --integration=INTEGRATION_NAME                Specify an integration that will be used to access
                                                the source of this collection. For sources that don't need
                                                special access or credentials, this can be left unspecified.
  --event-time-field=FIELD_NAME                 specify a root-level field, representing time in one of the
                                                formats supported by rockset (look at --event-time-format)
                                                this field will be mapped to event-time.
  --event-time-format=TIME_FORMAT               specify the format of time in which the field mapped to event-time
                                                is formatted in your documents. (requires --event-time-field)
                                                supported formats   * milliseconds_since_epoch (default)
                                                                    * seconds_since_epoch
  --event-time-default-timezone=TIME_ZONE       specify the time zone of event times in the documents which will be
                                                added into this collection. (requires --event-time-field)
                                                default is 'UTC' (supported time zones: one of standard IANA time zones)
  --retention=RETENTION_DURATION                specify the minimum time duration using short-hand notation
                                                (such as 24h, 8d, or 13w) for which documents in this collection
                                                will be retained before being automatically deleted.
                                                (default: none i.e., documents will be retained indefinitely)

examples:

    Create a collection and source all contents from an AWS S3 bucket:

        $ rock create collection customers s3://customers-mycompany-com

    Create a collection from an AWS S3 bucket but only pull a particular
    path prefix within the S3 bucket:

        $ rock create collection event-log \\
            s3://event-log.mycompany.com/root/path/in/bkt --integration aws-rockset-readonly

    Create a collection and map a field to event-time

        $ rock create collection \\
            my-event-data --event-time-field timestamp --event-time-format milliseconds_since_epoch

    Create a collection with retention set to 10 days

        $ rock create collection \\
            my-event-data --retention="10d"

        """,
            "integration":
                """
arguments for `rock create integration`:
  <name>              name of the new integration you wish to create

options for `rock create integration --type=AWS`:
  --aws_access_key_id=AWS_ACCESS_KEY_ID              AWS access key id
  --aws_secret_access_key=AWS_SECRET_ACCESS_KEY      AWS secret access key
  
examples:

    Create an integration of type AWS
    
        $ rock create integration aws-rockset-readonly --type=AWS --aws_access_key_id=access_key --aws_secret_access_key=secret_access
        """
        }

        if subcommand == 'collection':
            return usage + usage_subcommand['collection']
        elif subcommand == 'integration':
            return usage + usage_subcommand['integration']
        elif subcommand == 'all':
            return (
                usage + usage_subcommand['collection'] +
                usage_subcommand['integration']
            )

        return usage

    def convert_to_seconds(self, duration):

        num = duration[:-1]
        try:
            num = int(num)
        except ValueError as e:
            ret = 'invalid duration "{}"\n'.format(num)
            raise ValueError(ret)

        unit = duration[-1]
        try:
            if unit == 'h':
                time_delta = timedelta(hours=num)
            elif unit == 'd':
                time_delta = timedelta(days=num)
            elif unit == 'w':
                time_delta = timedelta(weeks=num)
            else:
                ret = 'invalid time unit "{}"\n'.format(unit)
                raise ValueError(ret)
        except OverflowError:
            ret = 'duration "{}" too large for specified time units\n'.format(
                num
            )
            raise OverflowError(ret)

        return int(time_delta.total_seconds())

    def _source_s3(self, s3_url, integration):
        parts = s3_url[5:].split('/')
        bucket = parts[0]
        prefixes = (len(parts) > 1) and ['/'.join(parts[1:])] or []

        return self.client.Source.s3(
            bucket=bucket, prefixes=prefixes, integration=integration
        )

    def parse_args(self, args):
        parsed_args = dict(docopt(self.usage('all'), argv=args, help=False))

        # handle help
        if parsed_args['--help']:
            if parsed_args['collection']:
                ret = self.usage('collection')
            elif parsed_args['integration']:
                ret = self.usage('integration')
            else:
                ret = self.usage()
            raise SystemExit(ret.strip())

        # see if YAMLFILE was specified
        fn = parsed_args['--file']
        if fn:
            self.set_batch_items('resource', self._parse_yaml_file(fn))
            return {}

        # construct a valid CreateRequest object
        resource = {}

        if parsed_args['collection']:
            resource['name'] = parsed_args['<name>']
            sources = []
            if parsed_args['--desc']:
                resource['description'] = parsed_args['--desc']

            integration = parsed_args['--integration']
            if integration is not None:
                integration = self.client.Integration.retrieve(integration)

            resource['type'] = 'COLLECTION'
            for source in parsed_args['<data_source_url>']:
                if source[:5] == 's3://':
                    sources.append(self._source_s3(source, integration))
                else:
                    ret = 'Error: invalid data source URL "{}"\n'.format(source)
                    ret += self.usage()
                    ret += self.usage('collection')
                    raise SystemExit(ret.strip())

            # handle options related to event_time
            if parsed_args['--event-time-field'] is not None:
                resource['event_time_field'] = parsed_args['--event-time-field']
                resource['event_time_format'
                        ] = parsed_args['--event-time-format']
                resource['event_time_default_timezone'
                        ] = parsed_args['--event-time-default-timezone']
            elif parsed_args['--event-time-format'] is not None:
                ret = 'Error: --event-time-field is required to specify --event-time-format'
                ret += self.usage()
                raise SystemExit(ret.strip())
            elif parsed_args['--event-time-default-timezone'] is not None:
                ret = 'Error: --event-time-field is required to specify --event-time-default-timezone'
                ret += self.usage()
                raise SystemExit(ret.strip())

            #handle retention
            if parsed_args['--retention'] is not None:
                try:
                    retention = self.convert_to_seconds(
                        parsed_args['--retention']
                    )
                    resource['retention_secs'] = retention
                except ValueError as e:
                    ret = 'Error: invalid argument "{}" for --retention, {}'.format(
                        parsed_args['--retention'], str(e)
                    )
                    ret += self.usage()
                    raise SystemExit(ret)
                except OverflowError as e:
                    ret = 'Error: invalid value "{}" for --retention, {}'.format(
                        parsed_args['--retention'], str(e)
                    )
                    ret += self.usage()
                    raise SystemExit(ret)

            resource['sources'] = sources
            return {'resource': resource}
        elif parsed_args['integration']:
            resource['name'] = parsed_args['<name>']
            resource['type'] = 'INTEGRATION'

            if parsed_args['--desc']:
                resource['description'] = parsed_args['--desc']

            if parsed_args['--type'] == 'AWS':
                resource['integration_type'] = 'AWS'

                resource['aws_access_key_id'
                        ] = parsed_args['--aws_access_key_id']
                resource['aws_secret_access_key'
                        ] = parsed_args['--aws_secret_access_key']
            else:
                ret = "Error: invalid integration type, supported types: AWS\n"
                ret += self.usage()
                ret += self.usage('integration')
                raise SystemExit(ret.strip())

        return {'resource': resource}

    def go(self):
        self.logger.info('create {}'.format(self.resource))
        rtype = self.resource.pop('type', None)
        if rtype is None:
            return 1
        if rtype == 'COLLECTION':
            return self.go_collection(self.resource)
        elif rtype == 'INTEGRATION':
            return self.go_integration(self.resource)
        return 1

    def go_collection(self, resource):
        name = resource.pop('name')
        c = self.client.Collection.create(name, **resource)
        self.lprint(0, 'Collection "%s" was created successfully.' % (c.name))
        return 0

    def go_integration(self, resource):
        name = resource.pop('name')
        integration_type = resource.pop('integration_type')

        if integration_type == 'AWS':
            aws_access_key_id = resource.pop('aws_access_key_id')
            aws_secret_access_key = resource.pop('aws_secret_access_key')
            try:
                i = self.client.Integration.AWS.create(
                    name, aws_access_key_id, aws_secret_access_key, **resource
                )
                self.lprint(
                    0, 'Integration "%s" was created successfully.' % (i.name)
                )
            except ValueError as e:
                ret = "Error: {}\n".format(str(e))
                ret += self.usage('integration')
                raise SystemExit(ret.strip())
            return 0
        return 1
