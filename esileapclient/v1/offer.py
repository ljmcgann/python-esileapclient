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

from esileapclient.common import base

LOG = logging.getLogger(__name__)


class Offer(base.Resource):

    detailed_fields = {
        'availabilities': "Availabilities",
        'end_time': "End Time",
        'project_id': "Project ID",
        'properties': "Properties",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'start_time': "Start Time",
        'status': "Status",
        'uuid': "UUID",
    }

    fields = {
        'uuid': "UUID",
        'start_time': "Start Time",
        'end_time': "End Time",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'status': "Status",
        'availabilities': "Availabilities",
    }

    def __repr__(self):
        return "<Offer %s>" % self._info


class OfferManager(base.Manager):
    resource_class = Offer
    _creation_attributes = ['resource_type', 'resource_uuid',
                            'start_time', 'end_time', 'status',
                            'project_id', 'properties']

    _resource_name = 'offers'

    def create(self, os_esileap_api_version=None, **kwargs):
        """Create an offer based on a kwargs dictionary of attributes.
        :returns: a :class: `Offer` object
        """

        offer = self._create(os_esileap_api_version=os_esileap_api_version,
                             **kwargs)

        return offer

    def list(self, filters, os_esileap_api_version=None):
        """Retrieve a list of offers.
        :returns: A list of offers.
        """

        resource_id = ''

        url_variables = OfferManager._url_variables(filters)
        url = self._path(resource_id) + url_variables

        offers = self._list(url,
                            os_esileap_api_version=os_esileap_api_version)

        if type(offers) is list:
            return offers

    def get(self, offer_uuid):
        """Get an offer with the specified identifier.
        :param offer_uuid: The uuid of an offer.
        :returns: a :class:`Offer` object.
        """

        offer = self._get(offer_uuid)

        return offer

    def delete(self, offer_uuid):
        """Delete an offer with the specified identifier.
        :param offer_uuid: The uuid of an offer.
        :returns: a :class:`Offer` object.
        """

        self._delete(resource_id=offer_uuid)
