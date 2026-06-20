import unittest

from unittest.mock import MagicMock, patch

import json

class TestVisitorCounter(unittest.TestCase):

  @patch.dict('os.environ', {'COSMOS_CONNECTION_STRING': 'fake_connection_string'})
    @patch('function_app.TableServiceClient')
  def test_existing_count_increments(self, mock_table_service):
    mock_table_client = MagicMock()
    mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table_client
    
    mock_table_client.get_entity.return_value = {
       "PartitionKey": "counter",
      "rowKey": "visits",
      "Count": 5
   }  

    import function_app
    req = MagicMock()
    response = function_app.visitor_counter(req)
    result = json.loads(response.get_body())

    self.assertEqual(result["count"], 6)


 @patch.dict('os.environ', {'COSMOS_CONNECTION_STRING': 'fake_connection_string'})
    @patch('function_app.TableServiceClient')
def test_new_count_starts_at_one(self, mock_table_service):

  mock_table_client = MagicMock()
  mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table_client

  mock_table_client.get_entity.side_effect = Exception("Not Found")

  import function_app
  req = MagicMock()
  response = function_app.visitor_counter(req)
  result = json.loads(response.get_body())

  self.assertEqual(result["count"], 1)

if __name__ == '__main__':
    unittest.main()

