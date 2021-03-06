#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import json

from osc_lib.command import command
from osc_lib import utils as oscutils

from esileapclient.v1.offer import Offer as OFFER_RESOURCE

LOG = logging.getLogger(__name__)


class CreateLeaseOffer(command.ShowOne):
    """Create a new lease offer."""

    log = logging.getLogger(__name__ + ".CreateLeaseOffer")

    def get_parser(self, prog_name):
        parser = super(CreateLeaseOffer, self).get_parser(prog_name)

        parser.add_argument(
            '--end-time',
            dest='end_time',
            required=False,
            help="Time when the offer will expire and no longer be "
                 "'available'.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=True,
            help='Type of the resource to be offered.')
        parser.add_argument(
            '--resource-uuid',
            dest='resource_uuid',
            required=True,
            help="UUID of the resource")
        parser.add_argument(
            '--status',
            dest='status',
            required=False,
            help='State which the offer should be created in.')
        parser.add_argument(
            '--start-time',
            dest='start_time',
            required=False,
            help="Time when the offer will be made 'available'.")
        parser.add_argument(
            '--project-id',
            dest='project_id',
            required=False,
            help="Project ID to assign ownership of the offer to."
                 "If this attribute is not set, ESI-Leap will set the "
                 "project_id to the id of the user which invoked the "
                 "command.")
        parser.add_argument(
            '--properties',
            dest='properties',
            required=False,
            help="Record arbitrary key/value resource property "
                 "information. Pass in as a json object.")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease

        field_list = OFFER_RESOURCE.detailed_fields.keys()

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        if 'properties' in fields:
            fields['properties'] = json.loads(fields['properties'])

        offer = lease_client.offer.create(**fields)

        data = dict([(f, getattr(offer, f, '')) for f in
                    OFFER_RESOURCE.fields])

        return self.dict2columns(data)


class ListLeaseOffer(command.Lister):
    """List lease offers."""

    log = logging.getLogger(__name__ + ".ListLeaseOffer")

    def get_parser(self, prog_name):
        parser = super(ListLeaseOffer, self).get_parser(prog_name)

        parser.add_argument(
            '--long',
            default=False,
            help="Show detailed information about the offers.",
            action='store_true')

        parser.add_argument(
            '--status',
            dest='status',
            required=False,
            help="Show all offers with given status.")

        parser.add_argument(
            '--time-range',
            dest='time_range',
            nargs=2,
            required=False,
            help="Show all offers with start and end times "
                 "which begin and end in the given range."
                 "Must pass in two valid datetime strings."
                 "Example: --time-range 2020-06-30T00:00:00"
                 "2021-06-30T00:00:00")

        parser.add_argument(
            '--availability-range',
            dest='availability_range',
            nargs=2,
            required=False,
            help="Show all offers with availabilities "
                 "which will have no conflicting contracts within "
                 "the given range. Must pass in two valid datetime "
                 "strings."
                 "Example: --availability-range 2020-06-30T00:00:00"
                 "2021-06-30T00:00:00")

        parser.add_argument(
            '--project-id',
            dest='project_id',
            required=False,
            help="Show all offers owned by given project id.")

        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all offers with given resource-type.")

        parser.add_argument(
            '--resource-uuid',
            dest='resource_uuid',
            required=False,
            help="Show all offers with given resource-uuid.")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease

        filters = {
            'status': parsed_args.status,

            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,

            'available_start_time': str(parsed_args.availability_range[0]) if
            parsed_args.availability_range else None,
            'available_end_time': str(parsed_args.availability_range[1]) if
            parsed_args.availability_range else None,

            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        data = lease_client.offer.list(filters)

        if parsed_args.long:
            columns = OFFER_RESOURCE.detailed_fields.keys()
            labels = OFFER_RESOURCE.detailed_fields.values()
        else:
            columns = OFFER_RESOURCE.fields.keys()
            labels = OFFER_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))


class ShowLeaseOffer(command.ShowOne):
    """Show lease offer details."""

    log = logging.getLogger(__name__ + ".ShowLeaseOffer")

    def get_parser(self, prog_name):
        parser = super(ShowLeaseOffer, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="UUID of the offer")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease

        offer = lease_client.offer.get(parsed_args.uuid)._info

        return zip(*sorted(offer.items()))


class DeleteLeaseOffer(command.Command):
    """Unregister lease offer"""

    log = logging.getLogger(__name__ + ".DeleteLeaseOffer")

    def get_parser(self, prog_name):
        parser = super(DeleteLeaseOffer, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="Offer to delete (UUID)")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease
        lease_client.offer.delete(parsed_args.uuid)
        print('Deleted offer %s' % parsed_args.uuid)
