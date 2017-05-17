from tkinter import Canvas
from cores import Cores
class Semaforo:

    def __init__(self, tag, pos):
        """

        """
        self.tag = tag
        self.estado = False
        self.posicao = pos

    def add_horizontal(self, master: Canvas, x, y, verde=False, amarelo=False, vermelho=False):
        """

        :param master:
        :param x:
        :param y:
        :param verde:
        :param amarelo:
        :param vermelho:
        :return:
        """
        semaforos = []

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        if vermelho is True:
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.estado = False
        if amarelo is True:
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.estado = True
        if verde is True:
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.estado = True

        semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                            width=largura_vm))
        semaforos.append(master.create_oval(x - 25, y, x, y + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                            width=largura_am))
        semaforos.append(master.create_oval(x - 50, y, x + 25 - 50, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                            width=largura_vd))

        return semaforos

    def add_vertical(self, master: Canvas, x, y, verde=False, amarelo=False, vermelho=False):
        """

        :param master:
        :param x:
        :param y:
        :param verde:
        :param amarelo:
        :param vermelho:
        :return:
        """
        semaforos = []

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        if vermelho is True:
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.estado = False
        if amarelo is True:
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.estado = True
        if verde is True:
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.estado = True

        semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                            width=largura_vm))
        semaforos.append(master.create_oval(x, y + 25, x + 25, y + 25 + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                            width=largura_am))
        semaforos.append(master.create_oval(x, y + 50, x + 25, y + 25 + 50, fill=cor_verde, tag=self.tag + '_vd',
                                            width=largura_vd))

        return semaforos

    def mudar_estado(self, master, verde=False, vermelho=False, amarelo=False):
        """
        :param master:
        :param verde:
        :param vermelho:
        :param amarelo:
        :return:
        """
        cor_vermelho = Cores().vermelho_off
        cor_amarelo = Cores().amarelo_off
        cor_verde = Cores().verde_off

        if vermelho is True:
            cor_vermelho = Cores().vermelho_on
            self.estado = False
        if amarelo is True:
            cor_amarelo = Cores().amarelo_on
            self.estado = True
        if verde is True:
            cor_verde = Cores().verde_on
            self.estado = True

        master.itemconfig(self.tag + '_vm', fill=cor_vermelho)
        master.itemconfig(self.tag + '_am', fill=cor_amarelo)
        master.itemconfig(self.tag+'_vd', fill=cor_verde)

