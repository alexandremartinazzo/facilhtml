#!/usr/bin/env python

# Arquivo editor.py

import pygtk
pygtk.require('2.0')
import gtk
import htmlrender
import pango
import sys
#import HTMLParser
import tela

class Editor:
    '''
    Componente para implementar a l�gica de neg�cios do FACIL
    '''
    
    # Definições de variáveis internas e formatação
    
    #__buffer = None
    #__view = None
    #__html = None
        
    # Aqui definimos as tags alinhadas:
    __inline = [ "b", "i", "strong", "u" ]

    # Aqui definimos as tags que geram seus próprios blocos:
    __block = [ "h1", "h2", "h3", "h4", "p", "dl", "dt", "dd" ]

    # Aqui algumas tags que não vamos renderizar:
    __ignore = [ "body", "html", "div" ]

    # Aqui algumas tags que geralmente são deixadas abertas:
    __open = [ "dt", "dd", "p" ]

    # Formatos e fontes aplicadas às tags
    __formats = {
         'h1': { 'size-points': 24,
                 #'justification': gtk.JUSTIFY_CENTER,
                 'weight': pango.WEIGHT_BOLD,
                 'pixels-above-lines': 8,
                 'pixels-below-lines': 4 },
         'h2': { 'size-points': 18,
                 #'justification': gtk.JUSTIFY_CENTER,
                 'weight': pango.WEIGHT_BOLD,
                 'pixels-above-lines': 6,
                 'pixels-below-lines': 3 },
         'h3': { 'size-points': 14,
                 'weight': pango.WEIGHT_BOLD,
                 'pixels-above-lines': 4,
                 'pixels-below-lines': 0 },
         
         # definido por mim
         'h4': { 'size-points': 12,
                 'weight': pango.WEIGHT_BOLD,
                 'pixels-above-lines': 0,
                 'pixels-below-lines': 0 },
         
         # tags de uso interno
         'tamanho1': { 'size-points': 24 },
         'tamanho2': { 'size-points': 18 },
         'tamanho3': { 'size-points': 14 },
         'tamanho4': { 'size-points': 12 },
         'center':   { 'justification': gtk.JUSTIFY_CENTER },
         'right':    { 'justification': gtk.JUSTIFY_RIGHT },
         'left':     { 'justification': gtk.JUSTIFY_LEFT },
         # a cor de fundo não usa tag
         #'background': {#'background-full-height-set': True,
         #               'paragraph-background': 'white'},
         
         # o foreground não pode ficar em uma tag única
         #'foreground': {'foreground': 'black'},
         
         'a':    { 'foreground':   'blue',
                   'underline':    pango.UNDERLINE_SINGLE },
         
         'dl': { 'font': "sans 10" },
         'dd': { 'font': "sans 10",
                 'left-margin': 10, 'right-margin': 10,
                 'pixels-above-lines': 2,
                 'pixels-below-lines': 2 },
         'dt': { 'font': "sans bold 10",
                 'pixels-above-lines': 3,
                 'pixels-below-lines': 2 },
         'p': { 'font': "sans 10",
                'pixels-above-lines': 4,
                'pixels-below-lines': 4 },
         'b': { 'weight': pango.WEIGHT_BOLD },
         'i': { 'style': pango.STYLE_ITALIC },
         'strong': { 'weight': pango.WEIGHT_BOLD ,
                     'style': pango.STYLE_ITALIC }, 
                    
         'u': { 'underline': pango.UNDERLINE_SINGLE },
         'code': { 'font': "monospace 10" }
    }
        
    def __init__(self, textbuffer=None):
        # acertar chamadas!!!
        # componentes não conseguem conversar entre si!!!
        # trazer o buffer da interface
        self.__render = htmlrender.HTMLRender(self.__formats)
        
        
        interface = tela.Tela(self, self.__render)
        self.__buffer = interface.get_buffer()
        self.__view = interface.get_view()
        
                
        # Iniciando tags
        #for tag in self.__formats:
        #    self.__buffer.create_tag(tag, **self.__formats[tag])
        
        interface.run()
        
        #######################################################################
        # definições trazidas do arquivo "htmlrender.py"
        # acho que não vou usar...
        
    def set_text(self, txt):
        self.feed(txt)


    def handle_starttag(self, tag, attr):
        # Se a tag deve ser ignorada, nada deve ser feito. 
        if tag in self.__ignore:
            pass
        # Se a tag deve criar um bloco, adicionamos uma quebra de
        # linha ao parágrafo, para simular o efeito de blocagem.
        # Adicionalmente, blocos 'fecham' tags previamente abertas.
        elif tag in self.__block:
            if self.__last in self.__open:
                self.handle_endtag(self.__last)
            self.__last = tag
            end_iter = self.__tb.get_end_iter()
            self.__tb.insert(end_iter, "\n")

        # Marcamos a posição da tag para posterior aplicação da
        # formatação.
        end_iter = self.__tb.get_end_iter()
        mark = self.__tb.create_mark(None, end_iter, True)
        if tag in self.__tags:
            self.__tags[tag].append(mark)
        else:
            self.__tags[tag] = [ mark ]


    def handle_data(self, data):
        data = ' '.join(data.split()) + ' '
        end_iter = self.__tb.get_end_iter()
        self.__tb.insert(end_iter, data)
        

    def handle_endtag(self, tag):
        try:
            if tag not in self.__ignore:
                start_mark = self.__tags[tag].pop()
                start = self.__tb.get_iter_at_mark(start_mark)
                end = self.__tb.get_end_iter()
                self.__tb.apply_tag_by_name(tag, start, end)
                return
        except KeyError:
            pass

        
        # final das definições do arquivo "htmlrender.py"
        #######################################################################
    
    def italico(self, data=None):
        '''
        Função para aplicar formata��o "it�lico" em um texto
        Se o texto j� tiver essa formata��o, o m�todo deve retir�-la
        '''
        print "Método: Editor.italico(self, data)"
        start, end = self.__buffer.get_selection_bounds()
        tag = self.__buffer.get_tag_table().lookup('i')
        # Se a tag itálico já estiver aplicada, deve ser retirada
        if start.has_tag(tag) == True:
            self.__buffer.remove_tag(tag, start, end)
        else:
            self.__buffer.apply_tag(tag, start, end)
        
    def negrito(self, data=None):
        '''
        Função para aplicar formata��o "negrito" em um texto
        Se o texto j� tiver essa formata��o, o m�todo deve retir�-la
        '''
        print "Método: Editor.negrito(self, data)"
        
        tag = self.__buffer.get_tag_table().lookup('b')
        try:
            # Aplica formatação em porção de texto selecionado
            start, end = self.__buffer.get_selection_bounds()
            # Se a tag negrito já estiver aplicada, deve ser retirada
            print 'texto selecionado\n'
            if start.has_tag(tag) == True:
                self.__buffer.remove_tag(tag, start, end)
            else:
                self.__buffer.apply_tag(tag, start, end)
        except:
            # Aplica formatação no texto a ser digitado, não funciona!!!
            print 'não há texto selecionado'
            mark = self.__buffer.get_mark('insert')
            iter = self.__buffer.get_iter_at_mark(mark)
            #iter = self.__buffer.get_property('cursor-position')
            self.__buffer.apply_tag(tag, iter, iter)
        
    def sublinhado(self, data=None):
        '''
        Função para aplicar formataçãoo "sublinhado" em um texto
        Se o texto já tiver essa formataçãoo, o método deve retirá-la
        '''
        print "Método: Editor.negrito(self, data)"
        
        tag = self.__buffer.get_tag_table().lookup('u')
        try:
            # Aplica formatação em porção de texto selecionado
            start, end = self.__buffer.get_selection_bounds()
            # Se a tag negrito já estiver aplicada, deve ser retirada
            print 'texto selecionado\n'
            if start.has_tag(tag) == True:
                self.__buffer.remove_tag(tag, start, end)
            else:
                self.__buffer.apply_tag(tag, start, end)
        except:
            pass

    def fonte(self, tamanho=None, cor=None):
        '''
        Função para aplicar tamanho e cor em um texto
        '''
        print "Método: Editor.fonte(self, tamanho, cor)"
        
        tags = ['tamanho1', 'tamanho2', 'tamanho3', 'tamanho4']
