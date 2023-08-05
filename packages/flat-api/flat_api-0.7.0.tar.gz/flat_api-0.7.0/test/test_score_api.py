# coding: utf-8

"""
    Flat API

    The Flat API allows you to easily extend the abilities of the [Flat Platform](https://flat.io), with a wide range of use cases including the following:  * Creating and importing new music scores using MusicXML, MIDI, Guitar Pro (GP3, GP4, GP5, GPX, GP), PowerTab, TuxGuitar and MuseScore files * Browsing, updating, copying, exporting the user's scores (for example in MP3, WAV or MIDI) * Managing educational resources with Flat for Education: creating & updating the organization accounts, the classes, rosters and assignments.  The Flat API is built on HTTP. Our API is RESTful It has predictable resource URLs. It returns HTTP response codes to indicate errors. It also accepts and returns JSON in the HTTP body. The [schema](/swagger.yaml) of this API follows the [OpenAPI Initiative (OAI) specification](https://www.openapis.org/), you can use and work with [compatible Swagger tools](http://swagger.io/open-source-integrations/). This API features Cross-Origin Resource Sharing (CORS) implemented in compliance with [W3C spec](https://www.w3.org/TR/cors/).  You can use your favorite HTTP/REST library for your programming language to use Flat's API. This specification and reference is [available on Github](https://github.com/FlatIO/api-reference).  Getting Started and learn more:  * [API Overview and interoduction](https://flat.io/developers/docs/api/) * [Authentication (Personal Access Tokens or OAuth2)](https://flat.io/developers/docs/api/authentication.html) * [SDKs](https://flat.io/developers/docs/api/sdks.html) * [Rate Limits](https://flat.io/developers/docs/api/rate-limits.html) * [Changelog](https://flat.io/developers/docs/api/changelog.html)   # noqa: E501

    OpenAPI spec version: 2.7.0
    Contact: developers@flat.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import flat_api
from flat_api.api.score_api import ScoreApi  # noqa: E501
from flat_api.rest import ApiException


class TestScoreApi(unittest.TestCase):
    """ScoreApi unit test stubs"""

    def setUp(self):
        self.api = flat_api.api.score_api.ScoreApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_score_collaborator(self):
        """Test case for add_score_collaborator

        Add a new collaborator  # noqa: E501
        """
        pass

    def test_add_score_track(self):
        """Test case for add_score_track

        Add a new video or audio track to the score  # noqa: E501
        """
        pass

    def test_create_score(self):
        """Test case for create_score

        Create a new score  # noqa: E501
        """
        pass

    def test_create_score_revision(self):
        """Test case for create_score_revision

        Create a new revision  # noqa: E501
        """
        pass

    def test_delete_score(self):
        """Test case for delete_score

        Delete a score  # noqa: E501
        """
        pass

    def test_delete_score_comment(self):
        """Test case for delete_score_comment

        Delete a comment  # noqa: E501
        """
        pass

    def test_delete_score_track(self):
        """Test case for delete_score_track

        Remove an audio or video track linked to the score  # noqa: E501
        """
        pass

    def test_edit_score(self):
        """Test case for edit_score

        Edit a score's metadata  # noqa: E501
        """
        pass

    def test_fork_score(self):
        """Test case for fork_score

        Fork a score  # noqa: E501
        """
        pass

    def test_ger_user_likes(self):
        """Test case for ger_user_likes

        List liked scores  # noqa: E501
        """
        pass

    def test_get_group_scores(self):
        """Test case for get_group_scores

        List group's scores  # noqa: E501
        """
        pass

    def test_get_score(self):
        """Test case for get_score

        Get a score's metadata  # noqa: E501
        """
        pass

    def test_get_score_collaborator(self):
        """Test case for get_score_collaborator

        Get a collaborator  # noqa: E501
        """
        pass

    def test_get_score_collaborators(self):
        """Test case for get_score_collaborators

        List the collaborators  # noqa: E501
        """
        pass

    def test_get_score_comments(self):
        """Test case for get_score_comments

        List comments  # noqa: E501
        """
        pass

    def test_get_score_revision(self):
        """Test case for get_score_revision

        Get a score revision  # noqa: E501
        """
        pass

    def test_get_score_revision_data(self):
        """Test case for get_score_revision_data

        Get a score revision data  # noqa: E501
        """
        pass

    def test_get_score_revisions(self):
        """Test case for get_score_revisions

        List the revisions  # noqa: E501
        """
        pass

    def test_get_score_submissions(self):
        """Test case for get_score_submissions

        List submissions related to the score  # noqa: E501
        """
        pass

    def test_get_score_track(self):
        """Test case for get_score_track

        Retrieve the details of an audio or video track linked to a score  # noqa: E501
        """
        pass

    def test_get_user_scores(self):
        """Test case for get_user_scores

        List user's scores  # noqa: E501
        """
        pass

    def test_list_score_tracks(self):
        """Test case for list_score_tracks

        List the audio or video tracks linked to a score  # noqa: E501
        """
        pass

    def test_mark_score_comment_resolved(self):
        """Test case for mark_score_comment_resolved

        Mark the comment as resolved  # noqa: E501
        """
        pass

    def test_mark_score_comment_unresolved(self):
        """Test case for mark_score_comment_unresolved

        Mark the comment as unresolved  # noqa: E501
        """
        pass

    def test_post_score_comment(self):
        """Test case for post_score_comment

        Post a new comment  # noqa: E501
        """
        pass

    def test_remove_score_collaborator(self):
        """Test case for remove_score_collaborator

        Delete a collaborator  # noqa: E501
        """
        pass

    def test_untrash_score(self):
        """Test case for untrash_score

        Untrash a score  # noqa: E501
        """
        pass

    def test_update_score_comment(self):
        """Test case for update_score_comment

        Update an existing comment  # noqa: E501
        """
        pass

    def test_update_score_track(self):
        """Test case for update_score_track

        Update an audio or video track linked to a score  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
