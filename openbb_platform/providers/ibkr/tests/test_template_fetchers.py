"""Template Fetchers tests."""

from datetime import datetime

import pytest
from openbb_core.app.service.user_service import UserService

#from openbb_template.models.template import (
#    TemplateFetcher,
#)


test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [
            ("User-Agent", None),
            ("api_key", "MOCK_API_KEY"),
            ("x-api-token", "MOCK_API_KEY"),
        ],
        "filter_query_parameters": [
            ("api_key", "MOCK_API_KEY"),
            ("x-api-token", "MOCK_API_KEY"),
        ],
    }



#@pytest.mark.record_http
#def test_mock_fetcher(credentials=test_credentials):
#    params = {
#        "start_date": datetime.date(2023, 11, 3),
#        "end_date": datetime.date(2023, 11, 3),
#    }

#    fetcher = TemplateFetcher()
#    result = fetcher.test(params, credentials)
#    assert result is None
