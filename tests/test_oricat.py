# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch #, call
import unittest.mock
import unittest
# from oricat import categorise
from oricat import cli

class TestOricat(unittest.TestCase):

    # @patch('time.sleep')
    # @patch('boto3.client')
    # @patch('oricat.load')
    # @patch('oricat.init')
    # def test_apply( # pylint: disable=too-many-arguments
    #         self,
    #         func_init,
    #         func_load,
    #         func_client,
    #         func_sleep):

    #     mock_logger = unittest.mock.Mock()
    #     mock_client = unittest.mock.Mock()
    #     mock_tagset = unittest.mock.Mock()
    #     mock_resource = unittest.mock.Mock()
    #     mock_tagset_tag = unittest.mock.Mock()
    #     mock_resource_tag = unittest.mock.Mock()

    #     func_init.return_value = mock_logger
    #     func_client.return_value = mock_client
    #     func_load.return_value = (
    #         { 'sometagsetname': mock_tagset },
    #         [mock_resource]
    #     )

    #     mock_resource.get_arn.return_value = 'somearn'
    #     mock_resource_tag.get_key.return_value = 'someresourcekey'
    #     mock_resource_tag.get_value.return_value = 'someresourcevalue'
    #     mock_tagset_tag.get_key.return_value = 'sometagkey'
    #     mock_tagset_tag.get_value.return_value = 'sometagvalue'
    #     mock_resource.get_tagset_names.return_value = ['sometagsetname']
    #     mock_tagset.get_tags.return_value = [mock_tagset_tag]
    #     mock_resource.get_tags.return_value = [mock_resource_tag]
    #     mock_client.tag_resources.return_value = {}

    #     apply(conf_file='oricat.yaml', dry_run=False, batch_size=5, delay=3)

    #     self.assertEqual(mock_logger.info.call_count, 3)
    #     mock_logger.info.assert_has_calls([
    #         call('Loading configuration file oricat.yaml'),
    #         call('Adding resource somearn to a batch with tags ' \
    #             "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
    #         call("Applying 1 resource(s) with tags "\
    #              "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}")
    #     ])
    #     # should call tag_resources once as part of remaining batches
    #     mock_client.tag_resources.assert_called_once_with(
    #         ResourceARNList=['somearn'],
    #         Tags={'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}
    #     )
    #     func_sleep.assert_called_once_with(3)

    @patch('oricat.categorise')
    def test_cli( # pylint: disable=too-many-arguments
            self,
            func_categorise):

        func_categorise.return_value = None

        cli('someinputdir', 'someoutputdir')

        # should delegate call to apply
        func_categorise.assert_called_once_with('someinputdir', 'someoutputdir')
