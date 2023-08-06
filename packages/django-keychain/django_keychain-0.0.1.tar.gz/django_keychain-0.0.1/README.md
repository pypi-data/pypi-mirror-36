# django_keychain

Django plugin that pulls secrets from AWS Secrets Manager.

**Usage**

Make sure you set up your AWS creadentials as you would for using `boto3`.

Usually, in your `settings.py`, point to the region you want to use.
Then, use `get_secret` function for simple values or nested secrets.

```
keychain = DjangoKeychain('eu-west-1')

SOMEVARIABLE = keychain.get_secret('TEST_SECRET')
SOMEOTHERVARIABLE = keychain.get_secret('TEST_SECRET_STORING_A_DICTIONARY', 'KEY')
