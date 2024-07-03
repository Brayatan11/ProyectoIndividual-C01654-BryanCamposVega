# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:42:18 2024

@author: usu
"""

import tkinter as tk
from tkinter import messagebox

class WordleVisual:
    '''
    Inicializa la clase WordleVisual con la ventana principal de la aplicación.

    Parameters
    ----------
    root : Tk
        Ventana principal de la aplicación.
    '''
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Visual")
        self.root.geometry("400x300")

         # Entrada de texto para que el usuario ingrese la palabra
        self.entry = tk.Entry(self.root, font=("Helvetica", 24))
        self.entry.pack(pady=20)

        # Lista de botones que representan las letras
        self.letter_buttons = []
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Crear botones para las letras y añadirlos a la lista
        for i in range(5):
            button = tk.Button(self.frame, text="", width=4, height=2, bg="gray", font=("Helvetica", 24))
            button.grid(row=0, column=i, padx=5)
            button.config(command=lambda b=button: self.change_color(b))
            self.letter_buttons.append(button)

        # Botón para enviar la palabra
        self.submit_button = tk.Button(self.root, text="Enviar", command=self.submit_word)
        self.submit_button.pack(pady=20)

        # Enlazar el evento de liberar una tecla para actualizar los botones
        self.entry.bind("<KeyRelease>", self.update_buttons)
        
        # Variable para indicar si la palabra está lista
        self.word_ready = tk.BooleanVar()
        self.word_ready.set(False)
        
    @property
    def word_ready_status(self):
        return self.word_ready
    
    @word_ready_status.setter
    def word_ready_status(self, value):
        self.word_ready.set(value)

    def change_color(self, button):
        '''
        Cambia el color de un botón en función de su color actual.

        Parameters
        ----------
        button : Button
            El botón cuyo color cambiará.
        '''
        current_color = button.cget("bg")
        if current_color == "gray":
            button.config(bg="yellow")
        elif current_color == "yellow":
            button.config(bg="green")
        else:
            button.config(bg="gray")

    def update_buttons(self, event):
        '''
        Actualiza el texto de los botones en función del texto ingresado.

        Parameters
        ----------
        event : Event
            Evento de tecla liberada.
        '''
        word = self.entry.get().upper()[:5]
        for i in range(5):
            if i < len(word):
                self.letter_buttons[i].config(text=word[i])
            else:
                self.letter_buttons[i].config(text="")

    def submit_word(self):
        '''
        Envía la palabra ingresada y muestra un mensaje con la palabra y sus estados.
        '''
        word = self.get_word()
        estados = self.get_states()
        estados_string = "".join(estados)
        
        self.word_ready.set(True)
        
        messagebox.showinfo("Palabra Enviada", f"Palabra: {''.join(word)}\nEstados: {estados_string}")

    def get_word(self):
        '''
        Obtiene la palabra ingresada a partir de los botones de letras.

        Returns
        -------
        list
            Lista de caracteres de la palabra ingresada.
        '''
        return [btn.cget("text") for btn in self.letter_buttons]

    def get_states(self):
        '''
        Obtiene los estados de las letras a partir de los colores de los botones.

        Returns
        -------
        list
            Lista de estados de las letras (G, Y, ?).
        '''
        colors = [btn.cget("bg") for btn in self.letter_buttons]
        estados = []

        for color in colors:
            if color == 'green':
                estados.append('G')
            elif color == 'yellow':
                estados.append('Y')
            else:
                estados.append('?')
        
        return estados
    
    def get_word_and_states(self):
        '''
        Obtiene la palabra y los estados de las letras.

        Returns
        -------
        tuple
            Palabra y estados como una tupla (word, states).
        '''
        word = ''.join(self.get_word())
        states = ''.join(self.get_states())
        return word, states
    
    def reset_word_ready(self):
        '''
        Restablece la variable word_ready a False.
        '''
        self.word_ready.set(False)

