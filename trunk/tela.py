#!/usr/bin/env python

# Arquivo tela.py
# Contém as declarações do componente Tela

import pygtk
pygtk.require('2.0')
import gtk
import dialogo

#import editor as classe_editor

# Definição dos tipos MIME para inserir imagens. Vide Tela.mensagem()
# não funciona direito!!!
MIME_IMAGEM = ['*.jpg', '*.jpeg', '*.gif', '*.png']

# número de botões total e na barra horizontal
N_BOTOES = 20
N_BOTOES_H = 12

class Tela:
    '''
    Componente para implementar a interface gráfica do FACIL
    '''
        
    __dicas = {1: 'itálico',    2: 'negrito',    3: 'tamanho 1',    4: 'tamanho 2',
               5: 'tamanho 3', 6: 'tamanho 4', 7: 'esquerda', 8: 'direita', 
               9: 'centralizado', 10: 'cor do texto', 11: 'cor de fundo', 
               12: 'ajuda', 13: 'abrir arquivo', 14: 'salvar arquivo', 
               15: 'inserir link', 16: 'inserir imagem', 
               17: 'inserir tabela', 18: 'criar um novo arquivo', 
               19: 'sair', 20: 'sublinhado'
               }
    
    def clique_botao(self, widget, data=None):
        '''
        Função única para tratar do evento clicked em todos os botões
        Cada um dos botões deve estar associado a um identificador único
        para que sua funcionalidade dele executada corretamente (será?)
        '''
        print "botão %s clicado!" % data
        
        # Botões para formatação de texto e afins
        if data == 1:
            # chama o método da classe Editor associado ao botao1
            # aplica ITALICO
            print "chamando o método para o botão %d" % data
            self.__editor.italico("texto selecionado")
            
        elif data == 2:
            # chama o método da classe Editor associado ao botao2
            # aplica NEGRITO
            print "chamando o método para o botão %d" % data
            self.__editor.negrito("texto selecionado")
            
        elif data == 3:
            # chama o método da classe Editor associado ao botao3
            # aplica tamanho T1 no texto
            print "chamando o método para o botão %d" % data
            self.__editor.fonte("tamanho1")
            
        elif data == 4:
            # chama o método da classe Editor associado ao botao4
            # aplica tamanho T2 no texto
            print "chamando o método para o botão %d" % data
            self.__editor.fonte("tamanho2")
            
        elif data == 5:
            # chama o método da classe Editor associado ao botao5
            # aplica tamanho T3 no texto
            print "chamando o método para o botão %d" % data
            self.__editor.fonte("tamanho3")
            
        elif data == 6:
            # chama o método da classe Editor associado ao botao6
            # aplica tamanho T4 no texto
            print "chamando o método para o botão %d" % data
            self.__editor.fonte("tamanho4")
            
        elif data == 7:
            # chama o método da classe Editor associado ao botao7
            # aplica alinhamento à ESQUERDA
            print "chamando o método para o botão %d" % data
            self.__editor.alinhamento("left")
            
        elif data == 8:
            # chama o método da classe Editor associado ao botao8
            # aplica alinhamento à DIREITA
            print "chamando o método para o botão %d" % data
            self.__editor.alinhamento("right")
            
        elif data == 9:
            # chama o método da classe Editor associado ao botao9
            # aplica alinhamento CENTRALIZADO
            print "chamando o método para o botão %d" % data
            self.__editor.alinhamento("center")
            
        elif data == 10:
            # chama o método da classe Editor associado ao botao10
            # aplica a nova COR DE TEXTO escolhida pelo usuário
            print "chamando o método para o botão %d" % data
            cor = self.mensagem('cor')
            #print 'botão cor de texto', cor
            self.__editor.fonte(None, cor)
            
        elif data == 11:
            # chama o método da classe Editor associado ao botao11
            # aplica a nova COR DE FUNDO escolhida pelo usuário
            print "chamando o método para o botão %d" % data
            cor = self.mensagem('cor')
            #print 'botão cor de fundo', cor
            #cor = gtk.gdk.color_parse('red')
            self.__editor.cor_de_fundo(cor)
            
        # Botões de funcionalidades externas
        # Pertencem à barra de ferramentas vertical
        elif data == 12:
            # chama o método da classe Editor associado ao botao12
            # exibe a AJUDA do programa
            print "chamando o método para o botão %d" % data
            self.__editor.ajuda()
            
        elif data == 13:
            # chama o método da classe Editor associado ao botao13
            # ABRE um ARQUIVO para edição
            print "chamando o método para o botão %d" % data
            caminho = self.mensagem('abrir_arquivo')
            if caminho:
                self.__editor.abrir_arquivo(caminho)
            else:
                print 'não abriu nada!'
            
            
        elif data == 14:
            # chama o método da classe Editor associado ao botao14
            # SALVA um ARQUIVO em edição
            print "chamando o método para o botão %d" % data
            self.__editor.salvar_arquivo("caminho_do_arquivo")
            
        elif data == 15:
            # chama o método da classe Editor associado ao botao15
            # INSERE um LINK
            print "chamando o método para o botão %d" % data
            self.__editor.inserir_link("endereço_do_link")
            
        elif data == 16:
            # chama o método da classe Editor associado ao botao16
            # INSERE uma IMAGEM externa
            print "chamando o método para o botão %d" % data
            caminho = self.mensagem('abrir_imagem')
            if caminho != None:
                self.__editor.inserir_imagem(caminho)
            #classe_editor.Editor().inserir_imagem()
            
        elif data == 17:
            # chama o método da classe Editor associado ao botao17
            # INSERE uma TABELA
            print "chamando o método para o botão %d" % data
            self.__editor.inserir_tabela("linhas", "colunas")
            
        elif data == 18:
            # chama o método da classe Editor associado ao botao18
            # cria um NOVO ARQUIVO
            print "chamando o método para o botão %d" % data
            self.__editor.novo_arquivo()
            
        elif data == 19:
            # chama o método da classe Editor associado ao botao19
            # fecha o FACIL
            # obs.: não sei se este botão será necessário
            print "chamando o método para o botão %d" % data
            gtk.main_quit()
            
        # acrescentado em 24/10/2006
        elif data == 20:
            self.__editor.sublinhado()
            
        else:
            print "excedeu o número de botões!"
            
    def aumenta_imagem(self, widget, data=None):
        '''
        Troca a imagem de um botão por uma de tamanho maior
        Chamada pelo envento "enter" dos botões
        '''
        widget.set_label(self.__dicas[data])
        return
        
        imagem = gtk.Image()
        # carrega a imagem no diretório 'pixmaps'
        nome = "pixmaps/button%s_gde.png" % repr(data) 
        imagem.set_from_file(nome)
        widget.set_image(imagem)


    def diminui_imagem(self, widget, data=None):
        '''
        Troca a imagem de um botão por uma de tamanho menor
        Chamada pelo envento "leave" dos botões
        '''
        widget.set_label('')
        return
        
        imagem = gtk.Image()
        # carrega a imagem no diretório 'pixmaps'
        nome = "pixmaps/button%s_peq.png" % repr(data) 
        imagem.set_from_file(nome)
        widget.set_image(imagem)

    
    def __init__(self, editor=None, render=None):
        ''' Contrução da interface gráfica'''
        
        #print editor
        self.__editor = editor
        
        
        # Janela
        self.__window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.__window.set_resizable(True)  
        self.__window.connect("destroy", gtk.main_quit)
        self.__window.set_title("FACIL")
        self.__window.set_border_width(0)
        #self.__window.set_resizable(False)
        #self.__window.set_decorated(False)
        self.__window.set_default_size(600,450)
        
        # Encapsulamento por containers
        # árvore dos widgets:
        # window
        #    vbox
        #       (hbox_lateral)
        #           scrolledwindow
        #               textview
        #           (fixed_lateral)
        #               (vbox_lateral)
        #                   (button)
        #       fixed
        #           hbox
        #               button
        # obs.: se houver barra de ferramentas lateral, o widget
        # scrolledwindow deve ser encapsulado em um hbox
        
        vbox = gtk.VBox(False, 0)
        self.__window.add(vbox)
        
        # implementação da barra lateral
        hbox_lateral = gtk.HBox(False, 0)
        
        # Cria uma scrolledwindow para encapsular o texto
        sw = gtk.ScrolledWindow()
        #sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        # funciona melhor com AUTOMATIC na vertical e horizontal
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        if render == None:
            #print 'criando um textview'
            self.textview = gtk.TextView()
        else:
            print 'recebeu um renderizador'
            self.textview = render
                
        
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textview.show()
        
        sw.add(self.textview)
        
        #vbox.pack_start(sw, True, True, 0)
        # implementação da barra lateral:
        #    @vbox encapsula @hbox_lateral
        #    @hbox_lateral encapsula @scrolledwindow e @fixed_lateral
        #    @fixed_lateral encapsula @vbox_lateral, que contém os botões
        
        vbox.pack_start(hbox_lateral, True, True, 0)
        hbox_lateral.pack_start(sw, True, True, 0)
        
        
        fixed_lateral = gtk.Fixed()
        hbox_lateral.pack_end(fixed_lateral, False, False, 0)
        
        vbox_lateral = gtk.VBox()
        fixed_lateral.put(vbox_lateral, 0, 0)
        
        #### pode ser removido!!!
        #b = gtk.Button('teste')
        #vbox_lateral.pack_start(b, False, False, 0)
        #b.show()
        ###
        
        vbox_lateral.show()
        fixed_lateral.show()
        hbox_lateral.show()
        
        # Encapsulamento da barra de ferramentas horizontal
        fixed = gtk.Fixed()
        vbox.pack_end(fixed, False, False, 0)
        
        hbox = gtk.HBox()
        fixed.put(hbox, 0, 0)
        
        # empacota os botões dentro do hbox, total de 11 botões
        for i in range(1, N_BOTOES+1):
            imagem = gtk.Image()
            #nome = "pixmaps/button%s_peq.png" % repr(i)
            nome = "pixmaps/button5_peq.png"
            imagem.set_from_file(nome)
            botao = gtk.Button()
            botao.set_image(imagem)
            botao.set_property("relief", gtk.RELIEF_NONE)
            
            dica = gtk.Tooltips()
            dica.set_tip(botao, self.__dicas[i])
            #botao.set_label(self.__dicas[i])
            
            if i < N_BOTOES_H + 1:
                hbox.pack_start(botao, False, False, 0)
            else:
                vbox_lateral.pack_start(botao, False, False, 0)
                
            botao.show()
            # eventos para conectar
            botao.connect("clicked", self.clique_botao, i)
            botao.connect("enter", self.aumenta_imagem, i)
            botao.connect("leave", self.diminui_imagem, i)
        
            
        
        hbox.show()
        
        fixed.show()
        sw.show()
        vbox.show()
        
        #self.__window.reshow_with_initial_size()
        self.__window.show()
        print self.__window.get_size()
        
        #============================================================
        # testes com o pango no textview
        # não funciona como eu quero!
        #self.textview.create_pango_context()
        #s = open("teste/samples/simples.html").read()
        #text= gtk.TextView()
        #s = "<b><span color='blue'>Atenção</span></b>, Você está "\
        #        "Preste a <b>Apagar</b> um Arquivo <b>Importante</b>!"
        #pango_layout = self.textview.create_pango_layout("")
        #pango_layout.set_markup(s)
        #print pango_layout.get_text()
        #============================================================
        
        #self.editor = classe_editor.Editor()

    def run(self):
        gtk.main()
        return 0
    
    def get_view(self):
        return self.textview
    
    def get_buffer(self):
        return self.textview.get_buffer()
    
    def mensagem(self, tipo=None):
        '''
        Esse método contém toda a interface de janelas de diálogo, escolha
        de arquivo e quaiquer notificações para o usuário
        Um componente externo a esta classe implementa a classe propriamente
        dita, para manter a generalidade
        '''
        if tipo == "abrir_arquivo":
            d = dialogo.Arquivo(self.__window,
                                'Aquivos HTML',
                                '*.htm', '*.html')
        elif tipo == 'abrir_imagem':
            # são aceitos muitos formatos de imagem, ver gtk.gdk.pixbuf_get_formats()
            # a função retorna uma lista de dicionários com os formatos
            d = dialogo.Arquivo(self.__window,
                                'Imagens',
                                '*.jpg', '*.jpeg', '*.gif', '*.png')
                                #MIME_IMAGEM)
        elif tipo == "salvar_arquivo":
            d = dialogo.Salvar(self.__window)
        elif tipo == 'cor':
            d = dialogo.Cor(self.__window)
            
            #d = dialogo.outrotipo()
        retorno = d.run()
        #print retorno
        d.destroy()
        return retorno
        
def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    Tela()
    main()
