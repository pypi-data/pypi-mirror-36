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


class ScoreTrack(object):
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
        'title': 'str',
        'score': 'str',
        'creator': 'str',
        'creation_date': 'datetime',
        'modification_date': 'datetime',
        'default': 'bool',
        'state': 'ScoreTrackState',
        'type': 'ScoreTrackType',
        'url': 'str',
        'media_id': 'str',
        'synchronization_points': 'list[ScoreTrackPoint]'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'score': 'score',
        'creator': 'creator',
        'creation_date': 'creationDate',
        'modification_date': 'modificationDate',
        'default': 'default',
        'state': 'state',
        'type': 'type',
        'url': 'url',
        'media_id': 'mediaId',
        'synchronization_points': 'synchronizationPoints'
    }

    def __init__(self, id=None, title=None, score=None, creator=None, creation_date=None, modification_date=None, default=None, state=None, type=None, url=None, media_id=None, synchronization_points=None):  # noqa: E501
        """ScoreTrack - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._title = None
        self._score = None
        self._creator = None
        self._creation_date = None
        self._modification_date = None
        self._default = None
        self._state = None
        self._type = None
        self._url = None
        self._media_id = None
        self._synchronization_points = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if score is not None:
            self.score = score
        if creator is not None:
            self.creator = creator
        if creation_date is not None:
            self.creation_date = creation_date
        if modification_date is not None:
            self.modification_date = modification_date
        if default is not None:
            self.default = default
        if state is not None:
            self.state = state
        if type is not None:
            self.type = type
        if url is not None:
            self.url = url
        if media_id is not None:
            self.media_id = media_id
        if synchronization_points is not None:
            self.synchronization_points = synchronization_points

    @property
    def id(self):
        """Gets the id of this ScoreTrack.  # noqa: E501

        The unique identifier of the score track  # noqa: E501

        :return: The id of this ScoreTrack.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ScoreTrack.

        The unique identifier of the score track  # noqa: E501

        :param id: The id of this ScoreTrack.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this ScoreTrack.  # noqa: E501

        Title of the track  # noqa: E501

        :return: The title of this ScoreTrack.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this ScoreTrack.

        Title of the track  # noqa: E501

        :param title: The title of this ScoreTrack.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def score(self):
        """Gets the score of this ScoreTrack.  # noqa: E501

        The unique identifier of the score  # noqa: E501

        :return: The score of this ScoreTrack.  # noqa: E501
        :rtype: str
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this ScoreTrack.

        The unique identifier of the score  # noqa: E501

        :param score: The score of this ScoreTrack.  # noqa: E501
        :type: str
        """

        self._score = score

    @property
    def creator(self):
        """Gets the creator of this ScoreTrack.  # noqa: E501

        The unique identifier of the track creator  # noqa: E501

        :return: The creator of this ScoreTrack.  # noqa: E501
        :rtype: str
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this ScoreTrack.

        The unique identifier of the track creator  # noqa: E501

        :param creator: The creator of this ScoreTrack.  # noqa: E501
        :type: str
        """

        self._creator = creator

    @property
    def creation_date(self):
        """Gets the creation_date of this ScoreTrack.  # noqa: E501

        The creation date of the track  # noqa: E501

        :return: The creation_date of this ScoreTrack.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this ScoreTrack.

        The creation date of the track  # noqa: E501

        :param creation_date: The creation_date of this ScoreTrack.  # noqa: E501
        :type: datetime
        """

        self._creation_date = creation_date

    @property
    def modification_date(self):
        """Gets the modification_date of this ScoreTrack.  # noqa: E501

        The modification date of the track  # noqa: E501

        :return: The modification_date of this ScoreTrack.  # noqa: E501
        :rtype: datetime
        """
        return self._modification_date

    @modification_date.setter
    def modification_date(self, modification_date):
        """Sets the modification_date of this ScoreTrack.

        The modification date of the track  # noqa: E501

        :param modification_date: The modification_date of this ScoreTrack.  # noqa: E501
        :type: datetime
        """

        self._modification_date = modification_date

    @property
    def default(self):
        """Gets the default of this ScoreTrack.  # noqa: E501

        True if the track should be used as default audio source  # noqa: E501

        :return: The default of this ScoreTrack.  # noqa: E501
        :rtype: bool
        """
        return self._default

    @default.setter
    def default(self, default):
        """Sets the default of this ScoreTrack.

        True if the track should be used as default audio source  # noqa: E501

        :param default: The default of this ScoreTrack.  # noqa: E501
        :type: bool
        """

        self._default = default

    @property
    def state(self):
        """Gets the state of this ScoreTrack.  # noqa: E501


        :return: The state of this ScoreTrack.  # noqa: E501
        :rtype: ScoreTrackState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ScoreTrack.


        :param state: The state of this ScoreTrack.  # noqa: E501
        :type: ScoreTrackState
        """

        self._state = state

    @property
    def type(self):
        """Gets the type of this ScoreTrack.  # noqa: E501


        :return: The type of this ScoreTrack.  # noqa: E501
        :rtype: ScoreTrackType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ScoreTrack.


        :param type: The type of this ScoreTrack.  # noqa: E501
        :type: ScoreTrackType
        """

        self._type = type

    @property
    def url(self):
        """Gets the url of this ScoreTrack.  # noqa: E501

        The URL of the track  # noqa: E501

        :return: The url of this ScoreTrack.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ScoreTrack.

        The URL of the track  # noqa: E501

        :param url: The url of this ScoreTrack.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def media_id(self):
        """Gets the media_id of this ScoreTrack.  # noqa: E501

        The unique identifier of the track when hosted on an external service. For example, if the url is `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, `mediaId` will be `dQw4w9WgXcQ`   # noqa: E501

        :return: The media_id of this ScoreTrack.  # noqa: E501
        :rtype: str
        """
        return self._media_id

    @media_id.setter
    def media_id(self, media_id):
        """Sets the media_id of this ScoreTrack.

        The unique identifier of the track when hosted on an external service. For example, if the url is `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, `mediaId` will be `dQw4w9WgXcQ`   # noqa: E501

        :param media_id: The media_id of this ScoreTrack.  # noqa: E501
        :type: str
        """

        self._media_id = media_id

    @property
    def synchronization_points(self):
        """Gets the synchronization_points of this ScoreTrack.  # noqa: E501


        :return: The synchronization_points of this ScoreTrack.  # noqa: E501
        :rtype: list[ScoreTrackPoint]
        """
        return self._synchronization_points

    @synchronization_points.setter
    def synchronization_points(self, synchronization_points):
        """Sets the synchronization_points of this ScoreTrack.


        :param synchronization_points: The synchronization_points of this ScoreTrack.  # noqa: E501
        :type: list[ScoreTrackPoint]
        """

        self._synchronization_points = synchronization_points

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
        if not isinstance(other, ScoreTrack):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
