import os
import time
import random
import platform
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'objetos'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'animacoes'))

from anim_veiculo import AnimVeiculos
from veiculo import Veiculo
from semaforo import Semaforo
from anim_semaforo import AnimSemaforos
from rua import Rua

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'objetos'))


class Principal:
    def __init__(self):

        self.i_r1 = 608, 0      # inicio da rua 1
        self.i_r2 = 208, 400    # inicio da rua 2

        self.veiculos_ns = []  # fila de veiculos na via Norte->Sul
        self.veiculos_sn = []  # fila de veiculos na via Sul->Norte
        self.veiculos_ol = []  # fila de veiculos na via Oeste->Leste
        self.veiculos_lo = []  # fila de veiculos na via Leste->Oeste

        self.semaforos = []

        self.velocidades = [8, 11, 11]   # 30km/h, 40km/h, 40km/h, em metros por segundo, valores aproximados

        # Configurações da tela/conteiner
        self.root = Tk()
        self.root.title('Cruzamento')
        self.root.option_add('*tearOff', False)

        if platform.system().lower() == 'linux':
            self.root.attributes('-zoomed', True)
        else:
            self.root.state('zoomed')

        # Canvas
        self.frame_canvas = Frame(self.root, bg='white')
        self.frame_canvas.pack(fill=BOTH, expand=YES)

        self.frame_canvas.columnconfigure(0, weight=1)
        self.frame_canvas.columnconfigure(1, weight=1)
        self.frame_canvas.rowconfigure(0, weight=1)

        self.canvas = Canvas(self.frame_canvas, width='1280', height='1280', scrollregion=(0, 0, 1280*2, 1480))
        self.canvas.grid(row=0, column=0, columnspan=2, stick=('n', 's', 'w', 'e'))
        self.canvas.bind("<MouseWheel>", self.evento_scroll_bar)

        #Scrollbar
        self.scroll_vertical_canvas = Scrollbar(self.frame_canvas, relief='groove')
        self.scroll_vertical_canvas.grid(row=0, column=3, sticky=('n', 's'))

        self.canvas.config(yscrollcommand=self.scroll_vertical_canvas.set)
        self.scroll_vertical_canvas.config(command=self.canvas.yview)

        self.scroll_horizontal_canvas = Scrollbar(self.frame_canvas, relief='groove', orient=HORIZONTAL)
        self.scroll_horizontal_canvas.grid(row=1, column=0, columnspan=2, sticky=('e', 'w'))

        self.canvas.config(xscrollcommand=self.scroll_horizontal_canvas.set)
        self.scroll_horizontal_canvas.config(command=self.canvas.xview)

        self.inserir_semaforos()
        self.inserir_ruas()

        self.anim_semaforos = AnimSemaforos(self.canvas, self.semaforos)
        self.anim_semaforos.setDaemon(True)
        self.anim_semaforos.start()

        self.inserir_saidas()
        self.inserir_entradas()
        self.preencher_entradas(None)
        self.coletar_seeder_r1()
        self.coletar_seeder_r2()

        self.thread_seeder_veiculos = threading.Thread(target=self.seeder_veiculos)
        self.thread_seeder_veiculos.setDaemon(True)
        self.thread_seeder_veiculos.start()

        anim_veiculos_ns = AnimVeiculos(self.canvas, self.sem_ns, self.veiculos_ns, 'ns')
        anim_veiculos_ns.setDaemon(True)
        anim_veiculos_ns.start()

        anim_veiculos_sn = AnimVeiculos(self.canvas, self.sem_sn, self.veiculos_sn, 'sn')
        anim_veiculos_sn.setDaemon(True)
        anim_veiculos_sn.start()

        anim_veiculos_ol = AnimVeiculos(self.canvas, self.sem_ol, self.veiculos_ol, 'ol')
        anim_veiculos_ol.setDaemon(True)
        anim_veiculos_ol.start()

        anim_veiculos_lo = AnimVeiculos(self.canvas, self.sem_lo, self.veiculos_lo, 'lo')
        anim_veiculos_lo.setDaemon(True)
        anim_veiculos_lo.start()

    def inserir_ruas(self):
        """
        Insere na interface a representação gráfica das ruas
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
                                self.i_r1[1] + comp + larg,  # comp da 1ª parte + larg do cruzamento
                                self.i_r1[0],
                                self.i_r1[1] + comp + larg + comp,  # comp da 1ª parte + larg cruzamento + comp da rua
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

        self.canvas.create_line(self.i_r2[0] + comp + larg,  # comp da 1ª parte + larg do cruzamento
                                self.i_r2[1],
                                self.i_r2[0] + comp + larg + comp,  # comp da 1ª parte + larg cruzamento + comp da rua
                                self.i_r2[1],
                                width=3)

        self.canvas.create_line(self.i_r2[0] + comp + larg,
                                self.i_r2[1] + larg,
                                self.i_r2[0] + comp + larg + comp,
                                self.i_r2[1] + larg,
                                width=3)

    def inserir_semaforos(self):
        """
        Insere na interface a representação gráfica dos semáforos
        :return:
        """
        # Semaforos

        self.sem_ns = Semaforo('sem_1', self.i_r1[1] + Rua().comprimento - 40)

        self.sem_ns.add_horizontal(self.canvas, self.i_r1[0] - 40,
                                   self.i_r1[1] + Rua().comprimento - 35,
                                   "vermelho")

        self.canvas.create_text(self.i_r1[0] - 104,
                                self.i_r1[1] + Rua().comprimento - 23,
                                font=("Arial", 14), text="S1")

        self.semaforos.append(self.sem_ns)

        self.sem_ol = Semaforo('sem_2', self.i_r2[0] + Rua().comprimento - 40)

        self.sem_ol.add_vertical(self.canvas, self.i_r2[0] + Rua().comprimento - 40,
                                 self.i_r2[1] + Rua().largura + 15,
                                 "verde")

        self.canvas.create_text(self.i_r2[0] + Rua().comprimento - 27,
                                self.i_r2[1] + Rua().largura + 105,
                                font=("Arial", 14), text="S2")

        self.semaforos.append(self.sem_ol)

        self.sem_sn = Semaforo('sem_3', self.i_r2[1] + Rua().largura + 10)

        self.sem_sn.add_horizontal(self.canvas, self.i_r2[0] + Rua().comprimento + Rua().largura + 60,
                                   self.i_r2[1] + Rua().largura + 10,
                                   "vermelho", 1)

        self.canvas.create_text(self.i_r2[0] + Rua().comprimento + Rua().largura + 101,
                                self.i_r2[1] + Rua().largura + 22,
                                font=("Arial", 14), text="S3")

        self.semaforos.append(self.sem_sn)

        self.sem_lo = Semaforo('sem_4', self.i_r1[0] + Rua().largura)

        self.sem_lo.add_vertical(self.canvas, self.i_r1[0] + Rua().largura + 10,
                                 self.i_r1[1] + Rua().comprimento - Rua().largura - 15,
                                 "verde", 1)

        self.canvas.create_text(self.i_r1[0] + Rua().largura + 25,
                                self.i_r1[1] + Rua().comprimento - Rua().largura - 27,
                                font=("Arial", 14), text="S4")

        self.semaforos.append(self.sem_lo)

    def inserir_saidas(self):
        """
        Insere no gráfico os contadores de veículos
        :return:
        """

        # Norte Sul
        self.canvas.create_text(self.i_r1[0] + Rua().largura + 20,
                                self.i_r1[1] + 10,
                                text="Gerados: 0",
                                anchor='w',
                                tag='ger_ns')
        self.canvas.create_text(self.i_r1[0] + Rua().largura + 20,
                                self.i_r1[1] + 30,
                                text="Impedidos: 0",
                                anchor='w',
                                tag='imp_ns')

        # Oeste Leste
        self.canvas.create_text(self.i_r2[0],
                                self.i_r2[1] + Rua().largura + 20,
                                text="Gerados: 0",
                                anchor='w',
                                tag='ger_ol')
        self.canvas.create_text(self.i_r2[0],
                                self.i_r2[1] + Rua().largura + 40,
                                text="Impedidos: 0",
                                anchor='w',
                                tag='imp_ol')

        # Sul Norte
        self.canvas.create_text(self.i_r1[0] + Rua().largura + 20,
                                self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - 40,
                                text="Gerados: 0",
                                anchor='w',
                                tag='ger_sn')
        self.canvas.create_text(self.i_r1[0] + Rua().largura + 20,
                                self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - 20,
                                text="Impedidos: 0",
                                anchor='w',
                                tag='imp_sn')

        # Leste Oeste
        self.canvas.create_text(self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento - 70,
                                self.i_r2[1] + Rua().largura + 20,
                                text="Gerados: 0",
                                anchor='w',
                                tag='ger_lo')
        self.canvas.create_text(self.i_r2[0] + + Rua().comprimento + Rua().largura + Rua().comprimento - 70,
                                self.i_r2[1] + Rua().largura + 40,
                                text="Impedidos: 0",
                                anchor='w',
                                tag='imp_lo')

        # Total de veículos
        self.canvas.create_text(self.i_r2[0] + + Rua().comprimento + Rua().largura + Rua().comprimento - 90,
                                self.i_r2[1] + Rua().largura + 370,
                                font=('Arial', 18),
                                text="Total: 00",
                                anchor='w',
                                tag='total')

    def inserir_entradas(self):
        """

        :return:
        """

        self.canvas.create_text(1308, 10, font=("Arial", 16), text='Geradores')

        # GERADOR RUA 1
        self.canvas.create_text(1308, 45, font=("Arial", 14), text='Rua 1:')

        self.spin_veiculos_ns = Spinbox(self.canvas, width=3, from_=1, to=99)
        self.spin_veiculos_ns.place(x=1308, y=80)
        self.spin_veiculos_ns.pack()
        self.canvas.create_window(1328, 85, window=self.spin_veiculos_ns)
        self.spin_veiculos_ns.delete(0, END)
        self.spin_veiculos_ns.insert(0, 5)

        self.canvas.create_text(1348, 85, anchor='w', text='Carro(s) a cada')

        self.spin_minutos_ns = Spinbox(self.canvas, width=3, from_=1, to=99)
        self.spin_minutos_ns.pack()
        self.canvas.create_window(1458, 85, window=self.spin_minutos_ns)

        self.canvas.create_text(1478, 85, anchor='w', text='Minuto(s)')

        self.bt_enviar_seeder_r1 = Button(self.canvas, width=10, text="Enviar",
                                          command=self.coletar_seeder_r1)
        self.bt_enviar_seeder_r1.pack()
        self.canvas.create_window(1608, 85, window=self.bt_enviar_seeder_r1)

        # GERADOR RUA 2
        self.canvas.create_text(1308, self.i_r1[1] + 125, font=("Arial", 14), text='Rua 2:')

        self.spin_veiculos_ol = Spinbox(self.canvas, width=3, from_=1, to=99)
        self.spin_veiculos_ol.pack()
        self.canvas.create_window(1328, 165, window=self.spin_veiculos_ol)
        self.spin_veiculos_ol.delete(0, END)
        self.spin_veiculos_ol.insert(0, 10)

        self.canvas.create_text(1348, 165, anchor='w', text='Carro(s) a cada')

        self.spin_minutos_ol = Spinbox(self.canvas, width=3, from_=1, to=99)
        self.spin_minutos_ol.pack()
        self.canvas.create_window(1458, 165, window=self.spin_minutos_ol)

        self.canvas.create_text(1478, 165, anchor='w', text='Minuto(s)')

        self.bt_enviar_seeder_r2 = Button(self.canvas, width=10, text="Enviar", command=self.coletar_seeder_r2)
        self.bt_enviar_seeder_r2.pack()
        self.canvas.create_window(1608, 165, window=self.bt_enviar_seeder_r2)

        # PLANO
        self.canvas.create_text(1318, 255, font=("Arial", 16), text='Configuração')

        self.canvas.create_text(1318, 285, anchor='w', text="Tipo:")
        self.combo_plano = ttk.Combobox(self.canvas, width=10, value=('principal', "atuado"), state='readonly')
        self.combo_plano.set('principal')
        self.combo_plano.bind("<<ComboboxSelected>>", self.preencher_entradas)
        self.combo_plano.pack()
        self.canvas.create_window(1428, 285, window=self.combo_plano)

        self.canvas.create_text(1493, 285, anchor='w', text="Ciclo:")
        self.ciclo = Spinbox(self.canvas, width=6, from_=1, to=255, bg='white')
        self.ciclo.pack()
        self.canvas.create_window(1563, 285, window=self.ciclo)

        # GRUPOS

        paragrafo_1 = 35
        paragrafo_2 = 30
        espac_interno = 30
        espac_externo = 90
        cor_inicial = ['verde', 'vermelho']

        # Grupo 1
        self.canvas.create_text(1318, 325, font=("Arial", 12), anchor='w', text='Semáforo 1')

        self.canvas.create_text(1318, 360, anchor='w', text='Cor Inicial:')
        self.combo_ci_gp1 = ttk.Combobox(self.canvas, width=10, value=cor_inicial, state='readonly')
        self.combo_ci_gp1.pack()
        self.canvas.create_window(1338 + espac_externo, 360, window=self.combo_ci_gp1)

        self.canvas.create_text(1318, 360 + paragrafo_1, anchor='w', text='VD:')
        self.tempo_vd_g1 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vd_g1.pack()
        self.canvas.create_window(1338 + espac_interno, 365 + paragrafo_2, window=self.tempo_vd_g1)

        self.canvas.create_text(1318 + espac_externo, 360 + paragrafo_1, anchor='w', text='AM:')
        self.tempo_am_g1 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_am_g1.pack()
        self.canvas.create_window(1338 + espac_externo + espac_interno, 365 + paragrafo_2, window=self.tempo_am_g1)

        self.canvas.create_text(1318 + espac_externo*2, 360 + paragrafo_1, anchor='w', text='VM:')
        self.tempo_vm_g1 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vm_g1.pack()
        self.canvas.create_window(1338 + espac_externo*2 + espac_interno, 365 + paragrafo_2, window=self.tempo_vm_g1)

        # Grupo 2
        self.canvas.create_text(1318, 460, font=("Arial", 12), anchor='w', text='Semáforo 2')

        self.canvas.create_text(1318, 495, anchor='w', text='Cor Inicial:')
        self.combo_ci_gp2 = ttk.Combobox(self.canvas, width=10, value=cor_inicial, state='readonly')
        self.combo_ci_gp2.pack()
        self.canvas.create_window(1338 + espac_externo, 495, window=self.combo_ci_gp2)

        self.canvas.create_text(1318, 490 + paragrafo_1, anchor='w', text='VD:')
        self.tempo_vd_g2 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vd_g2.pack()
        self.canvas.create_window(1338 + espac_interno, 495 + paragrafo_2, window=self.tempo_vd_g2)

        self.canvas.create_text(1318 + espac_externo, 490 + paragrafo_1, anchor='w', text='AM:')
        self.tempo_am_g2 =Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_am_g2.pack()
        self.canvas.create_window(1338 + espac_externo + espac_interno, 495 + paragrafo_2, window=self.tempo_am_g2)

        self.canvas.create_text(1318 + espac_externo*2, 490 + paragrafo_1, anchor='w', text='VM:')
        self.tempo_vm_g2 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vm_g2.pack()
        self.canvas.create_window(1338 + espac_externo*2 + espac_interno, 495 + paragrafo_2, window=self.tempo_vm_g2)

        # Grupo 3
        self.canvas.create_text(1318, 595, font=("Arial", 12), anchor='w', text='Semáforo 3')

        self.canvas.create_text(1318, 625, anchor='w', text='Cor Inicial:')
        self.combo_ci_gp3 = ttk.Combobox(self.canvas, width=10, value=cor_inicial, state='readonly')
        self.combo_ci_gp3.pack()
        self.canvas.create_window(1338 + espac_externo, 625, window=self.combo_ci_gp3)

        self.canvas.create_text(1318, 620 + paragrafo_1, anchor='w', text='VD:')
        self.tempo_vd_g3 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vd_g3.pack()
        self.canvas.create_window(1338 + espac_interno, 620 + paragrafo_2, window=self.tempo_vd_g3)

        self.canvas.create_text(1318 + espac_externo, 620 + paragrafo_1, anchor='w', text='AM:')
        self.tempo_am_g3 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_am_g3.pack()
        self.canvas.create_window(1338 + espac_externo + espac_interno, 625 + paragrafo_2, window=self.tempo_am_g3)

        self.canvas.create_text(1318 + espac_externo*2, 620 + paragrafo_1, anchor='w', text='VM:')
        self.tempo_vm_g3 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vm_g3.pack()
        self.canvas.create_window(1338 + espac_externo*2 + espac_interno, 625 + paragrafo_2, window=self.tempo_vm_g3)

        # Grupo 4
        self.canvas.create_text(1318, 726, font=("Arial", 12), anchor='w', text='Semáforo 4')

        self.canvas.create_text(1318, 756, anchor='w', text='Cor Inicial:')
        self.combo_ci_gp4 = ttk.Combobox(self.canvas, width=10, value=cor_inicial, state='readonly')
        self.combo_ci_gp4.pack()
        self.canvas.create_window(1338 + espac_externo, 756, window=self.combo_ci_gp4)

        self.canvas.create_text(1318, 751 + paragrafo_1, anchor='w', text='VD:')
        self.tempo_vd_g4 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vd_g4.pack()
        self.canvas.create_window(1338 + espac_interno, 756 + paragrafo_2, window=self.tempo_vd_g4)

        self.canvas.create_text(1318 + espac_externo, 751 + paragrafo_1, anchor='w', text='AM:')
        self.tempo_am_g4 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_am_g4.pack()
        self.canvas.create_window(1338 + espac_externo + espac_interno, 756 + paragrafo_2, window=self.tempo_am_g4)

        self.canvas.create_text(1318 + espac_externo*2, 751 + paragrafo_1, anchor='w', text='VM:')
        self.tempo_vm_g4 = Spinbox(self.canvas, width=6, from_=0, to=255, bg='white')
        self.tempo_vm_g4.pack()
        self.canvas.create_window(1338 + espac_externo*2 + espac_interno, 756 + paragrafo_2, window=self.tempo_vm_g4)

        # Enviar
        self.bt_enviar_plano = Button(self.canvas, text="enviar", width=10, command=self.coletar_dados_grupos)
        self.bt_enviar_plano.pack()
        self.canvas.create_window(1338, 840, window=self.bt_enviar_plano)

        # ATUADO
        self.bt_atuado = Button(self.canvas, text="Atuar", width=10, height=3,
                                command=self.iniciar_atuado)
        self.bt_atuado.pack()
        self.canvas.create_window(250, 800, window=self.bt_atuado)

    def desenhar_grafico(self, tempos):
        """
        Insere na interface o gráfico representativo do tempo configurado para os semáforos
        :return:
        """
        expessura = 15              # Espessura da linha do gráfico
        tamanho_total = 300         # Tamanho total do gráfico com as três cores
        x_inicial = 1590            # Posição do primeiro gráfico
        y_inicial = 390             # Posição do primeiro gráfico
        paragrafo = 130             # distância entre os gráficos

        dic_cores = {'verde': 'green',
                     'amarelo': 'yellow',
                     'vermelho': 'red'}

        tempos_semaforo =tempos                                                         # Recupera o tempo operante
        indice_tempos = AnimSemaforos(self.canvas, self.semaforos).indice_cor           # Auxiliar
        seq_cores = AnimSemaforos(self.canvas, self.semaforos).seq_cores                # Auxiliar

        # Remove o gráfico antigo
        self.canvas.delete('cor_1')
        self.canvas.delete('cor_2')
        self.canvas.delete('cor_3')

        indice = 0
        for semaforo in self.semaforos:

            cor = semaforo.cor_inicial                              # Cor da primeira parte
            tempo = (tempos_semaforo[indice])[indice_tempos[cor]]   # Tempo da cor
            ciclo = sum(tempos_semaforo[indice])                    # ciclo total do semáforo
            escala = (tamanho_total * tempo)/ciclo                  # Conversão de tempo para pixels

            fim_anterior = x_inicial

            # Desenha o gráfico de acordo com os valores de tempo
            for aux in range(0, 3):

                self.canvas.create_rectangle(fim_anterior,
                                             y_inicial + paragrafo * indice,
                                             fim_anterior + escala,
                                             y_inicial + expessura + paragrafo * indice,
                                             fill=dic_cores[cor],
                                             tag='cor_' + str(indice))

                fim_anterior += escala  # inicio de uma cor = final de outra e final de outra = inicio + escala
                cor = seq_cores[cor]
                tempo = (tempos_semaforo[indice])[indice_tempos[cor]]
                escala = (tamanho_total * tempo) / ciclo

            indice += 1

    def preencher_entradas(self, event):
        """
        Completa as entradas do sistema com os valores padrões
        :return:
        """

        # PLANO E GRUPOS
        tempo_atual = []
        if self.combo_plano.get() == 'principal':
            tempo_atual = self.anim_semaforos.matriz_principal
        elif self.combo_plano.get() == 'atuado':
            tempo_atual = self.anim_semaforos.matriz_atuado

        self.ciclo.delete(0, END)
        self.ciclo.insert(0, sum(tempo_atual[0]))

        self.tempo_vd_g1.delete(0, END)
        self.tempo_vd_g1.insert(0, (tempo_atual[0])[0])
        self.tempo_am_g1.delete(0, END)
        self.tempo_am_g1.insert(0, (tempo_atual[0])[1])
        self.tempo_vm_g1.delete(0, END)
        self.tempo_vm_g1.insert(0, (tempo_atual[0])[2])

        self.tempo_vd_g2.delete(0, END)
        self.tempo_vd_g2.insert(0, (tempo_atual[1])[0])
        self.tempo_am_g2.delete(0, END)
        self.tempo_am_g2.insert(0, (tempo_atual[1])[1])
        self.tempo_vm_g2.delete(0, END)
        self.tempo_vm_g2.insert(0, (tempo_atual[1])[2])

        self.tempo_vd_g3.delete(0, END)
        self.tempo_vd_g3.insert(0, (tempo_atual[2])[0])
        self.tempo_am_g3.delete(0, END)
        self.tempo_am_g3.insert(0, (tempo_atual[2])[1])
        self.tempo_vm_g3.delete(0, END)
        self.tempo_vm_g3.insert(0, (tempo_atual[2])[2])

        self.tempo_vd_g4.delete(0, END)
        self.tempo_vd_g4.insert(0, (tempo_atual[3])[0])
        self.tempo_am_g4.delete(0, END)
        self.tempo_am_g4.insert(0, (tempo_atual[3])[1])
        self.tempo_vm_g4.delete(0, END)
        self.tempo_vm_g4.insert(0, (tempo_atual[3])[2])

        if self.combo_plano.get() == 'principal':
            cores_iniciais = self.anim_semaforos.matriz_cor_inicial
        else:
            cores_iniciais = self.anim_semaforos.matriz_cor_inicial_atuado

        self.combo_ci_gp1.set(cores_iniciais[0])
        self.combo_ci_gp2.set(cores_iniciais[1])
        self.combo_ci_gp3.set(cores_iniciais[2])
        self.combo_ci_gp4.set(cores_iniciais[3])

        self.desenhar_grafico(tempo_atual)

    def coletar_dados_grupos(self):
        """
        Coleta os valores de entrada para os semárofos enviados pelo usuário
        :return:
        """
        ciclo = int(self.ciclo.get())

        semaforo1 = [int(self.tempo_vd_g1.get()), int(self.tempo_am_g1.get()), int(self.tempo_vm_g1.get())]
        s1_cor = self.combo_ci_gp1.get()

        if sum(semaforo1) != ciclo:
            messagebox.showerror("Ciclo", "A soma dos tempos do Semáforo 1 são diferentes do ciclo!")
            return

        semaforo2 = [int(self.tempo_vd_g2.get()), int(self.tempo_am_g2.get()), int(self.tempo_vm_g2.get())]
        s2_cor = self.combo_ci_gp2.get()

        if sum(semaforo2) != ciclo:
            messagebox.showerror("Ciclo", "A soma dos tempos do Semáforo 2 são diferentes do ciclo!")
            return

        semaforo3 = [int(self.tempo_vd_g3.get()), int(self.tempo_am_g3.get()), int(self.tempo_vm_g3.get())]
        s3_cor = self.combo_ci_gp3.get()

        if sum(semaforo3) != ciclo:
            messagebox.showerror("Ciclo", "A soma dos tempos do Semáforo 3 são diferentes do ciclo!")
            return

        semaforo4 = [int(self.tempo_vd_g4.get()), int(self.tempo_am_g4.get()), int(self.tempo_vm_g4.get())]
        s4_cor = self.combo_ci_gp4.get()

        if sum(semaforo4) != ciclo:
            messagebox.showerror("Ciclo", "A soma dos tempos do Semáforo 4 são diferentes do ciclo!")
            return

        if self.combo_plano.get() == 'principal':
            self.anim_semaforos.matriz_principal.clear()
            self.anim_semaforos.matriz_cor_inicial.clear()
            self.anim_semaforos.matriz_cor_inicial = [s1_cor, s2_cor, s3_cor, s4_cor]
            self.anim_semaforos.matriz_principal = [semaforo1, semaforo2, semaforo3, semaforo4]

            self.desenhar_grafico(self.anim_semaforos.matriz_principal)

        elif self.combo_plano.get() == 'atuado':
            self.anim_semaforos.matriz_atuado.clear()
            self.anim_semaforos.matriz_cor_inicial_atuado.clear()
            self.anim_semaforos.matriz_cor_inicial_atuado = [s1_cor, s2_cor, s3_cor, s4_cor]
            self.anim_semaforos.matriz_atuado = [semaforo1, semaforo2, semaforo3, semaforo4]

            self.desenhar_grafico(self.anim_semaforos.matriz_atuado)
        else:
            messagebox.showerror("Tipo", "Antes, selecione um tipo de plano!")

    def iniciar_atuado(self):
        """
        Ativa o plano atuado no sistema
        :return:
        """
        self.anim_semaforos.flag_atuado = True

    def coletar_seeder_r1(self):
        """
        Doleta os dados do gerador de veiculos para a rua 1
        :return:
        """
        self.seeder_ns = (int(self.spin_minutos_ns.get()) * 60) / int(self.spin_veiculos_ns.get())

    def coletar_seeder_r2(self):
        """
        Coleta os dados do gerador de veiculos para a rua 2
        :return:
        """
        self.seeder_ol = (int(self.spin_minutos_ol.get()) * 60) / int(self.spin_veiculos_ol.get())

    def evento_scroll_bar(self, event):
        """
        Gerencia o evento de Mouse Wheel na imagem do mapa
        :param event: gerador do evento
        :return:
        """
        direction = 0
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:   # sobe a imagem (evento num 5 no linux ou delta -120 no windows)
            direction = 1
        if event.num == 4 or event.delta == 120:    # desce a imagem
            direction = -1
        self.canvas.yview_scroll(direction, "units")

    def seeder_veiculos(self):
        """
        Gera veículos no sistema periodicamente, de acordo com os valores de entrada
        :return:
        """
        seeder_ns = 0
        seeder_ol = 0

        while True:

            if seeder_ns == 0:

                seeder_ns = self.seeder_ns
                self.inserir_veiculo_vertical()

            else:
                seeder_ns -= 1

            if seeder_ol == 0:
                seeder_ol = self.seeder_ol
                self.inserir_veiculo_horizontal()

            else:
                seeder_ol -= 1

            time.sleep(1)

    def inserir_veiculo_vertical(self):
        """
        Insere veículos na via Norte<->Sul
        :return:
        """

        sentidos = ['ns', 'sn']

        # O sentido (Norte->Sul ou Sul-> Norte) e a velocidade (20, 30 ou 40km/h) são aleatórios
        sentido = random.randint(0, 1)
        velocidade = random.randint(0, 2)

        if sentidos[sentido] == 'ns':

            # Verifica se não a via não está cheia, ou seja, se houver veículo na última posição da via,
            # cancela a inserção e acelera a geração de um novo veículo, para que seja adicionado a via o mais
            # rápido possível
            for veiculo in self.veiculos_ns:

                if veiculo.pos_atual[1] <= self.i_r1[1] + Veiculo().comprimento + Rua().metro:
                    self.incrementar_contador('imp_ns', "Impedidos")
                    return

            veiculo = Veiculo(self.i_r1[0],
                              self.i_r1[1],
                              self.i_r1[0],
                              self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento,
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_vertical(self.canvas, self.i_r1[0], self.i_r1[1])
            self.veiculos_ns.append(veiculo)
            self.incrementar_contador('ger_ns', "Gerados")
            self.incrementar_contador('total', "Total")

        elif sentidos[sentido] == 'sn':

            for veiculo in self.veiculos_sn:

                if veiculo.pos_atual[1] + Veiculo().comprimento + Rua().metro \
                        >= self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento:
                    self.incrementar_contador('imp_sn', "Impedidos")
                    return

            veiculo = Veiculo(self.i_r1[0] + Rua().largura - 16,
                              self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento,
                              self.i_r1[0] + Rua().largura - 16,
                              self.i_r1[1],
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_vertical(self.canvas, self.i_r1[0] + Rua().largura - 16,
                                       self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento)
            self.veiculos_sn.append(veiculo)
            self.incrementar_contador("ger_sn", "Gerados")
            self.incrementar_contador('total', "Total")

    def inserir_veiculo_horizontal(self):
        """
        Insere veículos na via Oeste<->Leste
        :return:
        """

        sentidos = ['ol', 'lo']

        # O sentido (Norte->Sul ou Sul-> Norte) e a velocidade (20, 30 ou 40km/h) são aleatórios
        sentido = random.randint(0, 1)
        velocidade = random.randint(0, 2)

        if sentidos[sentido] == 'ol':

            # Verifica se não a via não está cheia, ou seja, se houver veículo na última posição da via,
            # cancela a inserção de um novo
            for veiculo in self.veiculos_ol:

                if veiculo.pos_atual[0] <= self.i_r2[0] + Veiculo().comprimento + Rua().metro:
                    self.incrementar_contador('imp_ol', "Impedidos")
                    return

            veiculo = Veiculo(self.i_r2[0],
                              self.i_r2[1] + 48,
                              self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                              self.i_r2[1] + 48,
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_horizontal(self.canvas, self.i_r2[0], self.i_r2[1] + 48)
            self.veiculos_ol.append(veiculo)
            self.incrementar_contador('ger_ol', "Gerados")
            self.incrementar_contador('total', "Total")

        elif sentidos[sentido] == 'lo':

            for veiculo in self.veiculos_lo:

                if veiculo.pos_atual[0] + Veiculo().comprimento + Rua().metro \
                        >= self.i_r1[0] + Rua().comprimento + Rua().largura + Rua().comprimento + Veiculo().comprimento:
                    self.incrementar_contador('imp_lo', "Impedidos")
                    return

            veiculo = Veiculo(self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                              self.i_r2[1],
                              self.i_r2[0],
                              self.i_r2[1],
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_horizontal(self.canvas,
                                         self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                                         self.i_r2[1])
            self.veiculos_lo.append(veiculo)
            self.incrementar_contador('ger_lo', "Gerados")
            self.incrementar_contador('total', "Total")

    def incrementar_contador(self, tag_contador: str, texto: str):
        """
        Incrementa os diversos contadores do sistema em 1
        :param tag_contador: nome do contador em questão
        :param texto: texto complementar
        :return:
        """

        contador = (self.canvas.itemcget(tag_contador, 'text').split(" "))[1]
        contador = int(contador) + 1
        self.canvas.itemconfig(tag_contador, text=texto + ": " + str(contador))

    def iniciar_app(self):
        """
        Inicia a aplicação
        :return:
        """
        self.root.minsize(600, 640)
        self.root.mainloop()

iniciar = Principal()
iniciar.iniciar_app()
