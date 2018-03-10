class Rot13():
    '''Usage:
    rot=Rot13()
    rot.encode(str)
    rot.decode(str)
    :returns a list with each element in str
    rot.decodes(str)
    rot.encodes(str)
    :returns a str'''

    def __init__(self):
        self.dic_en = {}
        for c in (65, 97):
            for i in range(26):
                self.dic_en[chr(i + c)] = chr((i + 13) % 26 + c)
        self.dic_dn = {}
        for key, value in self.dic_en.items():
            self.dic_dn[value] = key

    def __str__(self):
        return 'ROT13 Passcode'

    def __repr__(self):
        return 'ROT13 Passcode'

    def encode(self, string):
        self.l = []
        for each in string:
                if self.dic_en.get(each) == None:
                    self.l.append(each)
                else:
                    self.l.append(self.dic_en.get(each))
        return self.l

    def decode(self, string):
        self.l = []
        for each in string:
                if self.dic_dn.get(each) == None:
                    self.l.append(each)
                else:
                    self.l.append(self.dic_dn.get(each))
        return self.l

    def encodes(self, string):
        self.l = []
        for each in string:
                if self.dic_en.get(each) == None:
                    self.l.append(each)
                else:
                    self.l.append(self.dic_en.get(each))
        return ''.join(self.l)

    def decodes(self, string):
        self.l = []
        for each in string:
                if self.dic_dn.get(each) == None:
                    self.l.append(each)
                else:
                    self.l.append(self.dic_dn.get(each))
        return ''.join(self.l)
