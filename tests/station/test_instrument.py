import pytest

from mamba_client.station import NetworkController, Instrument
from mamba_client.mock.mamba_server_mock import MambaServerMock
from mamba_client.station.exceptions import ParameterSetException


class TestClass:
    def test_parameter_init(self):
        MambaServerMock(port=34574)
        network_controller = NetworkController(port=34574)

        inst = Instrument(instrument_id='inst_1',
                          network_controller=network_controller)

        assert inst._id == 'inst_1'
        assert inst._network_controller is not None
        assert inst._parameters == {}

        inst.add_parameter(parameter_id='test_1')

        assert list(inst._parameters.keys()) == ['test_1']
        assert inst.test_1._parameter_id == 'test_1'
        assert inst.test_1._get is not None
        assert inst.test_1._get._parameter_id == 'inst_1_test_1'
        assert inst.test_1._set is not None
        assert inst.test_1._set._parameter_id == 'inst_1_test_1'

        inst.add_parameter(parameter_id='test_2',
                           get_alias='test_2_get',
                           set_alias='test_2_set')

        assert list(inst._parameters.keys()) == ['test_1', 'test_2']
        assert inst.test_2._parameter_id == 'test_2'
        assert inst.test_2._get is not None
        assert inst.test_2._get._parameter_id == 'test_2_get'
        assert inst.test_2._set is not None
        assert inst.test_2._set._parameter_id == 'test_2_set'

        inst.add_parameter(parameter_id='test_3', set_arg_1=1)

        assert list(inst._parameters.keys()) == ['test_1', 'test_2', 'test_3']
        assert inst.test_3._parameter_id == 'test_3'
        assert inst.test_3._get is not None
        assert inst.test_3._get._parameter_id == 'inst_1_test_3'
        assert inst.test_3._set is not None
        assert inst.test_3._set._parameter_id == 'inst_1_test_3'
        assert inst.test_3._set._arg_1 == 1
        assert inst.test_3._set._arg_2 is None

        with pytest.raises(KeyError) as excinfo:
            inst.add_parameter(parameter_id='test_3')

        assert str(excinfo.value) == "'Duplicate parameter name test_3'"

        inst.add_get_parameter(parameter_id='test_4')

        assert list(inst._parameters.keys()) == [
            'test_1', 'test_2', 'test_3', 'test_4'
        ]
        assert inst.test_4._parameter_id == 'test_4'
        assert inst.test_4._get is not None
        assert inst.test_4._get._parameter_id == 'inst_1_test_4'
        assert inst.test_4._set is None

        inst.add_get_parameter(parameter_id='test_5', get_alias='test_5_get')

        assert list(inst._parameters.keys()) == [
            'test_1', 'test_2', 'test_3', 'test_4', 'test_5'
        ]
        assert inst.test_5._parameter_id == 'test_5'
        assert inst.test_5._get is not None
        assert inst.test_5._get._parameter_id == 'test_5_get'
        assert inst.test_5._set is None

        inst.add_set_parameter(parameter_id='test_6')

        assert list(inst._parameters.keys()) == [
            'test_1', 'test_2', 'test_3', 'test_4', 'test_5', 'test_6'
        ]
        assert inst.test_6._parameter_id == 'test_6'
        assert inst.test_6._set is not None
        assert inst.test_6._set._parameter_id == 'inst_1_test_6'
        assert inst.test_6._get is None

        inst.add_set_parameter(parameter_id='test_7',
                               set_alias='test_7_set',
                               set_arg_1=2)

        assert list(inst._parameters.keys()) == [
            'test_1', 'test_2', 'test_3', 'test_4', 'test_5', 'test_6',
            'test_7'
        ]
        assert inst.test_7._parameter_id == 'test_7'
        assert inst.test_7._set is not None
        assert inst.test_7._set._parameter_id == 'test_7_set'
        assert inst.test_7._get is None
        assert inst.test_7._set._arg_1 == 2
        assert inst.test_7._set._arg_2 is None

        network_controller.close()

    def test_parameter_call(self):
        mock = MambaServerMock(port=34575)
        network_controller = NetworkController(port=34575)

        inst = Instrument(instrument_id='inst_1',
                          network_controller=network_controller)

        inst.add_parameter(parameter_id='test_1')

        assert mock._shared_memory['last_tc'] == 'tc_meta inst_1_test_1'
        assert mock._shared_memory[
            'last_tm'] == '> OK inst_1_test_1;1;test description'

        reply = inst.test_1.get()

        assert mock._shared_memory['last_tc'] == 'tm inst_1_test_1'
        assert '> OK inst_1_test_1;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        inst.test_1.set(1)

        assert mock._shared_memory['last_tc'] == 'tc inst_1_test_1 "1"'
        assert mock._shared_memory['last_tm'] == '> OK inst_1_test_1'

        with pytest.raises(ParameterSetException) as excinfo:
            inst.test_1.set(1, 2)

        assert str(
            excinfo.value
        ) == 'inst_1_test_1 set - Wrong number of arguments. Expected: 1, Received: 2.'

        inst.add_parameter(parameter_id='test_2', set_arg_1=1)

        reply = inst.test_2.get()

        assert mock._shared_memory['last_tc'] == 'tm inst_1_test_2'
        assert '> OK inst_1_test_2;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        inst.test_2.set()

        assert mock._shared_memory['last_tc'] == 'tc inst_1_test_2 "1"'
        assert mock._shared_memory['last_tm'] == '> OK inst_1_test_2'

        inst.test_2.set(2)

        assert mock._shared_memory['last_tc'] == 'tc inst_1_test_2 "2"'
        assert mock._shared_memory['last_tm'] == '> OK inst_1_test_2'

        network_controller.close()
