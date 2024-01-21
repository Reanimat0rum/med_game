import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_analysis(val: list, mean=None, func='normal', coeff = 1, std_coef = 3):
        if mean is None:
            mean = (val[0] + val[1]) / 2
        std_dev = abs(mean - val[1])/ std_coef
        if func == 'normal':
            fun = np.random.normal
        elif func == 'lognormal':
            fun = np.random.lognormal
        else:
            raise ValueError
        gen_val = fun(mean, std_dev)
        while gen_val < val[0] or gen_val > val[1]:
            gen_val = fun(mean, std_dev)
        return coeff * round(gen_val, 1)

class Organ():
    def __init__(self):
        self.tissue = {'Соединительная':None, 'Мышечная':None, 'Эпителий':None, 'Жировая':None, 'Нервная':None}
        for key in self.tissue.keys():
            self.tissue[key] = 1 / len(self.tissue)

class Stomach(Organ):
    def __init__(self):
        Organ.__init__(self)
        self.organ_name = 'Желудок'
        self.tissue['Соединительная'] = .03
        self.tissue['Мышечная'] = .70
        self.tissue['Эпителий'] = .2
        self.tissue['Жировая'] = .03
        self.tissue['Нервная'] = .03
        self.system = 'ЖКТ'


class Blood(Organ):
    def __init__(self):
        Organ.__init__(self)
        self.organ_name = 'Кровь'
        self.tissue['Соединительная'] = 1
        self.tissue['Мышечная'] = 0
        self.tissue['Эпителий'] = 0
        self.tissue['Жировая'] = 0
        self.tissue['Нервная'] = 0
        self.system = 'Кровеносная'


class NormalAnalysis():
    def __init__(self):
        df = pd.read_csv('CBC.csv', encoding='cp1251', sep=';', names=['name', 'short_name', 'women', 'man'])
        cbc = {}
        for i in df.iterrows():
            cbc[i[1][1]] = {'name': i[1][0], 'woman': [float(i[1][2].split('-')[0].replace(',', '.')),
                                                            float(i[1][2].split('-')[1].replace(',', '.'))],
                                 'man': [float(i[1][3].split('-')[0].replace(',', '.')),
                                         float(i[1][3].split('-')[1].replace(',', '.'))]
                                 }
        del df
        self.norm_analysis = {}
        self.norm_analysis['cbc'] = cbc

class Patient(NormalAnalysis):
    def __init__(self, name='John', sex='man'):
        NormalAnalysis.__init__(self)
        self.human_name = name
        self.stomach = Stomach()
        self.sex = sex
        self.set_analysis()

    def set_analysis(self):

        self.analysis ={}
        for i in self.norm_analysis.keys():
            self.analysis[i] = {}
            for keys in self.norm_analysis[i].keys():
                self.analysis[i][keys] = {}
                self.analysis[i][keys]['name'] = self.norm_analysis[i][keys]['name']
                self.analysis[i][keys]['value'] = generate_analysis(self.norm_analysis[i][keys][self.sex])
        return None

class General_pathology():
    def __init__(self):
        self.affected_organs = None
        self.affected_tissue = None
        self.analysis_dev = None

    def act_analysis(self, patient:Patient):
        if not self.analysis_dev:
            return print('Не влияет на анализы')
        for i in self.analysis_dev.keys():
            for keys in self.analysis_dev[i].keys():
                val = self.analysis_dev[i][keys]
                dif = generate_analysis(list(map(abs, val)), mean=0, coeff=val[1]/abs(val[1]), func='lognormal')
                patient.analysis[i][keys]['value'] = patient.analysis[i][keys]['value'] + dif
                print(patient.analysis[i][keys]['value'])
                print(dif)
        return patient

class Pathology_malabsorbtion(General_pathology):
    def __init__(self,target_org=('Желудок'), target_tissue = ('Эпителий')):
        General_pathology.__init__(self)
        self.affected_organs = target_org
        self.affected_tissue = target_tissue
        self.analysis_dev = {'cbc':{'RBC':[0, -3]}}


if __name__ == '__main__':
    p = Patient('Mary', 'woman')
    print(p.analysis)
    pat = Pathology_malabsorbtion()
    d = pat.act_analysis(p)
    print(d.analysis)
    # t = np.empty(shape=[1,1000])
    # print(t)
    # for i in range(t.shape[1]):
    #     t[0][i] = generate_analysis([4.1,5.2])
    # print(t.mean())
    # print(t.max())
    # print(t.min())
    # print(t.std())
    # fig, ax = plt.subplots()
    # n, bins, patches = plt.hist(t[0], 12, density=True, facecolor='g', alpha=0.75)
    # plt.show()

    #
    # t = np.empty(shape=[1,1000])
    # for i in range(t.shape[1]):
    #     t[0][i] = generate_analysis([0,3], 0, 'lognormal', -1, 3)
    # print('mean', t.mean())
    # print('max', t.max())
    # print('min', t.min())
    # print('std', t.std())
    # # print(t[0])
    # fig, ax = plt.subplots()
    # n, bins, patches = plt.hist(t[0], 20, density=True, facecolor='g', alpha=0.75)
    # plt.show()
