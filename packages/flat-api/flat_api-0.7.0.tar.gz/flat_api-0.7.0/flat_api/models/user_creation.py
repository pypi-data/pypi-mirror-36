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


class UserCreation(object):
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
        'username': 'str',
        'email': 'str',
        'password': 'str',
        'locale': 'FlatLocales'
    }

    attribute_map = {
        'username': 'username',
        'email': 'email',
        'password': 'password',
        'locale': 'locale'
    }

    def __init__(self, username=None, email=None, password=None, locale=None):  # noqa: E501
        """UserCreation - a model defined in OpenAPI"""  # noqa: E501

        self._username = None
        self._email = None
        self._password = None
        self._locale = None
        self.discriminator = None

        self.username = username
        if email is not None:
            self.email = email
        self.password = password
        if locale is not None:
            self.locale = locale

    @property
    def username(self):
        """Gets the username of this UserCreation.  # noqa: E501

        Username of the new account  # noqa: E501

        :return: The username of this UserCreation.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UserCreation.

        Username of the new account  # noqa: E501

        :param username: The username of this UserCreation.  # noqa: E501
        :type: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501
        if username is not None and not re.search('^[A-Za-z0-9\\-_.]+$', username):  # noqa: E501
            raise ValueError("Invalid value for `username`, must be a follow pattern or equal to `/^[A-Za-z0-9\\-_.]+$/`")  # noqa: E501

        self._username = username

    @property
    def email(self):
        """Gets the email of this UserCreation.  # noqa: E501

        Email of the new account  # noqa: E501

        :return: The email of this UserCreation.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserCreation.

        Email of the new account  # noqa: E501

        :param email: The email of this UserCreation.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def password(self):
        """Gets the password of this UserCreation.  # noqa: E501

        Password of the new account  # noqa: E501

        :return: The password of this UserCreation.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this UserCreation.

        Password of the new account  # noqa: E501

        :param password: The password of this UserCreation.  # noqa: E501
        :type: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501
        if password is not None and len(password) < 6:
            raise ValueError("Invalid value for `password`, length must be greater than or equal to `6`")  # noqa: E501

        self._password = password

    @property
    def locale(self):
        """Gets the locale of this UserCreation.  # noqa: E501


        :return: The locale of this UserCreation.  # noqa: E501
        :rtype: FlatLocales
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """Sets the locale of this UserCreation.


        :param locale: The locale of this UserCreation.  # noqa: E501
        :type: FlatLocales
        """

        self._locale = locale

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
        if not isinstance(other, UserCreation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
