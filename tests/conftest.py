import json

import pytest
import yaml

from src.db_utils import DBUtils
from src.image_processing import ImageProcessing


processed_image_results = []


@pytest.fixture()
def load_config():
    with open('../config/config.yaml', 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope='class')
def process_image(request):
    return ImageProcessing().get_spot_data(request.param)


@pytest.fixture(autouse=True, scope='class')
def save_to_json(process_image):
    yield
    processed_image_results.append(process_image)
    with open('../config/output.json', 'w+') as file:
        json.dump(processed_image_results, file, indent=2)


@pytest.fixture(scope='session', autouse=True)
def connect_to_db():
    DBUtils().connect()
    yield
    DBUtils().disconnect()


@pytest.fixture(scope='class', autouse=True)
def upload_to_db(process_image):
    yield
    DBUtils().update_results_table(process_image)



