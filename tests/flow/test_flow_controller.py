import pytest

from mamba_client.testing.utils import CallbackTestClass
from mamba_client.flow.exceptions import MambaFlowException
from mamba_client.flow.operator import PythonOperator, CyclicPythonOperator
from mamba_client.flow.flow_controller import FlowController


class TestClass:
    def test_flow_controller(self):
        cb = CallbackTestClass()

        ctrl = FlowController(10)
        assert ctrl._iterations == 10
        assert ctrl._operator_list == []
        assert ctrl._operator_lifecycle == {}
        assert ctrl._operator_downstream == {}
        assert ctrl._log is None

        ctrl.add(
            PythonOperator(operator_id='op_1',
                           schedule=0,
                           python_callable=lambda it, st, cxt, args: cb.
                           test_func_1(f'{it} - op_1')))

        ctrl.add(
            PythonOperator(operator_id='op_2',
                           schedule=9,
                           python_callable=lambda it, st, cxt, args: cb.
                           test_func_1(f'{it} - op_2')))

        ctrl.add(
            CyclicPythonOperator(operator_id='op_3',
                                 schedule=1,
                                 cycle=2,
                                 python_callable=lambda it, st, cxt, args: cb.
                                 test_func_1(f'{it} - op_3')))

        ctrl.add(
            CyclicPythonOperator(operator_id='op_4',
                                 schedule=0,
                                 cycle=1,
                                 schedule_end=5,
                                 python_callable=lambda it, st, cxt, args: cb.
                                 test_func_1(f'{it} - op_4')))

        ctrl.execute()

        # assert operator.ready(0, {})
        # assert operator._lifecycle == OperatorLifecycle.no_status
        assert cb.func_1_calls == [
            '0 - op_1', '0 - op_4', '1 - op_3', '1 - op_4', '2 - op_4',
            '3 - op_3', '3 - op_4', '4 - op_4', '5 - op_3', '5 - op_4',
            '7 - op_3', '9 - op_2', '9 - op_3'
        ]
        with pytest.raises(MambaFlowException) as excinfo:
            ctrl.add(
                PythonOperator(operator_id='op_2',
                               schedule=9,
                               python_callable=lambda it, st, cxt, args: cb.
                               test_func_1(f'{it} - op_2')))

        assert str(excinfo.value) == 'Operator op_2 is already defined'

        with pytest.raises(MambaFlowException) as excinfo:
            ctrl.add(
                PythonOperator(operator_id='op_7',
                               schedule=10,
                               python_callable=lambda it, st, cxt, args: cb.
                               test_func_1(f'{it} - op_3')))

        assert str(
            excinfo.value
        ) == 'Operator op_7 schedule is greater than number of iterations: [0-9]'

        with pytest.raises(MambaFlowException) as excinfo:
            FlowController('10')

        assert str(excinfo.value
                   ) == 'FlowController iterations must be a positive integer'

        with pytest.raises(MambaFlowException) as excinfo:
            FlowController(-1)

        assert str(excinfo.value
                   ) == 'FlowController iterations must be a positive integer'

        ctrl = FlowController(1, log=lambda _: cb.test_func_2(_))

        ctrl.add(
            PythonOperator(operator_id='op_1',
                           schedule=0,
                           python_callable=lambda it, st, cxt, args: cb.
                           test_func_1(f'{it} - op_1')))

        ctrl.execute()

        assert cb.func_2_calls == [
            'Start Execution Flow', 'Start iteration 0', 'Stop Execution Flow'
        ]

        with pytest.raises(MambaFlowException) as excinfo:
            FlowController(1, log='')

        assert str(
            excinfo.value) == 'FlowController log param must be callable'
