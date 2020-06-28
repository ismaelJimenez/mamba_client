import pytest

from mamba_client.testing.utils import CallbackTestClass
from mamba_client.flow.operator.lifecycle import OperatorLifecycle

from mamba_client.station import Station
from mamba_client.flow.exceptions import MambaFlowException
from mamba_client.flow.operator import PythonOperator


class TestClass:
    def test_python_operator(self):
        cb = CallbackTestClass()

        operator = PythonOperator(
            operator_id='op_1',
            schedule=0,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert operator.ready(0, {})
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert cb.func_1_calls == []

        operator.execute(0)

        assert cb.func_1_calls == [0]
        assert operator._lifecycle == OperatorLifecycle.success
        assert not operator.ready(0, {})

        operator = PythonOperator(
            operator_id='op_1',
            schedule=0,
            op_args='asd',
            python_callable=lambda it, st, cxt, args: cb.test_func_1(args))

        assert operator.ready(0, {})
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert cb.func_1_calls == [0]

        operator.execute(0)

        assert cb.func_1_calls == [0, 'asd']
        assert operator._lifecycle == OperatorLifecycle.success
        assert not operator.ready(0, {})

        station = Station(station_id='station_1')

        operator = PythonOperator(
            operator_id='op_1',
            schedule=0,
            op_args='asd',
            station=station,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(st))

        assert operator.ready(0, {})
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert cb.func_1_calls == [0, 'asd']

        operator.execute(0)

        assert cb.func_1_calls == [0, 'asd', station]
        assert operator._lifecycle == OperatorLifecycle.success
        assert not operator.ready(0, {})

        operator = PythonOperator(
            operator_id='op_1',
            schedule=0,
            op_args='asd',
            station=station,
            context={'a': 'b'},
            python_callable=lambda it, st, cxt, args: cb.test_func_1(cxt))

        assert operator.ready(0, {})
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert cb.func_1_calls == [0, 'asd', station]

        operator.execute(0)

        assert cb.func_1_calls == [0, 'asd', station, {'a': 'b'}]
        assert operator._lifecycle == OperatorLifecycle.success
        assert not operator.ready(0, {})

        operator = PythonOperator(
            operator_id='op_1',
            schedule=4,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert not operator.ready(0, {})
        assert operator.ready(4, {})
        assert operator.ready(5, {})

        operator = PythonOperator(
            operator_id='op_1',
            upstream='op_0',
            python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert not operator.ready(0, {})
        assert operator.ready(0, {'op_0': OperatorLifecycle.success})

        with pytest.raises(MambaFlowException) as excinfo:
            PythonOperator(
                operator_id='op_1',
                schedule=0,
                upstream='op_0',
                python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert str(excinfo.value
                   ) == 'Operator op_1 can not have schedule and upstream'

        with pytest.raises(MambaFlowException) as excinfo:
            PythonOperator(
                operator_id='op_1',
                python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert str(
            excinfo.value) == 'Operator op_1 must have schedule or upstream'

        with pytest.raises(MambaFlowException) as excinfo:
            PythonOperator(operator_id='op_1',
                           schedule=0,
                           python_callable='text')

        assert str(excinfo.value
                   ) == 'Operator op_1 python_callable param must be callable'

        with pytest.raises(MambaFlowException) as excinfo:
            PythonOperator(
                operator_id='op_1',
                schedule='0',
                python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert str(excinfo.value
                   ) == 'Operator op_1 schedule must be a positive integer'

        with pytest.raises(MambaFlowException) as excinfo:
            PythonOperator(
                operator_id='op_1',
                schedule=-1,
                python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert str(excinfo.value
                   ) == 'Operator op_1 schedule must be a positive integer'

        operator = PythonOperator(
            operator_id='op_1',
            schedule=0,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(it),
            log=lambda _: cb.test_func_2(_))

        operator.execute(0)

        assert len(cb.func_2_calls) == 2
        assert '[op_1] Start Operator Execution' in cb.func_2_calls[0]
        assert '[op_1] Stop Operator Execution' in cb.func_2_calls[1]

        with pytest.raises(MambaFlowException) as excinfo:
            PythonOperator(
                operator_id='op_1',
                schedule=0,
                python_callable=lambda it, st, cxt, args: cb.test_func_1(it),
                log='')

        assert str(excinfo.value) == 'Operator op_1 log param must be callable'
