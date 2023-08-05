# coding: utf-8

"""
    Flat API

    The Flat API allows you to easily extend the abilities of the [Flat Platform](https://flat.io), with a wide range of use cases including the following:  * Creating and importing new music scores using MusicXML, MIDI, Guitar Pro (GP3, GP4, GP5, GPX, GP), PowerTab, TuxGuitar and MuseScore files * Browsing, updating, copying, exporting the user's scores (for example in MP3, WAV or MIDI) * Managing educational resources with Flat for Education: creating & updating the organization accounts, the classes, rosters and assignments.  The Flat API is built on HTTP. Our API is RESTful It has predictable resource URLs. It returns HTTP response codes to indicate errors. It also accepts and returns JSON in the HTTP body. The [schema](/swagger.yaml) of this API follows the [OpenAPI Initiative (OAI) specification](https://www.openapis.org/), you can use and work with [compatible Swagger tools](http://swagger.io/open-source-integrations/). This API features Cross-Origin Resource Sharing (CORS) implemented in compliance with [W3C spec](https://www.w3.org/TR/cors/).  You can use your favorite HTTP/REST library for your programming language to use Flat's API. This specification and reference is [available on Github](https://github.com/FlatIO/api-reference).  Getting Started and learn more:  * [API Overview and interoduction](https://flat.io/developers/docs/api/) * [Authentication (Personal Access Tokens or OAuth2)](https://flat.io/developers/docs/api/authentication.html) * [SDKs](https://flat.io/developers/docs/api/sdks.html) * [Rate Limits](https://flat.io/developers/docs/api/rate-limits.html) * [Changelog](https://flat.io/developers/docs/api/changelog.html)   # noqa: E501

    OpenAPI spec version: 2.7.0
    Contact: developers@flat.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class LtiCredentials(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'name': 'str',
        'lms': 'LmsName',
        'organization': 'str',
        'creator': 'str',
        'creation_date': 'datetime',
        'last_usage': 'datetime',
        'consumer_key': 'str',
        'consumer_secret': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'lms': 'lms',
        'organization': 'organization',
        'creator': 'creator',
        'creation_date': 'creationDate',
        'last_usage': 'lastUsage',
        'consumer_key': 'consumerKey',
        'consumer_secret': 'consumerSecret'
    }

    def __init__(self, id=None, name=None, lms=None, organization=None, creator=None, creation_date=None, last_usage=None, consumer_key=None, consumer_secret=None):  # noqa: E501
        """LtiCredentials - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._name = None
        self._lms = None
        self._organization = None
        self._creator = None
        self._creation_date = None
        self._last_usage = None
        self._consumer_key = None
        self._consumer_secret = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if lms is not None:
            self.lms = lms
        if organization is not None:
            self.organization = organization
        if creator is not None:
            self.creator = creator
        if creation_date is not None:
            self.creation_date = creation_date
        if last_usage is not None:
            self.last_usage = last_usage
        if consumer_key is not None:
            self.consumer_key = consumer_key
        if consumer_secret is not None:
            self.consumer_secret = consumer_secret

    @property
    def id(self):
        """Gets the id of this LtiCredentials.  # noqa: E501

        The unique identifier of this couple of credentials  # noqa: E501

        :return: The id of this LtiCredentials.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this LtiCredentials.

        The unique identifier of this couple of credentials  # noqa: E501

        :param id: The id of this LtiCredentials.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this LtiCredentials.  # noqa: E501

        Name of the couple of credentials  # noqa: E501

        :return: The name of this LtiCredentials.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LtiCredentials.

        Name of the couple of credentials  # noqa: E501

        :param name: The name of this LtiCredentials.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def lms(self):
        """Gets the lms of this LtiCredentials.  # noqa: E501


        :return: The lms of this LtiCredentials.  # noqa: E501
        :rtype: LmsName
        """
        return self._lms

    @lms.setter
    def lms(self, lms):
        """Sets the lms of this LtiCredentials.


        :param lms: The lms of this LtiCredentials.  # noqa: E501
        :type: LmsName
        """

        self._lms = lms

    @property
    def organization(self):
        """Gets the organization of this LtiCredentials.  # noqa: E501

        The unique identifier of the Organization associated to these credentials  # noqa: E501

        :return: The organization of this LtiCredentials.  # noqa: E501
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this LtiCredentials.

        The unique identifier of the Organization associated to these credentials  # noqa: E501

        :param organization: The organization of this LtiCredentials.  # noqa: E501
        :type: str
        """

        self._organization = organization

    @property
    def creator(self):
        """Gets the creator of this LtiCredentials.  # noqa: E501

        Unique identifier of the user who created these credentials  # noqa: E501

        :return: The creator of this LtiCredentials.  # noqa: E501
        :rtype: str
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this LtiCredentials.

        Unique identifier of the user who created these credentials  # noqa: E501

        :param creator: The creator of this LtiCredentials.  # noqa: E501
        :type: str
        """

        self._creator = creator

    @property
    def creation_date(self):
        """Gets the creation_date of this LtiCredentials.  # noqa: E501

        The creation date of thse credentials  # noqa: E501

        :return: The creation_date of this LtiCredentials.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this LtiCredentials.

        The creation date of thse credentials  # noqa: E501

        :param creation_date: The creation_date of this LtiCredentials.  # noqa: E501
        :type: datetime
        """

        self._creation_date = creation_date

    @property
    def last_usage(self):
        """Gets the last_usage of this LtiCredentials.  # noqa: E501

        The last time these credentials were used  # noqa: E501

        :return: The last_usage of this LtiCredentials.  # noqa: E501
        :rtype: datetime
        """
        return self._last_usage

    @last_usage.setter
    def last_usage(self, last_usage):
        """Sets the last_usage of this LtiCredentials.

        The last time these credentials were used  # noqa: E501

        :param last_usage: The last_usage of this LtiCredentials.  # noqa: E501
        :type: datetime
        """

        self._last_usage = last_usage

    @property
    def consumer_key(self):
        """Gets the consumer_key of this LtiCredentials.  # noqa: E501

        OAuth 1 Consumer Key  # noqa: E501

        :return: The consumer_key of this LtiCredentials.  # noqa: E501
        :rtype: str
        """
        return self._consumer_key

    @consumer_key.setter
    def consumer_key(self, consumer_key):
        """Sets the consumer_key of this LtiCredentials.

        OAuth 1 Consumer Key  # noqa: E501

        :param consumer_key: The consumer_key of this LtiCredentials.  # noqa: E501
        :type: str
        """

        self._consumer_key = consumer_key

    @property
    def consumer_secret(self):
        """Gets the consumer_secret of this LtiCredentials.  # noqa: E501

        OAuth 1 Consumer Secret  # noqa: E501

        :return: The consumer_secret of this LtiCredentials.  # noqa: E501
        :rtype: str
        """
        return self._consumer_secret

    @consumer_secret.setter
    def consumer_secret(self, consumer_secret):
        """Sets the consumer_secret of this LtiCredentials.

        OAuth 1 Consumer Secret  # noqa: E501

        :param consumer_secret: The consumer_secret of this LtiCredentials.  # noqa: E501
        :type: str
        """

        self._consumer_secret = consumer_secret

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, LtiCredentials):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
