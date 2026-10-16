import sys
sys.path.insert(1, '././')

import json
from defs import ca
import os.path
import time


#TXT

if True:
    def limpar_txt(caminho):
        with open(caminho, 'w', encoding='UTF-8') as arquivo:
            arquivo.write('')
            

    def adc_txt(caminho, temp):
        with open(caminho, 'a', encoding='UTF-8') as arquivo:
            arquivo.write(temp)        

    def adc_linhas(caminho, temp):
        with open(caminho, 'a', encoding='UTF-8') as arquivo:
            arquivo.writelines(temp)
            

    def ler_txt(caminho):
        with open(caminho, 'r', encoding='UTF-8') as arquivo:
            return arquivo.read()


    def ler_linhas(caminho):
        with open(caminho, 'r', encoding='UTF-8') as arquivo:
            return arquivo.readlines()

                      
            
    def salvar_txt(caminho, temp='TEMP NÃO DEFINIDO'):
        try:
            with open(caminho, 'w', encoding='UTF-8') as arquivo:
                arquivo.write(temp)

        except:
            print(f'ERRO AO SAVLAR TEXTO')


    def salvar_linhas(caminho, temp='TEMP NÃO DEFINIDO'):
        try:
            with open(caminho, 'w', encoding='UTF-8') as arquivo:
                arquivo.writelines(temp)
                
        except:
            print(f'ERRO AO SAVLAR LINHAS')


            
        
# JSON
if True:     
                            
    def ler_json(caminho):
        while True:
            
            try:
                with open(caminho, 'r', encoding='UTF-8') as arquivo:
                    return json.load(arquivo)

            except:
                time.sleep(0.1) 
                print(f"{caminho:<50}", "\rERRO AO LER JSON",end='', flush=True)
                
                                                
    def limpar_json(caminho):
        with open(caminho, 'w', encoding='UTF-8') as arquivo:
            arquivo.write('{}')
            
        return
            
                                        
    def salvar_json(caminho, temp='TEMP NÃO DEFINIDO'):
        try:
            if (caminho[-4:]) == 'json':
                if type(temp) == dict:
                    try:
                    
                        with open(caminho, 'w', encoding='UTF-8') as arquivo:
                            
                            json.dump(temp, arquivo, indent = 4)
                            
                        
                    except:
                        print(f'ERRO AO SALVAR JSON')
                            
                else:
                    print(f'ERRO, JSON COM FORMATO INVALIDO')    
                                    
            else:
                print(f'ERRO, ESCOLHA UM CAMINHO .JSON')
        except:
            print(f'ERRO AO SALVAR JSON')
         
                                
    def att_json(caminho, temp='TEMP NÃO DEFINIDO', qtd_chave=0, chave1='', chave2='', chave3='', chave4='', chave5='', chave6='', chave7='', chave8='', chave9='', chave10=''):
        try:
            copy_dados = (ler_json(caminho))
                            
            if qtd_chave == 0:
                copy_dados = temp
            
            if qtd_chave == 1:
                copy_dados[chave1] = temp
                
            if qtd_chave == 2:
                copy_dados[chave1][chave2] = temp
                        
            if qtd_chave == 3:
                copy_dados[chave1][chave2][chave3] = temp
                
            if qtd_chave == 4:
                copy_dados[chave1][chave2][chave3][chave4] = temp
                
            if qtd_chave == 5:
                copy_dados[chave1][chave2][chave3][chave4][chave5] = temp        
                
            if qtd_chave == 6:
                copy_dados[chave1][chave2][chave3][chave4][chave5][chave6] = temp
                
            if qtd_chave == 7:
                copy_dados[chave1][chave2][chave3][chave4][chave5][chave6][chave7] = temp 
                    
            if qtd_chave == 8:
                copy_dados[chave1][chave2][chave3][chave4][chave5][chave6][chave7][chave8] = temp      
                        
            if qtd_chave == 9:
                copy_dados[chave1][chave2][chave3][chave4][chave5][chave6][chave7][chave8][chave9] = temp      
                        
            if qtd_chave == 10:
                copy_dados[chave1][chave2][chave3][chave4][chave5][chave6][chave7][chave8][chave9][chave10] = temp
            
            salvar_json(caminho, copy_dados)
            
        except TypeError:
            print(caminho, 'ERRO AO ATUALIZAR JSON', TypeError)
            

    def del_json(caminho, qtd_chave=1, chave1='', chave2='', chave3='', chave4='', chave5=''):
        try:
            copy_dados = (ler_json(caminho))
        
            if qtd_chave == 1:
                del copy_dados[chave1]
                
            if qtd_chave == 2:
                del copy_dados[chave1][chave2]
                        
            if qtd_chave == 3:
                del copy_dados[chave1][chave2][chave3]
                
            if qtd_chave == 4:
                del copy_dados[chave1][chave2][chave3][chave4]
                
            if qtd_chave == 5:
                del copy_dados[chave1][chave2][chave3][chave4][chave5]
                
            salvar_json(caminho, copy_dados)
        
        except:
            print(f'ERRO AO DELETA CHAVE {chave1} {chave2} {chave3} {chave4} {chave5} ')


    def remove_keys(caminho, keys):
        
        arquivo = ler_json(caminho)
        
        for c in range(0, len(keys)):
            if keys[c] in arquivo:
                chave = keys[c]
                print(chave)
                del arquivo[chave]
                
        salvar_json(caminho, arquivo)
        return f"{len(keys)} chaves removidas"

    def ler_qtd(caminho):
        
        ler = int(len(ler_json(caminho)))
        return ler


#LISTA
if True:
    def ler_lista(temp):
        lista = ler_txt(ca.cache)
        
        if type(lista) == list:
            lista = lista
        
        if type(lista) == str:
            lista = lista.splitlines()
            
        limpar_txt(ca.cache)
        
        
        for c in range(0, len(lista)):
            linha = lista[c]
            adc_txt(ca.cache, f"{linha}\n")
            
        texto = ler_txt(ca.cache)
        
        limpar_txt(ca.cache)
        
        return texto


# HTML
if True:
    def salvar_html(caminho, temp='TEMP NÃO DEFINIDO'):
        
        try:
            with open(caminho, 'w', encoding='UTF-8') as arquivo:
                arquivo.write(temp)

        except:
            print(f'ERRO AO SAVLAR HTML')

    def limpar_html(caminho):
        
        try:
            with open(caminho, 'w', encoding='UTF-8') as arquivo:
                arquivo.write('')

        except:
            print(f'ERRO AO LIMPAR HTML')
