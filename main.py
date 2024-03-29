from flask import Flask, render_template, flash, redirect, url_for, request
from data import Materias
import pandas as pd
import json
import openpyxl

x = 'json = [{"periodo":"2","disciplina":"Base Experimental das Ciências Naturais","conceito":"A",' \
    '"situacao":"Aprovado","ano":2015,"codigo":"BCS0001-13","categoria":"Obrigatória","creditos":3},{"periodo":"2",' \
    '"disciplina":"Estrutura da Matéria","conceito":"B","situacao":"Aprovado","ano":2015,"codigo":"BIK0102-13",' \
    '"categoria":"Obrigatória","creditos":3},{"periodo":"2","disciplina":"Origem da Vida e Diversidade dos Seres ' \
    'Vivos","conceito":"B","situacao":"Aprovado","ano":2015,"codigo":"BIL0304-13","categoria":"Obrigatória",' \
    '"creditos":3},{"periodo":"2","disciplina":"Bases Computacionais da Ciência","conceito":"A",' \
    '"situacao":"Aprovado","ano":2015,"codigo":"BIM0005-13","categoria":"Obrigatória","creditos":2},{"periodo":"2",' \
    '"disciplina":"Bases Matemáticas","conceito":"F","situacao":"Reprovado","ano":2015,"codigo":"BIN0003-13",' \
    '"categoria":"Obrigatória","creditos":4},{"periodo":"3","disciplina":"Fenômenos Mecânicos","conceito":"F",' \
    '"situacao":"Reprovado","ano":2015,"codigo":"BCJ0208-13","categoria":"Obrigatória","creditos":5},{"periodo":"3",' \
    '"disciplina":"Natureza da Informação","conceito":"B","situacao":"Aprovado","ano":2015,"codigo":"BCM0504-13",' \
    '"categoria":"Obrigatória","creditos":3},{"periodo":"3","disciplina":"Funções de Uma Variável","conceito":"F",' \
    '"situacao":"Reprovado","ano":2015,"codigo":"BCN0402-13","categoria":"Obrigatória","creditos":4},{"periodo":"3",' \
    '"disciplina":"Geometria Analítica","conceito":"B","situacao":"Aprovado","ano":2015,"codigo":"BCN0404-13",' \
    '"categoria":"Obrigatória","creditos":3},{"periodo":"1","disciplina":"Fenômenos Térmicos","conceito":"F",' \
    '"situacao":"Reprovado","ano":2016,"codigo":"BCJ0205-15","categoria":"Obrigatória","creditos":4},{"periodo":"1",' \
    '"disciplina":"Transformações Químicas","conceito":"C","situacao":"Aprovado","ano":2016,"codigo":"BCL0307-15",' \
    '"categoria":"Obrigatória","creditos":5},{"periodo":"1","disciplina":"Processamento da Informação",' \
    '"conceito":"B","situacao":"Aprovado","ano":2016,"codigo":"BCM0505-15","categoria":"Obrigatória","creditos":5},' \
    '{"periodo":"2","disciplina":"Fenômenos Eletromagnéticos","conceito":"D","situacao":"Aprovado","ano":2016,' \
    '"codigo":"BCJ0203-15","categoria":"Obrigatória","creditos":5},{"periodo":"2","disciplina":"Comunicação e Redes",' \
    '"conceito":"A","situacao":"Aprovado","ano":2016,"codigo":"BCM0506-15","categoria":"Obrigatória","creditos":3},' \
    '{"periodo":"2","disciplina":"Bases Epistemológicas da Ciência Moderna","conceito":"B","situacao":"Aprovado",' \
    '"ano":2016,"codigo":"BIR0004-15","categoria":"Obrigatória","creditos":3},{"periodo":"2","disciplina":"Bases ' \
    'Matemáticas","conceito":"C","situacao":"Aprovado","ano":2016,"codigo":"BIS0003-15","categoria":"Obrigatória",' \
    '"creditos":4},{"periodo":"3","disciplina":"Fenômenos Térmicos","conceito":"B","situacao":"Aprovado","ano":2016,' \
    '"codigo":"BCJ0205-15","categoria":"Obrigatória","creditos":4},{"periodo":"3","disciplina":"Bioquímica: ' \
    'Estrutura, Propriedade e Funções de Biomoléculas","conceito":"B","situacao":"Aprovado","ano":2016,' \
    '"codigo":"BCL0308-15","categoria":"Obrigatória","creditos":5},{"periodo":"3","disciplina":"Funções de Uma ' \
    'Variável","conceito":"C","situacao":"Aprovado","ano":2016,"codigo":"BCN0402-15","categoria":"Obrigatória",' \
    '"creditos":4},{"periodo":"3","disciplina":"Estrutura e Dinâmica Social","conceito":"C","situacao":"Aprovado",' \
    '"ano":2016,"codigo":"BIQ0602-15","categoria":"Obrigatória","creditos":3},{"periodo":"1","disciplina":"Funções de ' \
    'Várias Variáveis","conceito":"B","situacao":"Aprovado","ano":2017,"codigo":"BCN0407-15",' \
    '"categoria":"Obrigatória","creditos":4},{"periodo":"1","disciplina":"Bases Conceituais da Energia",' \
    '"conceito":"B","situacao":"Aprovado","ano":2017,"codigo":"BIJ0207-15","categoria":"Obrigatória","creditos":2},' \
    '{"periodo":"1","disciplina":"Ciência, Tecnologia e Sociedade","conceito":"B","situacao":"Aprovado","ano":2017,' \
    '"codigo":"BIR0603-15","categoria":"Obrigatória","creditos":3},{"periodo":"1","disciplina":"Introdução às ' \
    'Engenharias","conceito":"A","situacao":"Aprovado","ano":2017,"codigo":"ESTO005-13","categoria":"Opção Limitada",' \
    '"creditos":2},{"periodo":"1","disciplina":"Cálculo Numérico","conceito":"B","situacao":"Aprovado","ano":2017,' \
    '"codigo":"MCTB009-13","categoria":"Opção Limitada","creditos":4},{"periodo":"2","disciplina":"Introdução às ' \
    'Equações Diferenciais Ordinárias","conceito":"D","situacao":"Aprovado","ano":2017,"codigo":"BCN0405-15",' \
    '"categoria":"Obrigatória","creditos":4},{"periodo":"2","disciplina":"Energia, Meio Ambiente e Sociedade",' \
    '"conceito":"C","situacao":"Aprovado","ano":2017,"codigo":"ESTE004-17","categoria":"Opção Limitada",' \
    '"creditos":4},{"periodo":"2","disciplina":"Materiais e Suas Propriedades","conceito":"F","situacao":"Reprovado",' \
    '"ano":2017,"codigo":"ESTO006-17","categoria":"Opção Limitada","creditos":4},{"periodo":"2",' \
    '"disciplina":"Mecânica dos Sólidos I","conceito":"F","situacao":"Reprovado","ano":2017,"codigo":"ESTO008-17",' \
    '"categoria":"Opção Limitada","creditos":4},{"periodo":"2","disciplina":"Fundamentos de Desenho Técnico",' \
    '"conceito":"B","situacao":"Aprovado","ano":2017,"codigo":"ESTO011-17","categoria":"Opção Limitada",' \
    '"creditos":2},{"periodo":"3","disciplina":"Fenômenos Mecânicos","conceito":"D","situacao":"Aprovado","ano":2017,' \
    '"codigo":"BCJ0204-15","categoria":"Obrigatória","creditos":5},{"periodo":"3","disciplina":"Biodiversidade: ' \
    'Interações entre organismos e ambiente","conceito":"F","situacao":"Reprovado","ano":2017,"codigo":"BCL0306-15",' \
    '"categoria":"Obrigatória","creditos":3},{"periodo":"3","disciplina":"Introdução à Probabilidade e à ' \
    'Estatística","conceito":"F","situacao":"Reprovado","ano":2017,"codigo":"BIN0406-15","categoria":"Obrigatória",' \
    '"creditos":3},{"periodo":"3","disciplina":"Projeto Assistido por Computador","conceito":"A",' \
    '"situacao":"Aprovado","ano":2017,"codigo":"ESTA019-17","categoria":"Opção Limitada","creditos":2},' \
    '{"periodo":"3","disciplina":"Transformadas em Sinais e Sistemas Lineares","conceito":"F","situacao":"Reprovado",' \
    '"ano":2017,"codigo":"ESTI003-17","categoria":"Opção Limitada","creditos":4},{"periodo":"1",' \
    '"disciplina":"Modelagem e Controle","conceito":"F","situacao":"Reprovado","ano":2018,"codigo":"ESTA020-17",' \
    '"categoria":"Opção Limitada","creditos":2},{"periodo":"1","disciplina":"Transferência de Calor I",' \
    '"conceito":"F","situacao":"Reprovado","ano":2018,"codigo":"ESTE022-17","categoria":"Opção Limitada",' \
    '"creditos":4},{"periodo":"1","disciplina":"Política Energética","conceito":"B","situacao":"Aprovado","ano":2018,' \
    '"codigo":"ESZE111-17","categoria":"Livre Escolha","creditos":4},{"periodo":"1","disciplina":"Álgebra Linear",' \
    '"conceito":"C","situacao":"Aprovado","ano":2018,"codigo":"MCTB001-17","categoria":"Opção Limitada",' \
    '"creditos":6},{"periodo":"2","disciplina":"Introdução à Probabilidade e à Estatística","conceito":"F",' \
    '"situacao":"Reprovado","ano":2018,"codigo":"BIN0406-15","categoria":"Obrigatória","creditos":3},{"periodo":"2",' \
    '"disciplina":"Sistemas CAD/CAM","conceito":"C","situacao":"Aprovado","ano":2018,"codigo":"ESTA014-17",' \
    '"categoria":"Opção Limitada","creditos":4},{"periodo":"2","disciplina":"Economia da Energia","conceito":"C",' \
    '"situacao":"Aprovado","ano":2018,"codigo":"ESTE036-17","categoria":"Opção Limitada","creditos":4},' \
    '{"periodo":"2","disciplina":"Mecânica dos Fluidos I","conceito":"F","situacao":"Reprovado","ano":2018,' \
    '"codigo":"ESTO015-17","categoria":"Opção Limitada","creditos":4},{"periodo":"3","disciplina":"Física Quântica",' \
    '"conceito":"O","situacao":"Repr.Freq","ano":2018,"codigo":"BCK0103-15","categoria":"Obrigatória","creditos":3},' \
    '{"periodo":"3","disciplina":"Circuitos Elétricos I","conceito":"F","situacao":"Reprovado","ano":2018,' \
    '"codigo":"ESTA002-17","categoria":"Opção Limitada","creditos":5},{"periodo":"3","disciplina":"Engenharia de ' \
    'Petróleo e Gás","conceito":"D","situacao":"Aprovado","ano":2018,"codigo":"ESTE030-17","categoria":"Opção ' \
    'Limitada","creditos":4},{"periodo":"3","disciplina":"Materiais e Suas Propriedades","conceito":"B",' \
    '"situacao":"Aprovado","ano":2018,"codigo":"ESTO006-17","categoria":"Opção Limitada","creditos":4},' \
    '{"periodo":"1","disciplina":"Física Quântica","conceito":"C","situacao":"Aprovado","ano":2019,' \
    '"codigo":"BCK0103-15","categoria":"Obrigatória","creditos":3},{"periodo":"1","disciplina":"Biodiversidade: ' \
    'Interações entre organismos e ambiente","conceito":"C","situacao":"Aprovado","ano":2019,"codigo":"BCL0306-15",' \
    '"categoria":"Obrigatória","creditos":3},{"periodo":"1","disciplina":"Transformadas em Sinais e Sistemas ' \
    'Lineares","conceito":"F","situacao":"Reprovado","ano":2019,"codigo":"ESTI003-17","categoria":"Opção Limitada",' \
    '"creditos":4},{"periodo":"1","disciplina":"Redes de Computadores","conceito":"F","situacao":"Reprovado",' \
    '"ano":2019,"codigo":"MCTA022-17","categoria":"Opção Limitada","creditos":4},{"periodo":"1",' \
    '"disciplina":"Engenharia de Software","conceito":"F","situacao":"Reprovado","ano":2019,"codigo":"MCTA033-15",' \
    '"categoria":"Opção Limitada","creditos":4},{"periodo":"2","disciplina":"TRANCAMENTO TOTAL","conceito":"-",' \
    '"situacao":"Trt. Total","ano":2019,"codigo":"TRT","categoria":"-","creditos":0},{"periodo":"3",' \
    '"disciplina":"TRANCAMENTO TOTAL","conceito":"-","situacao":"Trt. Total","ano":2019,"codigo":"TRT",' \
    '"categoria":"-","creditos":0},{"periodo":"1","disciplina":"Informação e Sociedade","conceito":"C",' \
    '"situacao":"Aprovado","ano":2020,"codigo":"ESZI027-17","categoria":"Opção Limitada","creditos":2},' \
    '{"periodo":"1","disciplina":"Práticas de Ensino de Matemática I","conceito":"B","situacao":"Aprovado",' \
    '"ano":2020,"codigo":"MCTD016-18","categoria":"Opção Limitada","creditos":4},{"periodo":"2",' \
    '"disciplina":"Interações Atômicas e Moleculares","conceito":"C","situacao":"Aprovado","ano":2020,' \
    '"codigo":"BCK0104-15","categoria":"Obrigatória","creditos":3},{"periodo":"2","disciplina":"Introdução à ' \
    'Probabilidade e à Estatística","conceito":"C","situacao":"Aprovado","ano":2020,"codigo":"BIN0406-15",' \
    '"categoria":"Obrigatória","creditos":3},{"periodo":"2","disciplina":"Princípios de Administração",' \
    '"conceito":"C","situacao":"Aprovado","ano":2020,"codigo":"ESTO012-17","categoria":"Opção Limitada",' \
    '"creditos":2},{"periodo":"2","disciplina":"Programação Estruturada","conceito":"A","situacao":"Aprovado",' \
    '"ano":2020,"codigo":"MCTA028-15","categoria":"Opção Limitada","creditos":4}] '
app = Flask(__name__)
Materias = Materias()


@app.route('/', methods=['GET', 'POST'])
def index():
    excel = pd.read_excel('disciplinas_ufabc-grade.xlsx', sheet_name='Matérias', engine='openpyxl')
    cursos = excel.to_dict()
    cursos = [curso for curso in cursos['Curso'].values()]
    if request.method == 'POST':
        data_json = request.form['data_json']
        curso_atual = request.form['curso']
        tratamento(curso_atual, data_json)
        return render_template('materia.html', data=data_json, curso=curso_atual)
        pass
    return render_template('home.html', cursos=cursos)


@app.route('/sobre')
def about():
    return render_template('about.html')


@app.route('/grade')
def articles():
    return render_template('grade.html', materias=Materias)


@app.route('/materia/<string:codigo>/')
def materia(codigo):
    return render_template('materia.html', codigo=codigo)


def tratamento(curso, historico):
    historico = x  # im forcing a json to test
    historico = historico.rsplit('=')
    y = json.loads(historico[1])
    print(curso)
    pass


if __name__ == '__main__':
    app.run(debug=True)
