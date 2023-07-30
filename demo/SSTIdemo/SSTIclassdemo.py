
def shout1():
    print("all aw")
    return 'all aw'

class aw(object):

    def __init__(self):
        self.name = "aw"

    def shout2(self):
        print("aw")
        return 'aw'

class awtwo():

    def __init__(self):
        self.name = "aw two"

    def shout3(self):
        print("aw aw")
        return 'aw aw'

if __name__ == "__main__":
    import SSTIclassdemo2
    print(__file__ + " -> __builtins__ : " + str(type(__builtins__)))

    print('__import__' in dir(__builtins__))