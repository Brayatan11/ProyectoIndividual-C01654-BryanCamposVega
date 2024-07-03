# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 12:05:17 2024

@author: usu
"""

import re
import string
from collections import defaultdict, Counter
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox

class Juego:
    def __init__(self, list_possible_answers, df_words_5l, visual_app):
        '''
        Inicializa la clase Juego con las respuestas posibles y el DataFrame de
        palabras.

        Parameters
        ----------
        list_possible_answers : list
            Lista de posibles respuestas.
        df_words_5l : DataFrame
            DataFrame con las palabras de 5 letras.
        '''
        self.visual_app = visual_app
        #diccionario de las letras correctas en la palabra
        self.__dict_letters = defaultdict(lambda: None)
        for i in range(5):
            self.__dict_letters[i+1] = None
        
        #lista del abecedario en mayusculas
        self.__possible_letters = list(string.ascii_uppercase)
        #intentos del juego
        self.__max_intentos = 6
        self.__intentos = 0
        # Lista de palabras que son posibles respuestas
        self.__list_possible_answers = list_possible_answers
        
        # Lista de palabras con sus letras separadas por posicion
        self.__df_filtradas = df_words_5l
        
        self.__palabras_filtradas = df_words_5l['word']
        
        #Diccionario de letras mal posicionadas en la palabra.
        self.__dict_misplaced_letters = Counter()

    @property
    def dict_letters(self):
        return self.__dict_letters
    
    @dict_letters.setter
    def dict_letters(self, value):
        self.__dict_letters = value

    @property
    def possible_letters(self):
        return self.__possible_letters
    
    @possible_letters.setter
    def possible_letters(self, value):
        self.__possible_letters = value

    @property
    def max_intentos(self):
        return self.__max_intentos
    
    @max_intentos.setter
    def max_intentos(self, value):
        self.__max_intentos = value

    @property
    def intentos(self):
        return self.__intentos
    
    @intentos.setter
    def intentos(self, value):
        self.__intentos = value

    @property
    def list_possible_answers(self):
        return self.__list_possible_answers
    
    @list_possible_answers.setter
    def list_possible_answers(self, value):
        self.__list_possible_answers = value

    @property
    def df_filtradas(self):
        return self.__df_filtradas
    
    @df_filtradas.setter
    def df_filtradas(self, value):
        self.__df_filtradas = value

    @property
    def palabras_filtradas(self):
        return self.__palabras_filtradas
    
    @palabras_filtradas.setter
    def palabras_filtradas(self, value):
        self.__palabras_filtradas = value

    @property
    def dict_misplaced_letters(self):
        return self.__dict_misplaced_letters
    
    @dict_misplaced_letters.setter
    def dict_misplaced_letters(self, value):
        self.__dict_misplaced_letters = value

    def check_misplaced_letters(self, word: str) -> bool:
        '''
        Revisa las letras que están en las palabras pero no están en la posición
        correcta.

        Parameters
        ----------
        word : string
            Palabra que estamos revisando sus letras mal posicionadas
        Returns
        ----------
        valid: Devuelve un booleano si la palabra está correctamente
        '''
        
        word = re.sub(r'[^A-Z]', '', word.upper())
        assert len(word) == 5, 'Word must be 5 characters long'
        
        # Separar en las letras
        list_word = list(word)
        
        # Devuelve indices de la posicion de las letras aun no resueltas
        not_solved = [key for key, value in self.dict_letters.items() if value is None]
        
        # Filtra para palabras aun no resueltas
        list_word_unsolved = [list_word[i-1] for i in not_solved]
        
        # Cuentra la lista de palabras no resueltas
        dict_count_letters = Counter(list_word_unsolved)
        
        # Compara con el diccionario de letras aun no resueltas
        valid = True
        for check_key, check_value in self.dict_misplaced_letters.items():
            if dict_count_letters[check_key] < check_value:
                valid = False
                
        return valid

    def calcular_probabilidad_palabra(self, palabra, probabilidades_todas_posiciones):
        '''
        Esta función revisa la frecuencia de cada letra en la misma posicion
        en la lista de palabras posibles y devuelve una probabilidad siendo la suma
        de las probabilidades de las letras por aparte

        Parameters
        ----------
        palabra : string
            Palabra que estamos revisando su probabilidad
        probabilidades_todas_posiciones: lista
            Es una lista que posee las probabilidades individuales de las letras
            según su posición
        Returns
        ----------
        probabilidad_palabra: Devuelve la probabilidad de la palabra de entre
        las palabras posibles
        '''
        
        probabilidad_palabra = 0
        for i, letra in enumerate(palabra):
            posicion = i + 1
            probabilidad_letra = probabilidades_todas_posiciones.get(posicion, {}).get(letra, 0)
            probabilidad_palabra += probabilidad_letra
        return probabilidad_palabra

    def calcular_probabilidades_palabras(self, palabras, probabilidades_todas_posiciones):
        '''
        Esta función revisa la probabilidades de todas las palabras y las acomoda
        en orden decrecientes para obtener las palabras con mayor probabilidad.

        Parameters
        ----------
        palabras : list
            Lista de todas las palabras que queden posibles
        probabilidades_todas_posiciones: lista
            Es una lista que posee las probabilidades individuales de las letras
            según su posición
        Returns
        ----------
        lista_probabilidades: lista con todas las probabilidades en orden decreciente
        '''
        lista_probabilidades = []
        for palabra in palabras:
            probabilidad = self.calcular_probabilidad_palabra(palabra, probabilidades_todas_posiciones)
            lista_probabilidades.append((palabra, probabilidad))
        lista_probabilidades.sort(key=lambda x: x[1], reverse=True)
        return lista_probabilidades

    def conteo_letras(self, lista):
        '''
        Cuenta las letras en cada posicion del 1 al 5 para poder calcular su
        probabilidad

        Parameters
        ----------
        lista : list
            Lista de todas las palabras que queden posibles
        Returns
        ----------
        lista_probabilidades: lista con todas las probabilidades en orden decreciente
        '''
        arr_words_5l = np.array([list(w) for w in lista])
        df_words_5l = pd.DataFrame(data=arr_words_5l,
                               columns=[f'letter_{i+1}' for i in range(5)])
        df_words_5l['word'] = lista
        
        test_dict_letter_counts = Counter()
        for i in range(5):
            test_dict_letter_counts[i+1] = Counter(df_words_5l[f'letter_{i+1}'])
    
        total_palabras = len(df_words_5l)
        probabilidades_todas_posiciones = {}
        for i in range(5):
            probabilidades_todas_posiciones[i+1] = {letra: conteo / total_palabras for letra, conteo in test_dict_letter_counts[i+1].items()}
    
        return probabilidades_todas_posiciones

    def jugar(self):
        '''
        Esta función simula los juegos, pidiendo una palabra y los estados en cada ronda
        actualiza las probabilidades y devuelve las tres palabras con mas probabilidad y el diccionario
        con las palabras posibles restantes
        '''
        probabilidades_todas_posiciones = self.conteo_letras(self.df_filtradas['word'])
        lista_probabilidades_filtradas = self.calcular_probabilidades_palabras(self.palabras_filtradas, probabilidades_todas_posiciones)
        
        #Imprime las 3 palabras con más probabilidades de la lista completa        
        print("\nLas 3 palabras con más probabilidad:")
        for palabra, probabilidad in lista_probabilidades_filtradas[:3]:
            print(f"La probabilidad de la palabra '{palabra}' es: {probabilidad:.4}")
        
        # While que permite jugar 6 rondas
        while self.intentos < self.max_intentos:
            
            #Input que pide la palabra escogida
            self.visual_app.word_ready.set(False)
            self.visual_app.root.wait_variable(self.visual_app.word_ready)
            
            palabra_escogida, estados = self.visual_app.get_word_and_states()
            
            print(f"Palabra: {palabra_escogida}, Estados: {estados}")
            
            self.visual_app.reset_word_ready()
            
        
            # Verificar si se ha ganado el juego con "GGGGG"
            if estados == 'GGGGG':
                messagebox.showinfo("¡Ganaste!", f"¡Ganaste! La palabra correcta es '{palabra_escogida}'.")
                self.visual_app.root.quit()  # Cerrar la ventana del juego al ganar
                print(f"¡Ganaste! La palabra correcta es '{palabra_escogida}'.")
                break
        
            # Cnvierte palabra y estados en lista de letras
            lista_palabra = list(palabra_escogida.upper())
            lista_estados = list(estados.upper())
        
            # Zip con resultados
            df_guess_results = pd.DataFrame(data=list(zip(lista_palabra, lista_estados)),
                                            columns=['letra', 'estado'],
                                            index=np.arange(1,6))
        
            already_solved = [key for key, value in self.dict_letters.items() if value is not None]
        
            # Revisa las letras resueltas
            df_letras_ver = df_guess_results.query('estado == "G"')
            if df_letras_ver.shape[0] > 0:
                for idx, row in df_letras_ver.iterrows():
                    
                    # Previene que se actualice para letras ya resueltas
                    if idx in already_solved:
                        pass
                    else:
                        corr_letter = row['letra']
                        self.dict_letters[idx] = corr_letter
                    
                        # Si la letra correcta, estaba mal colocada antes se elimina del diccionario
                        if corr_letter in self.dict_misplaced_letters.keys():
                            self.dict_misplaced_letters[corr_letter] -= 1
                            
                        # Filtra el dataframe para que solo tenga las palabras con la letra en la posicion correcta
                        self.df_filtradas = self.df_filtradas.query(f'letter_{idx}=="{corr_letter}"')
        
            # Añade las letras mal colocadas al diccionario
            df_letras_amar = df_guess_results.query('estado == "Y"')
            if df_letras_amar.shape[0] > 0:
                
                # Filtra el dataframe para que no tenga las palabras con la letra en la posicion incorrecta
                for idx, row in df_letras_amar.iterrows():
                    mispl_letter = row['letra']
                    self.df_filtradas = self.df_filtradas.query(f'letter_{idx}!="{mispl_letter}"')  
                
                # Revisa cuantas letras mal colocadas tenemos para que se filtre por palabras con la misma cantidad de letras
                guess_mispl_letters = df_letras_amar['letra'].values
                dict_guess_mispl_letters = Counter(guess_mispl_letters)
                
                # Actualiza el diccionario
                for key, value in dict_guess_mispl_letters.items():
                    self.dict_misplaced_letters[key] = value   
                    
        
                vect_check_misplaced_letters = np.vectorize(self.check_misplaced_letters)
                self.df_filtradas['valid'] = vect_check_misplaced_letters(self.df_filtradas['word'])
                self.df_filtradas = self.df_filtradas.query('valid == True')
                self.df_filtradas = self.df_filtradas.drop('valid', axis=1) 
                
            # Remueve todas las palabras que tengan la letra incorrecta, si esta no está en la lista de letras mal colocadas
            df_wrong_answers = df_guess_results.query('estado == "?"')
            if df_wrong_answers.shape[0] > 0:
                
                # Elimina las palabras que tengan la letra en la misma posicion incorrecta
                for idx, row in df_wrong_answers.iterrows():
                    inc_letter = row['letra']
                    self.df_filtradas = self.df_filtradas.query(f'letter_{idx}!="{inc_letter}"')
                
                # Para asegurarnos de no contar doble
                for l in df_wrong_answers['letra'].unique():
                    if self.dict_misplaced_letters[l] == 0:
                        self.possible_letters.remove(l)
        
            # Finalmente, actualiza la lista de posibles palabras con 5 letras, removiendo
            # todas las filas donde las letras aún no han sido adivinadas
            yet_to_solve = [key for key, value in self.dict_letters.items() if value is None]
            for position in yet_to_solve:
                
                # Revisa todas las letras en cada posicion
                position_letters = self.df_filtradas[f'letter_{position}']
                
                # Devuelve una lista de booleanos que inidca que si la lista está en los posibles valores
                position_in_possible_letters = [l in self.possible_letters for l in position_letters]
                
                # Actualiza el df
                self.df_filtradas = self.df_filtradas[position_in_possible_letters].copy(deep=True)
        
        
            print(self.df_filtradas)
        
        
            #print(f"Después de aplicar los estados '{estados}', las palabras filtradas son: {self.df_filtradas['word']}")
        
            probabilidades_todas_posiciones = self.conteo_letras(self.df_filtradas['word'])
        
            
            # Recalcular y mostrar las probabilidades de las palabras filtradas
            lista_probabilidades_filtradas = self.calcular_probabilidades_palabras(self.df_filtradas['word'], probabilidades_todas_posiciones)
            print("\nLas 3 palabras con más probabilidad:")
            for palabra, probabilidad in lista_probabilidades_filtradas[:3]:
                print(f"La probabilidad de la palabra '{palabra}' es: {probabilidad:.4}")
                
            palabras_mas_probables = [palabra for palabra, _ in lista_probabilidades_filtradas[:3]]
            messagebox.showinfo("Palabras con más probabilidad", f"Las 3 palabras con más probabilidad son: {', '.join(palabras_mas_probables)}")
            
        
            self.intentos += 1
        
            # Si se han superado los intentos, mostrar mensaje
            if self.intentos == self.max_intentos:
                print("Has superado el máximo de intentos. Mejor suerte la próxima vez.")
