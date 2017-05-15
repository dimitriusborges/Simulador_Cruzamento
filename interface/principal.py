import platform
from tkinter import *
from veiculo import Veiculo
from semaforo import Semaforo
from rua import Rua


class Principal:

    def __init__(self):

        self.i_r1 = 608, 0      # inicio da rua 1
        self.i_r2 = 208, 400    # inicio da rua 2

        self.img_veiculo = []  # veiculos adcionados ao canvas
        self.veiculos = {}      # dicionario que relaciona obj_veiculo com img_veiculo

        # Configurações da tela/conteiner
        self.root = Tk()
        self.root.title('Cruzamento')
        self.root.option_add('*tearOff', False)

        if platform.system().lower() == 'linux':
            self. root.attributes('-zoomed', True)
        else:
            self.root.state('zoomed')

        # Canvas
        self.frame_canvas = Frame(self.root, bg='white')
        self.frame_canvas.pack(fill=BOTH, expand=YES)

        self.frame_canvas.columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frame_canvas, width='1280', height='1280', scrollregion=(0, 0, 300, 450))
        self.canvas.grid(row=0, column=0, stick=('n', 's'))

        self.inserir_ruas()

        car = Veiculo()

        self.img_veiculo.append(car.adicionar(self.canvas, self.i_r1[0], self.i_r1[1]))
        self.veiculos[car] = self.img_veiculo[0]

        self.sem_1 = Semaforo('sem_1')

        self.sem_1.add_horizontal(self.canvas, self.i_r1[0] - 40,
                                  self.i_r1[1] + Rua().comprimento - 35,
                                  vermelho=True)

        self.sem_2 = Semaforo('sem_2')

        self.sem_2.add_vertical(self.canvas, self.i_r2[0] + Rua().comprimento - 40,
                                self.i_r2[1] + Rua().largura + 15,
                                verde=True)

        self.sem_4 = Semaforo('sem_4')

        self.sem_4.add_vertical(self.canvas, self.i_r1[0] + Rua().largura + 10,
                                self.i_r1[1] + Rua().comprimento - Rua().largura - 15,
                                verde=True)

        self.sem_3 = Semaforo('sem_3')

        self.sem_3.add_horizontal(self.canvas, self.i_r2[0] + Rua().comprimento + Rua().largura + 60,
                                  self.i_r2[1] + Rua().largura + 10,
                                  vermelho=True)

    def inserir_ruas(self):
        """

        :return:
        """
        comp = Rua().comprimento
        larg = Rua().largura

        # Rua 1
        self.canvas.create_text(self.i_r1[0] - 20, self.i_r1[1] + 10, text="Rua 1")

        self.canvas.create_line(self.i_r1[0],
                                self.i_r1[1],
                                self.i_r1[0],
                                self.i_r1[1] + comp,
                                width=3)

        self.canvas.create_line(self.i_r1[0] + larg,
                                self.i_r1[1],
                                self.i_r1[0] + larg,
                                self.i_r1[1] + comp,
                                width=3)

        self.canvas.create_line(self.i_r1[0],
                                self.i_r1[1] + comp + larg,         # comp da 1ª parte + larg do cruzamento
                                self.i_r1[0],
                                self.i_r1[1] + comp + larg + comp,   # comp da 1ª parte + larg cruzamento + comp da rua
                                width=3)

        self.canvas.create_line(self.i_r1[0] + larg,
                                self.i_r1[1] + comp + larg,
                                self.i_r1[0] + larg,
                                self.i_r1[1] + comp + larg + comp,
                                width=3)

        # Rua 2
        self.canvas.create_text(self.i_r2[0], self.i_r2[1] - 10, text="Rua 2")

        self.canvas.create_line(self.i_r2[0],
                                self.i_r2[1],
                                self.i_r2[0] + comp,
                                self.i_r2[1],
                                width=3)

        self.canvas.create_line(self.i_r2[0],
                                self.i_r2[1] + larg,
                                self.i_r2[0] + comp,
                                self.i_r2[1] + larg,
                                width=3)

        self.canvas.create_line(self.i_r2[0] + comp + larg,         # comp da 1ª parte + larg do cruzamento
                                self.i_r2[1],
                                self.i_r2[0] + comp + larg + comp,  # comp da 1ª parte + larg cruzamento + comp da rua
                                self.i_r2[1],
                                width=3)

        self.canvas.create_line(self.i_r2[0] + comp + larg,
                                self.i_r2[1] + larg,
                                self.i_r2[0] + comp + larg + comp,
                                self.i_r2[1] + larg,
                                width=3)

    def iniciar_app(self):
        """

        :return:
        """
        self.root.minsize(640, 640)
        self.root.mainloop()


iniciar = Principal()
iniciar.iniciar_app()
