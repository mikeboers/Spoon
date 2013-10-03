from . import *


class SSHTestCase(TestCase):

    def setUp(self):

        self.account_name = 'test_' + mini_start + '_' + self.__class__.__name__
        self.log.info('creating account %s' % self.account_name)
        self.key = self.genkey()
        shell('''
            git-base-account -k {self.key}.pub {self.account_name}
            git-base-keys --rewrite var/ssh/authorized_keys
        '''.format(self=self))

    def tearDown(self):
        if CLEAN_DB:
            self.log.info('cleaning up account')
            shell('''
                git-base-account --delete 'test_*_{self.__class__.__name__}'
            '''.format(self=self))

    def shell(self, source, **kwargs):
        return shell(source, key=self.key, **kwargs)

    def shell_output(self, source, **kwargs):
        return shell_output(source, key=self.key, **kwargs)


class TestSSHEcho(SSHTestCase):

    def test(self):
        self.assertEqual(
            self.shell_output('''
                ssh -p 2222 localhost echo hello
            ''').strip(),
            'I got: hello'
        )


class TestSSHPasswd(SSHTestCase):

    def test(self):

        self.shell('''
            ssh -p 2222 localhost passwd password
        ''')

        with app.test_request_context():

            account = Account.query.filter_by(name=self.account_name).first()
            self.assertTrue(account.check_password('password'))


class TestSSHAutoCreate(SSHTestCase):

    def test(self):

        self.assertFalse(self.shell('''

            cd "{self.sandbox}"
            mkdir hello
            cd hello
            git init
            echo "Hello, world!" > README.txt
            git add README.txt
            git commit -m 'Greet the world.'
            git remote add origin ssh://localhost:2222/{self.account_name}/hello
            git push origin

        '''.format(self=self)))

        with app.test_request_context():

            account = Account.query.filter_by(name=self.account_name).first()
            self.assertEqual(account.repos[0].name, 'hello')




