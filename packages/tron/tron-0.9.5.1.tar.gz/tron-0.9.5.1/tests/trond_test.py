from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import textwrap
from subprocess import CalledProcessError
from textwrap import dedent

import pytest

from testifycompat import assert_equal
from testifycompat import assert_gt
from tests import sandbox
from tron.core import actionrun

BASIC_CONFIG = """
ssh_options:
    agent: true

nodes:
  - name: local
    hostname: 'localhost'

state_persistence:
    name: "state_data.shelve"
    store_type: shelve

"""

SINGLE_ECHO_CONFIG = BASIC_CONFIG + """
jobs:
  - name: "echo_job"
    node: local
    schedule: "interval 1 hour"
    actions:
      - name: "echo_action"
        command: "echo 'Echo!'" """

DOUBLE_ECHO_CONFIG = SINGLE_ECHO_CONFIG + """
      - name: "another_echo_action"
        command: "echo 'Today is %(shortdate)s, which is the same
                    as %(year)s-%(month)s-%(day)s' && false" """

ALT_NAMESPACED_ECHO_CONFIG = """
jobs:
  - name: "echo_job"
    node: local
    schedule: "interval 1 hour"
    actions:
      - name: "echo_action"
        command: "echo 'Echo!'" """

TOUCH_CLEANUP_FMT = """
    cleanup_action:
      command: "echo 'at last'"
"""


@pytest.mark.skip(reason="We don't have a setup for sandbox tests yet")
class TrondEndToEndTestCase(sandbox.SandboxTestCase):
    def test_end_to_end_basic(self):
        self.start_with_config(SINGLE_ECHO_CONFIG)
        client = self.sandbox.client

        assert_equal(
            self.client.config('MASTER')['config'],
            SINGLE_ECHO_CONFIG,
        )

        # reconfigure and confirm results
        second_config = DOUBLE_ECHO_CONFIG + TOUCH_CLEANUP_FMT
        self.sandbox.tronfig(second_config)
        assert_equal(client.config('MASTER')['config'], second_config)

        # reconfigure, by uploading a third configuration
        self.sandbox.tronfig(ALT_NAMESPACED_ECHO_CONFIG, name='ohce')
        self.sandbox.client.home()

        # run the job and check its output
        echo_job_name = 'MASTER.echo_job'
        job_url = client.get_url(echo_job_name)
        action_url = client.get_url('MASTER.echo_job.1.echo_action')

        self.sandbox.tronctl('start', echo_job_name)

        def wait_on_cleanup():
            return (
                len(client.job(job_url)['runs']) >= 2 and
                client.action_runs(action_url)['state'] ==
                actionrun.ActionRun.STATE_SUCCEEDED.name
            )

        sandbox.wait_on_sandbox(wait_on_cleanup)

        echo_action_run = client.action_runs(action_url)
        another_action_url = client.get_url(
            'MASTER.echo_job.1.another_echo_action',
        )
        other_act_run = client.action_runs(another_action_url)
        assert_equal(
            echo_action_run['state'],
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )
        assert_equal(echo_action_run['stdout'], ['Echo!'])
        assert_equal(
            other_act_run['state'],
            actionrun.ActionRun.STATE_FAILED.name,
        )

        now = datetime.datetime.now()
        stdout = now.strftime(
            'Today is %Y-%m-%d, which is the same as %Y-%m-%d',
        )
        assert_equal(other_act_run['stdout'], [stdout])

        job_runs_url = client.get_url('%s.1' % echo_job_name)
        assert_equal(
            client.job_runs(job_runs_url)['state'],
            actionrun.ActionRun.STATE_FAILED.name,
        )

    def test_node_reconfig(self):
        job_config = dedent(
            """
            jobs:
                - name: a_job
                  node: local
                  schedule: "interval 1s"
                  actions:
                    - name: first_action
                      command: "echo something"
        """
        )
        second_config = dedent(
            """
            ssh_options:
                agent: true

            nodes:
              - name: local
                hostname: '127.0.0.1'

            state_persistence:
                name: "state_data.shelve"
                store_type: shelve

        """
        ) + job_config
        self.start_with_config(BASIC_CONFIG + job_config)

        job_url = self.client.get_url('MASTER.a_job.0')
        sandbox.wait_on_state(
            self.client.job_runs,
            job_url,
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )

        self.sandbox.tronfig(second_config)

        job_url = self.client.get_url('MASTER.a_job')

        def wait_on_next_run():
            last_run = self.client.job(job_url)['runs'][0]
            return last_run['node']['hostname'] == '127.0.0.1'

        sandbox.wait_on_sandbox(wait_on_next_run)


