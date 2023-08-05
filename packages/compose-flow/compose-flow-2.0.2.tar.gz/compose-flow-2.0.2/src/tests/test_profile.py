from unittest import TestCase, mock

from compose_flow.commands.subcommands.profile import Profile


class ProfileTestCase(TestCase):
    def test_expand_services(self, *mocks):
        workflow = mock.Mock()

        data = {
            'services': {
                'foo': {
                    'build': '..',
                    'image': '${DOCKER_IMAGE}',
                    'environment': [
                        'FOO=1',
                        'SPARK_WORKER_PORT=8888',
                        'SPARK_WORKER_WEBUI_PORT=8080',
                    ],
                    'ports': [
                        '8000:8000',
                    ],
                    'deploy': {
                        'replicas': 3,
                    },
                },
            },

            'compose_flow': {
                'expand': {
                    'foo': {
                        'increment': {
                            'env': [
                                'SPARK_WORKER_PORT',
                                'SPARK_WORKER_WEBUI_PORT',
                            ],
                            'ports': {
                                'source_port': True,
                                'destination_port': True,
                            },
                        },
                    },
                },
            },
        }

        profile = Profile(workflow)
        new_data = profile._check_cf_config(data)

        self.assertEqual(len(new_data['services']), 3)

        self.assertEqual(sorted(new_data['services'].keys()), ['foo1', 'foo2', 'foo3'])

        self.assertEqual(
            [x['ports'] for x in new_data['services'].values()],
            [['8000:8000'], ['8001:8001'], ['8002:8002']]
        )

        self.assertEqual(
            [x['environment'] for x in new_data['services'].values()],
            [
                ['FOO=1', 'SPARK_WORKER_PORT=8888', 'SPARK_WORKER_WEBUI_PORT=8080'],
                ['FOO=1', 'SPARK_WORKER_PORT=8889', 'SPARK_WORKER_WEBUI_PORT=8081'],
                ['FOO=1', 'SPARK_WORKER_PORT=8890', 'SPARK_WORKER_WEBUI_PORT=8082'],
            ]
        )
