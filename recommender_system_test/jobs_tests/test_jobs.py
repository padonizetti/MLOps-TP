from movies_rs_dagster import defs
from dagster import ExecuteInProcessResult


def test_data_job():
    get_data_job = defs.get_job_def('get_data')
    result = get_data_job.execute_in_process()
    assert isinstance(result, ExecuteInProcessResult)
    assert result.success
    assert len(result.output_for_node('training_data')) > 10
