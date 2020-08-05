from django.shortcuts import render, redirect
import onetimepad


class Affine(object):
    DIE = 128
    KEY = (7, 3, 55)

    def __init__(self):
        pass

    def encryptChar(self, char):
        K1, K2, kI = self.KEY
        return chr((K1 * ord(char) + K2) % self.DIE)

    def encrypt(self, string):
        return "".join(map(self.encryptChar, string))

    def decryptChar(self, char):
        K1, K2, KI = self.KEY
        return chr(KI * (ord(char) - K2) % self.DIE)

    def decrypt(self, string):
        return "".join(map(self.decryptChar, string))
        affine = Affine()


def index(request):
    data = dict()
    affine = Affine()

    if request.method == 'POST':
        procedure = request.POST.get('procedure', None)
        method = request.POST.get('method', None)
        text = request.POST.get('message', None)
        if procedure and method and text:
            if procedure.lower() == 'encrypt'.lower():
                if method.lower() == 'affine'.lower():
                    result = affine.encrypt(text)
                elif method.lower() == 'onetime'.lower():
                    result = onetimepad.encrypt(text, 'random')
            elif procedure.lower() == 'decrypt'.lower():
                if method.lower() == 'affine'.lower():
                    result = affine.decrypt(text)
                elif method.lower() == 'onetime'.lower():
                    result = onetimepad.decrypt(text, 'random')
            data.update({'result': result})
        else:
            data.update({'error': 'Please fill all the details!!'})
        return render(request, 'index.html', data)
    else:
        return render(request, 'index.html', data)

