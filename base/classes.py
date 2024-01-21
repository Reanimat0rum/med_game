class Organ_system(object):
    systems_list = {}

class Organ(Organ_system):
    def extract(self):
        print('Вы извлекли орган')

class Stomach(Organ):
    organ_name = 'Желудок'
    system = 'ЖКТ'
class Human():
    def __init__(self, name):
        self.human_name = name
        self.systems = Organ_system()
        self.stomach = Stomach()
        self.systems.systems_list['ЖКТ']=self.stomach

if __name__ == '__main__':
    John = Human('Джон')
    print(John.systems.systems_list)

