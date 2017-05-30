from tkinter import Canvas
from cores import Cores


class Semaforo:

    def __init__(self, tag, pos):
        """

        :param tag: Tag de identificação do semáforo
        :param pos: posicão do semáforo no eixo X ou Y, para fins de localização
        """

        self.estados = ["verde", "amarelo", "vermelho"]
        self.tag = tag
        self.estado = 'vermelho'
        self.cor_inicial = 'vermelho'
        self.posicao = pos

    def add_horizontal(self, master: Canvas, x, y, estado, ordem = 0):
        """
        Adiciona um semáforo horizontal na posição indicada

        :param master: Conteiner
        :param x: Coordenada X
        :param y: Coordenada Y
        :param estado = cor atual do semaforo
        :return:
        """
        semaforos = []

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        self.cor_inicial = estado

        if estado is "vermelho":
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.estado = "vermelho"
        if estado is "amarelo":
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.estado = "amarelo"
        if estado is "verde":
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.estado = "verde"

        if ordem == 0:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))
            semaforos.append(master.create_oval(x - 25, y, x, y + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x - 50, y, x + 25 - 50, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
        elif ordem == 1:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
            semaforos.append(master.create_oval(x - 25, y, x, y + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x - 50, y, x + 25 - 50, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))

        return semaforos

    def add_vertical(self, master: Canvas, x, y, estado, ordem=0):
        """
        Adiciona um semáforo vertical na posição indicada

        :param master: Conteiner
        :param x: Coordenada X
        :param y: Coordenada Y
        :param estado = cor atual do semaforo
        :return:
        """
        semaforos = []

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        self.cor_inicial = estado

        if estado is "vermelho":
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.estado = "vermelho"
        if estado is "amarelo":
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.estado = "amarelo"
        if estado is "verde":
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.estado = "verde"

        if ordem == 0:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))
            semaforos.append(master.create_oval(x, y + 25, x + 25, y + 25 + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x, y + 50, x + 25, y + 25 + 50, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
        elif ordem == 1:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
            semaforos.append(master.create_oval(x, y + 25, x + 25, y + 25 + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x, y + 50, x + 25, y + 25 + 50, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))

        return semaforos

    def mudar_estado(self, master, estado):
        """
        Altera o estado do semáforo

        :param master: Conteiner
        :param estado = cor atual do semaforo
        :return:
        """

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        if estado is "vermelho":
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.estado = 'vermelho'
        if estado is "amarelo":
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.estado = 'amarelo'
        if estado is "verde":
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.estado = 'verde'

        master.itemconfig(self.tag + '_vm', fill=cor_vermelho, width=largura_vm)
        master.itemconfig(self.tag + '_am', fill=cor_amarelo, width=largura_am)
        master.itemconfig(self.tag + '_vd', fill=cor_verde, width=largura_vd)

