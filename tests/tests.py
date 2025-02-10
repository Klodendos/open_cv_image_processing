import pytest


class TestSuite:
    img_list = ['../config/source.png', '../config/source2.png', '../config/source3.png']

    @pytest.mark.parametrize('process_image', img_list, indirect=True)
    def test_spot_position(self, load_config, process_image):
        expected_spot_position = load_config['position']
        actual_spot_position = process_image['center_position']
        assert actual_spot_position == expected_spot_position, 'Spot position is not equal to expected'

    @pytest.mark.parametrize('process_image', img_list, indirect=True)
    def test_spot_dispersion(self, load_config, process_image):
        expected_dispersion = load_config['dispersion']
        actual_dispersion = float(process_image['dispersion'])
        assert actual_dispersion <= expected_dispersion, 'Actual dispersion is more than expected'

    @pytest.mark.parametrize('process_image', img_list, indirect=True)
    def test_spot_deviation(self, load_config, process_image):
        expected_deviation = load_config['std']
        actual_deviation = float(process_image['deviation'])
        assert actual_deviation <= expected_deviation, 'Actual deviation is more than expected'
