from . import *


class TestSSH(TestCase):

    def setUp(self):

        self.account_name = 'test_' + mini_timestamp()
        shell('''
            echo Creating account: %(account_name)s
            git-base-account --delete 'test_*'
            git-base-account -k var/ssh/id_rsa.pub %(account_name)s
            git-base-keys --rewrite var/ssh/authorized_keys
        ''' % self.__dict__)

    def tearDown(self):
        shell('''
            echo Cleaning up test accounts...
            git-base-account --delete 'test_*'
        ''' % self.__dict__)

    def test_echo(self):
        self.assertEqual(
            shell_output('''
                ssh -p 2222 localhost echo hello
            ''').strip(),
            'echo hello'
        )

    def test_passwd(self):

        shell('''
            ssh -p 2222 localhost passwd password
        ''')

        with app.test_request_context():

            account = Account.query.filter_by(name=self.account_name).first()
            self.assertTrue(account.check_password('password'))




