import pytest

from mamba_client.testing.utils import CallbackTestClass
from mamba_client.flow.operator.lifecycle import OperatorLifecycle

from mamba_client.station import Station
from mamba_client.flow.exceptions import MambaFlowException
from mamba_client.flow.operator import CyclicPythonOperator


class TestClass:
    def test_python_operator(self):
        cb = CallbackTestClass()

        operator = CyclicPythonOperator(
            operator_id='op_1',
            schedule=0,
            cycle=1,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert operator.ready(0, {})
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert cb.func_1_calls == []

        operator.execute(0)

        assert cb.func_1_calls == [0]
        assert operator._lifecycle == OperatorLifecycle.running
        assert operator.ready(0, {})

        assert operator.ready(1, {})

        operator.execute(1)

        assert cb.func_1_calls == [0, 1]
        assert operator._lifecycle == OperatorLifecycle.running
        assert operator.ready(2, {})

        operator = CyclicPythonOperator(operator_id='op_1',
                                        schedule=0,
                                        cycle=1,
                                        op_args='asd',
                                        python_callable=lambda it, st, cxt,
                                        args: cb.test_func_1(f'{it} - {args}'))

        assert cb.func_1_calls == [0, 1]
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert operator.ready(2, {})

        operator.execute(2)

        assert cb.func_1_calls == [0, 1, '2 - asd']
        assert operator._lifecycle == OperatorLifecycle.running
        assert operator.ready(3, {})

        station = Station(station_id='station_1')

        operator = CyclicPythonOperator(
            operator_id='op_1',
            schedule=0,
            cycle=1,
            op_args='asd',
            station=station,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(station))

        assert cb.func_1_calls == [0, 1, '2 - asd']
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert operator.ready(3, {})

        operator.execute(2)

        assert cb.func_1_calls == [0, 1, '2 - asd', station]
        assert operator._lifecycle == OperatorLifecycle.running
        assert operator.ready(4, {})

        operator = CyclicPythonOperator(
            operator_id='op_1',
            schedule=0,
            cycle=1,
            op_args='asd',
            station=station,
            context={'a': 'b'},
            python_callable=lambda it, st, cxt, args: cb.test_func_1(cxt))

        assert cb.func_1_calls == [0, 1, '2 - asd', station]
        assert operator._lifecycle == OperatorLifecycle.no_status
        assert operator.ready(4, {})

        operator.execute(4)

        assert cb.func_1_calls == [0, 1, '2 - asd', station, {'a': 'b'}]
        assert operator._lifecycle == OperatorLifecycle.running
        assert operator.ready(5, {})

        operator = CyclicPythonOperator(
            operator_id='op_1',
            schedule=2,
            cycle=2,
            schedule_end=10,
            python_callable=lambda it, st, cxt, args: cb.test_func_1(it))

        assert not operator.ready(0, {})
        assert not operator.ready(1, {})
        assert operator.ready(2, {})
        assert not operator.ready(3, {})
        assert operator.ready(4, {})
        assert operator.ready(10, {})
        assert not operator.ready(11, {})
        assert not operator.ready(12, {})

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule=0,
                                 cycle=1,
                                 python_callable='text')

        assert str(excinfo.value) == '"python_callable" param must be callable'

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule='0',
                                 cycle=1,
                                 python_callable='text')

        assert str(excinfo.value
                   ) == 'Operator op_1 schedule must be a positive integer'

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule=-1,
                                 cycle=1,
                                 python_callable='text')

        assert str(excinfo.value
                   ) == 'Operator op_1 schedule must be a positive integer'

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule=0,
                                 cycle='1',
                                 python_callable='text')

        assert str(
            excinfo.value) == 'Operator op_1 cycle must be a positive integer'

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule=0,
                                 cycle=-1,
                                 python_callable='text')

        assert str(
            excinfo.value) == 'Operator op_1 cycle must be a positive integer'

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule=0,
                                 cycle=1,
                                 schedule_end='2',
                                 python_callable='text')

        assert str(
            excinfo.value
        ) == 'Operator op_1 schedule_end must be a positive integer or None'

        with pytest.raises(MambaFlowException) as excinfo:
            CyclicPythonOperator(operator_id='op_1',
                                 schedule=0,
                                 cycle=1,
                                 schedule_end=-1,
                                 python_callable='text')

        assert str(
            excinfo.value
        ) == 'Operator op_1 schedule_end must be a positive integer or None'
