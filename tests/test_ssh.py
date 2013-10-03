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
        pass

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

    def test_autocreate(self):

        shell('''

            cd "{self.sandbox}"
            mkdir hello
            cd hello
            git init
            echo "Hello, world!" > README.txt
            git add README.txt
            git commit -m 'Greet the world.'
            git remote add origin ssh://localhost:2222/{self.account_name}/hello
            git push origin

        '''.format(self=self))




