#-*-coding:utf-8-*-

def test(data, bot=None):
    message = data['message']
    return message.startswith('echo')


def handle(data, bot, kv, app):
    return data['message']


if __name__ == '__main__':
    print test({'message': '123'})
    print test({'message': 'echo rz'})
    print handle({'message': '123'}, None, None, None)
    print handle({'message': 'echo rz'}, None, None, None)
