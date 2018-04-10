class Rot13():
    """Usage:
    rot=Rot13()
    rot.encode(str)
    rot.decode(str)
    :rtype list with each element in str
    rot.decodes(str)
    rot.encodes(str)
    :rtype str"""

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
        li = []
        for each in string:
            if not self.dic_en.get(each):
                li.append(each)
            else:
                li.append(self.dic_en.get(each))
        return li

    def decode(self, string):
        li = []
        for each in string:
            if not self.dic_dn.get(each):
                li.append(each)
            else:
                li.append(self.dic_dn.get(each))
        return li

    def encodes(self, string):
        li = []
        for each in string:
            if not self.dic_en.get(each):
                li.append(each)
            else:
                li.append(self.dic_en.get(each))
        return ''.join(li)

    def decodes(self, string):
        li = []
        for each in string:
            if not self.dic_dn.get(each):
                li.append(each)
            else:
                li.append(self.dic_dn.get(each))
        return ''.join(li)


if __name__ == '__main__':
    import this
    print(Rot13().decode(this.s))