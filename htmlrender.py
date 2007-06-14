#!python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import pango
from HTMLParser import HTMLParser

class HTMLRender(gtk.TextView, HTMLParser):

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
         #'b': { 'font': "sans bold 10", },
         'i': { 'style': pango.STYLE_ITALIC },
         #'i': { 'font': "sans italic 10", },
         'strong': { 'font': "sans bold italic 10" },
         'u': { 'underline': pango.UNDERLINE_SINGLE },
         'code': { 'font': "monospace 10" }
    }

    def __init__(self, formatos=None, *cnf, **kw):
        """
        Inicializamos o HTMLParser e o TextView. O TextView deve
        ser configurado não editável e com 'word-wraping', ou seja
        com quebra de linha nos limites de palavras. A formatação
        das tags também é inicializada. O dicionário __tags contém
        uma lista das tags presentes no texto e suas posições, para
        podermos alocar as formatações.
        """
        gtk.TextView.__init__(self, *cnf, **kw)
        HTMLParser.__init__(self)
        #self.set_editable(True)
        #self.set_wrap_mode(gtk.WRAP_WORD)
        self.__tb = self.get_buffer()
        self.__last = None
        self.__tags = { }
        
        if formatos != None:
            self.__formats = formatos
        for tag in self.__formats:
            self.__tb.create_tag(tag, **self.__formats[tag])
        #print "imprimindo...\n", self.get_starttag_text()


    def set_text(self, txt):
        """
        O widget TextView do PyGTK é desnecessariamente complicado.
        Para a inserção de texto, é necessário indicar um buffer de
        texto; para formatar o texto, é preciso encontrar marcas e
        tags no texto, etc. Para simplificar, este método alimenta o
        texto ao parser HTML que faz a formatação automaticamente.
        O nome é para seguir a aparente convenção de nomes do PyGTK.
        """
        self.feed(txt)


    def handle_starttag(self, tag, attr):
        """
        Aqui manipulamos a abertura das tags. Ao ser aberta, a tag
        tem sua posição registrada, para que a formatação seja a-
        plicada posteriormente, no fechamento.
        """
        print 'handle_starttag:', '"',tag,'"', 'atributos:', attr
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
        """
        Este método recebe os dados de uma tag, que, tipicamente,
        é texto a ser renderizado. Simplesmente inserimos o texto
        na widget. No entanto, os renderizadores de HTML devem
        tratar espaços contíguos e caracteres de tabulação e quebra
        de página como um simples espaço em branco. Na primeira
        linha nós fazemos esse serviço.
        """
        print 'handle_data', data
        
        data = ' '.join(data.split()) + ' '
        end_iter = self.__tb.get_end_iter()
        self.__tb.insert(end_iter, data)
        

    def handle_endtag(self, tag):
        """
        Aqui as tags são fechadas. Suas posições são encontradas
        e as formatações são aplicadas. O processo consiste em
        recuperar a posição inicial em que a formatação deve ser
        aplicada (obtida em handle_starttag), obter a posição
        atual (após o texto ter sido inserido em handle_data),
        inserir os marcadores do Text e aplicar a formatação. O
        processo é extremamente simples.
        """ 
        try:
            if tag not in self.__ignore:
                start_mark = self.__tags[tag].pop()
                start = self.__tb.get_iter_at_mark(start_mark)
                end = self.__tb.get_end_iter()
                
                #if tag == 'a':
                #    print 'achou tag a!'
                #    #link = gtk.TextTag()
                #    link = self.__tb.create_tag()
                #    
                #    link.set_property('underline', pango.UNDERLINE_SINGLE)
                #    link.set_property('foreground', 'blue')
                #    self.__tb.apply_tag(link, start, end)
                #else:
                #    self.__tb.apply_tag_by_name(tag, start, end)
                self.__tb.apply_tag_by_name(tag, start, end)
                return
        except KeyError:
            print 'erro em handle_endtag'
            pass
        
    def handle_entityref(self, name):
        print 'handle_entityref', name
        
    # pode ser retirado!!!
    def italico(self, data):
        '''
        Aplica formatação itálico em um texto selecionado
        '''
        start, end = self.__tb.get_selection_bounds()
        tag = self.__tb.get_tag_table().lookup('i')
        # Se a tag itálico já estiver aplicada, deve ser retirada
        if start.has_tag(tag) == True:
            self.__tb.remove_tag(tag, start, end)
        else:
            self.__tb.apply_tag(tag, start, end)
        
        # Por algum motivo, a formatação não é aplicada dependendo
        # da forma que se seleciona o texto
        # SOLUÇÃO: procurar a tag somente no começo do texto!
    
    # pode ser retirado!!!
    def negrito(self, data):
        start, end = self.__tb.get_selection_bounds()
        tag = self.__tb.get_tag_table().lookup('b')
        # Se a tag itálico já estiver aplicada, deve ser retirada
        if start.has_tag(tag) == True:
            self.__tb.remove_tag(tag, start, end)
        else:
            self.__tb.apply_tag(tag, start, end)
    
if __name__ == "__main__":
    q = gtk.Window()           # Criamos a janela
    box= gtk.VBox()

    t = HTMLRender()                  # Criamos o renderizador
    s = open("teste/samples/simples.html").read() # O texto precisa ser UTF-8!!!
    #print s
    t.set_text(s)
    t.show()

    sb = gtk.ScrolledWindow()  # Criamos um visualizador com barra de rolagem...
    sb.add(t)                  # e adicionamos o texto
    
    sb.show()
    box.pack_start(sb)
    
    
    lista = {1:"itálico", 2: "negrito", 3: "centro", 4:"esq", 5: "dir",
             7: "cor texto", 8: "T1", 9: "T2", 10: "T3", 11: 'T4', 
             12: 'cor fundo' }
    
    botao1 = gtk.Button('itálico')
    box.pack_end(botao1, False, False, 0)
    botao1.connect("clicked", t.italico)
    botao1.show()
    
    botao2 = gtk.Button('negrito')
    box.pack_end(botao2, False, False, 0)
    botao2.show()
    box.show()
    botao2.connect("clicked", t.negrito)
    
        
    q.connect("destroy", gtk.main_quit)    
    q.set_default_size(640,480)
    q.add(box)                  # Por fim, vamos para o loop principal.
    q.show()
    gtk.main()
