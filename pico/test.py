from talker import Talker

# create a Talker instance with default settings
talker = Talker()

# send a command to the device and expect a response
command = 'hello'
talker.send(command)
print('Device response: {}'.format(command))

# send another command and expect a response
command = 'world'
talker.send(command)
print('Device response: {}'.format(command))

# close the serial connection
talker.close()