@pytest.mark.skip(reason="We don't have a setup for sandbox tests yet")
class TronCommandsTestCase(sandbox.SandboxTestCase):
    def test_tronview(self):
        self.start_with_config(SINGLE_ECHO_CONFIG)
        expected = """\nServices:\nNo Services\n\n\nJobs:
            Name       State       Scheduler           Last Success
            MASTER.echo_job   enabled     interval 1:00:00    None
            """

        def remove_line_space(s):
            return [l.replace(' ', '') for l in s.split('\n')]

        actual = self.sandbox.tronview()[0]
        assert_equal(remove_line_space(actual), remove_line_space(expected))

    def test_tronctl_with_job(self):
        self.start_with_config(SINGLE_ECHO_CONFIG + TOUCH_CLEANUP_FMT)
        job_name = 'MASTER.echo_job'
        job_url = self.client.get_url(job_name)
        self.sandbox.tronctl('start', job_name)

        cleanup_url = self.client.get_url('MASTER.echo_job.1.cleanup')
        sandbox.wait_on_state(
            self.client.action_runs,
            cleanup_url,
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )

        action_run_url = self.client.get_url('MASTER.echo_job.1.echo_action')
        assert_equal(
            self.client.action_runs(action_run_url)['state'],
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )

        job_run_url = self.client.get_url('MASTER.echo_job.1')
        assert_equal(
            self.client.job_runs(job_run_url)['state'],
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )

        assert_equal(self.client.job(job_url)['status'], 'enabled')
        self.sandbox.tronctl('disable', job_name)
        sandbox.wait_on_state(self.client.job, job_url, 'disabled', 'status')

    def test_tronfig(self):
        self.start_with_config(SINGLE_ECHO_CONFIG)
        stdout, stderr = self.sandbox.tronfig()
        assert_equal(stdout.rstrip(), SINGLE_ECHO_CONFIG.rstrip())

    def test_tronfig_failure(self):
        self.start_with_config(SINGLE_ECHO_CONFIG)
        bad_config = 'this is not valid: yaml: is it?'

        def test_return_code(exc):
            assert_equal(exc.returncode, 1)

        with pytest.raises(CalledProcessError):
            test_return_code(self.sandbox.tronfig, bad_config)

    def test_tronfig_no_header(self):
        self.start_with_config(SINGLE_ECHO_CONFIG)
        namespace = 'second'
        self.sandbox.tronfig(ALT_NAMESPACED_ECHO_CONFIG, name=namespace)
        stdout, stderr = self.sandbox.tronfig(name=namespace, no_header=True)
        assert_equal(stdout.rstrip(), ALT_NAMESPACED_ECHO_CONFIG.rstrip())