#===============================================================================
#        
#        tag1 = self.__buffer.get_tag_table().lookup('tamanho1')
#        tag2 = self.__buffer.get_tag_table().lookup('tamanho2')
#        tag3 = self.__buffer.get_tag_table().lookup('tamanho3')
#        tag4 = self.__buffer.get_tag_table().lookup('tamanho4')
#        
#===============================================================================
        start, end = self.__buffer.get_selection_bounds()
        
        
        # se não tiver o tag, remove os outros e aplica o certo... será?
        if tamanho != None:
            tag = self.__buffer.get_tag_table().lookup(tamanho)
            if start.has_tag(tag) == False:
                for teste in tags:
                    self.__buffer.remove_tag_by_name(teste, start, end)
                self.__buffer.apply_tag(tag, start, end)
#===============================================================================
#        
#        if tamanho == 'tamanho1':
#            self.__buffer.apply_tag_by_name('t1', start, end)
#        elif tamanho == 'tamanho2':
#            self.__buffer.apply_tag_by_name('t2', start, end)
#        elif tamanho == 'tamanho3':
#            self.__buffer.apply_tag_by_name('t3', start, end)
#        elif tamanho == 'tamanho4':
#            self.__buffer.apply_tag_by_name('t4', start, end)
#            print 'aplicou'
#        
#===============================================================================
        if cor != None:
            print 'editor', cor
            #tag = self.__buffer.get_tag_table().lookup('foreground')
            tag = self.__buffer.create_tag()
            tag.set_property('foreground-gdk', cor)
            self.__buffer.apply_tag(tag, start, end)
        
    def alinhamento(self, alinhamento=None):
        '''
        Função para aplicar alinhamento (esquerda, centro, direita) em um texto
        '''
        print "Método: Editor.alinhamento(self, alinhamento)"
        
        tags = ['center', 'right', 'left']
        
        try:
            start, end = self.__buffer.get_selection_bounds()
            linha = start.get_line()
            iter = self.__buffer.get_iter_at_line(linha)
        except:
            # se não tiver texto selecionado, atua na linha do cursor
            # não funciona no caso em que o cursor está no começo da linha!!!
            mark = self.__buffer.get_mark('insert')
            end = self.__buffer.get_iter_at_mark(mark)
            linha = end.get_line()
            iter = self.__buffer.get_iter_at_line(linha)
        
        
        
        #if iter.has_tag(self.__buffer.get_tag_table().lookup(alinhamento)) == False:
        for tipo in tags:
           self.__buffer.remove_tag_by_name(tipo, iter, end)
        self.__buffer.apply_tag_by_name(alinhamento, iter, end)
        
    def cor_de_fundo(self, cor=None):
        '''
        Função para aplicar cor de fundo (background color)
        '''
        print "Método: Editor.cor_de_fundo(self, cor)"
        # @cor deve ser um objeto gtk.gdk.Color
        #print 'editor', cor
        self.__view.modify_base(gtk.STATE_NORMAL, cor)
        
        
    def ajuda(self):
        '''
        Função para exibir a p�gina de ajuda do programa
        '''
        print "Método: Editor.ajuda(self)"
    
    def abrir_arquivo(self, caminho=None):
        '''
        Função para aplicar abrir arquivos j� existentes
        '''
        print "Método: Editor.abrir_arquivo(self, data)"
        self.__html = open(caminho).read()
        
        self.__buffer.set_text('')
        self.__render.set_text(self.__html)
                
    def salvar_arquivo(self, data=None):
        '''
        Função para aplicar salvar um arquivo aberto
        '''
        print "Método: Editor.salvar_arquivo(self, data)"
        try:
            import cPickle
            f = file('tentativa.txt', 'w')
            cPickle.dump(self.__view, f)
            f.close
        except:
            pass
        start= self.__buffer.get_start_iter()
        end = self.__buffer.get_end_iter()
        print self.__buffer.get_text(start, end)
        
        
        
    def inserir_link(self, link=None):
        '''
        Função para inserir uma liga��o (link) dentro do arquivo em edi��o
        '''
        print "Método: Editor.inserir_link(self, link=None)"
        
    def inserir_imagem(self, arquivo=None):
        '''
        Função para inserir uma imagem dentro do arquivo em edi��o
        '''
        print "Método: Editor.inserir_imagem(self, data) "
        
        #textbuffer = render.get_buffer()
        mark = self.__buffer.get_mark('insert')
        iter = self.__buffer.get_iter_at_mark(mark)
        #iter = self.__buffer.get_iter_at_offset(0)
        if arquivo == None:
            pixbuf = gtk.gdk.pixbuf_new_from_file("pixmaps/button1_peq.png")
        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file(arquivo)
        self.__buffer.insert_pixbuf(iter, pixbuf)
        
    def inserir_tabela(self, linhas=0, colunas=0):
        '''
        Função para inserir uma tabela dentro do arquivo em edi��o
        '''
        print "Método: Editor.inserir_tabela(self, linhas, colunas)"
        
    def novo_arquivo(self):
        '''
        Função para inserir uma imagem dentro do arquivo em edi��o
        '''
        print "Método: Editor.novo_arquivo(self)"
        
        
        
    def fechar_programa(self):
        '''
        Função para fechar o programa
        '''
        print "Método: Editor.fechar_programa(self)"
        # essa fun��o � necess�ria? acho que n�o...
    

if __name__ == "__main__":
    editor = Editor()
    #consertar!!!!!
    print 'argumentos:', sys.argv[0], sys.argv[1]
    if sys.argv != None:
        editor.abrir_arquivo(sys.argv[1])
    
