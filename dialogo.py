# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk

class Arquivo:

    __retorno = None
    
    def response_event(self, widget, data):
        #print widget, data
        if data == gtk.RESPONSE_OK:
            print 'arquivo selecionado:', "%s" % self.janela.get_filename()
            self.__retorno = self.janela.get_filename()
        elif data == gtk.RESPONSE_CANCEL:
            print 'cancelando operação'
            self.__retorno = None
        
    def run(self):
        self.janela.run()
        return self.__retorno
    
    def destroy(self):
        self.janela.destroy()
    
    def __init__(self, parent, titulo_filtro=None, *mime):
        
        self.janela = gtk.FileChooserDialog("Selecionar Arquivo",
                                            parent,
                                            gtk.FILE_CHOOSER_ACTION_OPEN)
            
        # Usa os botões padrão do GTK, e define um identificador para
        # reconhecer no tratamento do evento "response"
        self.janela.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OK,     gtk.RESPONSE_OK)
        
        # preciso descobrir como abrir arquivos em localizações remotas
        #if self.janela.get_property('local-only') == True:
        #    self.janela.set_property('local-only', False)
        
        # adiciona um filtro para abertura de arquivos
        if mime != None:
            filtro = gtk.FileFilter()
            filtro.set_name(titulo_filtro)
        
            for tipo in mime:
                filtro.add_pattern(tipo)
            self.janela.add_filter(filtro)
        
        self.janela.connect('response', self.response_event)
    
class Salvar:
    
    
    
    def __init__(self, parent):
                
        self.janela = gtk.FileChooserDialog("Selecionar Arquivo",
                                            parent,
                                            gtk.FILE_CHOOSER_ACTION_SAVE)
            
        # Usa os botões padrão do GTK, e define um identificador para
        # reconhecer no tratamento do evento "response"
        self.janela.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_SAVE,   gtk.RESPONSE_OK)
        
        # ainda não sei como fazer, mas seria bom adicionar algum filtro
        # para permitir abertura de HTML somente
        
        self.janela.connect('response', self.response_event)

class Cor:
    
    __retorno = None
    
    def click_event(self, widget, data='ok'):
        #print data
        if data == 'ok':
            self.__retorno = self.janela.colorsel.get_current_color()
            #print self.__retorno
            
    def run(self):
        self.janela.run()
        return self.__retorno
    
    def destroy(self):
        self.janela.destroy()
    
    def __init__(self, parent):
        self.janela = gtk.ColorSelectionDialog('Selecione uma cor')
        # Usa os botões padrão do GTK, e define um identificador para
        # reconhecer no tratamento do evento "response"
        #self.janela.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
        #                        gtk.STOCK_SAVE,   gtk.RESPONSE_OK)
        
        self.janela.ok_button.connect('clicked', self.click_event)
        
    