@pytest.mark.skip(reason="We don't have a setup for sandbox tests yet")
class JobEndToEndTestCase(sandbox.SandboxTestCase):
    def test_cleanup_on_failure(self):
        config = BASIC_CONFIG + dedent(
            """
        jobs:
          - name: "failjob"
            node: local
            schedule: "constant"
            actions:
              - name: "failaction"
                command: "failplz"
        """
        ) + TOUCH_CLEANUP_FMT
        self.start_with_config(config)

        action_run_url = self.client.get_url('MASTER.failjob.0.failaction')
        sandbox.wait_on_state(
            self.client.action_runs,
            action_run_url,
            actionrun.ActionRun.STATE_FAILED.name,
        )

        action_run_url = self.client.get_url('MASTER.failjob.1.cleanup')
        sandbox.wait_on_state(
            self.client.action_runs,
            action_run_url,
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )
        job_runs = self.client.job(self.client.get_url('MASTER.failjob'),
                                   )['runs']
        assert_gt(len(job_runs), 1)

    def test_skip_failed_actions(self):
        config = BASIC_CONFIG + dedent(
            """
        jobs:
          - name: "multi_step_job"
            node: local
            schedule: "constant"
            actions:
              - name: "broken"
                command: "failingcommand"
              - name: "works"
                command: "echo ok"
                requires: [broken]
        """
        )
        self.start_with_config(config)
        action_run_url = self.client.get_url('MASTER.multi_step_job.0.broken')
        waiter = sandbox.build_waiter_func(
            self.client.action_runs,
            action_run_url,
        )

        waiter(actionrun.ActionRun.STATE_FAILED.name)
        self.sandbox.tronctl('skip', 'MASTER.multi_step_job.0.broken')
        waiter(actionrun.ActionRun.STATE_SKIPPED.name)

        action_run_url = self.client.get_url('MASTER.multi_step_job.0.works')
        sandbox.wait_on_state(
            self.client.action_runs,
            action_run_url,
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )

        job_run_url = self.client.get_url('MASTER.multi_step_job.0')
        sandbox.wait_on_state(
            self.client.job_runs,
            job_run_url,
            actionrun.ActionRun.STATE_SUCCEEDED.name,
        )

    def test_failure_on_multi_step_job_doesnt_wedge_tron(self):
        config = BASIC_CONFIG + dedent(
            """
            jobs:
                -   name: "random_failure_job"
                    node: local
                    queueing: true
                    schedule: "constant"
                    actions:
                        -   name: "fa"
                            command: "sleep 0.1; failplz"
                        -   name: "sa"
                            command: "echo 'you will never see this'"
                            requires: [fa]
        """
        )
        self.start_with_config(config)
        job_url = self.client.get_url('MASTER.random_failure_job')

        def wait_on_random_failure_job():
            return len(self.client.job(job_url)['runs']) >= 4

        sandbox.wait_on_sandbox(wait_on_random_failure_job)

        job_runs = self.client.job(job_url)['runs']
        expected = [actionrun.ActionRun.STATE_FAILED.name for _ in range(3)]
        assert_equal([run['state'] for run in job_runs[-3:]], expected)

    def test_cancel_schedules_a_new_run(self):
        config = BASIC_CONFIG + dedent(
            """
            jobs:
                -   name: "a_job"
                    node: local
                    schedule: "daily 05:00:00"
                    actions:
                        -   name: "first_action"
                            command: "echo OK"
        """
        )
        self.start_with_config(config)
        job_name = 'MASTER.a_job'
        job_url = self.client.get_url(job_name)

        self.sandbox.tronctl('cancel', '%s.0' % job_name)

        def wait_on_cancel():
            return len(self.client.job(job_url)['runs']) == 2

        sandbox.wait_on_sandbox(wait_on_cancel)

        run_states = [run['state'] for run in self.client.job(job_url)['runs']]
        expected = [
            actionrun.ActionRun.STATE_SCHEDULED.name,
            actionrun.ActionRun.STATE_CANCELLED.name,
        ]
        assert_equal(run_states, expected)

    def test_job_queueing_false_with_overlap(self):
        """Test that a job that has queueing false properly cancels an
        overlapping job run.
        """
        config = BASIC_CONFIG + dedent(
            """
            jobs:
                -   name: "cancel_overlap"
                    schedule: "interval 1s"
                    queueing: False
                    node: local
                    actions:
                        -   name: "do_something"
                            command: "sleep 3s"
                        -   name: "do_other"
                            command: "sleep 3s"
                    cleanup_action:
                        command: "echo done"
        """
        )
        self.start_with_config(config)
        job_url = self.client.get_url('MASTER.cancel_overlap')
        job_run_url = self.client.get_url('MASTER.cancel_overlap.1')

        def wait_on_job_schedule():
            return len(self.client.job(job_url)['runs']) == 2

        sandbox.wait_on_sandbox(wait_on_job_schedule)

        sandbox.wait_on_state(
            self.client.job,
            job_run_url,
            actionrun.ActionRun.STATE_CANCELLED.name,
        )

        action_run_states = [
            action_run['state']
            for action_run in self.client.job_runs(job_run_url)['runs']
        ]
        expected = [
            actionrun.ActionRun.STATE_CANCELLED.name
            for _ in range(len(action_run_states))
        ]
        assert_equal(action_run_states, expected)

    def test_trond_restart_job_with_run_history(self):
        config = BASIC_CONFIG + textwrap.dedent(
            """
           jobs:
              - name: fast_job
                node: local
                schedule: constant
                actions:
                  - name: single_act
                    command: "sleep 20 && echo good"
        """
        )
        self.start_with_config(config)

        action_run_url = self.client.get_url('MASTER.fast_job.0.single_act')
        sandbox.wait_on_state(
            self.client.action_runs,
            action_run_url,
            actionrun.ActionRun.STATE_RUNNING.name,
        )

        self.restart_trond()

        assert_equal(
            self.client.job_runs(action_run_url)['state'],
            actionrun.ActionRun.STATE_UNKNOWN.name,
        )

        next_run_url = self.client.get_url('MASTER.fast_job.-1.single_act')
        sandbox.wait_on_state(
            self.client.action_runs,
            next_run_url,
            actionrun.ActionRun.STATE_RUNNING.name,
        )

    def test_trond_restart_job_running_with_dependencies(self):
        config = BASIC_CONFIG + textwrap.dedent(
            """
            jobs:
                - name: complex_job
                  node: local
                  schedule: interval 10min
                  actions:
                    - name: first_act
                      command: sleep 20 && echo "I'm waiting"
                    - name: following_act
                      command: echo "thing"
                      requires: ['first_act']
                    - name: last_act
                      command: echo foo
                      requires: ['following_act']
        """
        )
        self.start_with_config(config)
        job_name = 'MASTER.complex_job'
        self.sandbox.tronctl('start', job_name)

        action_run_url = self.client.get_url('MASTER.complex_job.1.first_act')
        sandbox.wait_on_state(
            self.client.action_runs,
            action_run_url,
            actionrun.ActionRun.STATE_RUNNING.name,
        )

        self.restart_trond()

        assert_equal(
            self.client.job_runs(action_run_url)['state'],
            actionrun.ActionRun.STATE_UNKNOWN.name,
        )

        for followup_action_run in ('following_act', 'last_act'):
            url = self.client.get_url(
                '%s.1.%s' % (
                    job_name,
                    followup_action_run,
                )
            )
            assert_equal(
                self.client.action_runs(url)['state'],
                actionrun.ActionRun.STATE_QUEUED.name,
            )
