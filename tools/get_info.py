from getpass import getpass

def get_info(prompt=''):
  username = input (prompt)
  password = None
  while not password:
    password = getpass()
    password_verify = getpass('Verify the password again:')
    if password != password_verify:
      print ('Passwords do no matach. Try again:')
      password = None
  return username, password
