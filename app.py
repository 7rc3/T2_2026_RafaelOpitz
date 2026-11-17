# Dashboard Multimédia com IA - código Python que corre no browser (PyScript)
# Baseado nas fichas de Python de outubro (old/python.ipynb e old/parte2.ipynb)

import random
import time
from html import escape

from pyscript import document, when, window
from pyscript.ffi import create_proxy


def el(id):
    # atalho para ir buscar um elemento da página pelo id
    return document.getElementById(id)


# =====================================================================
# WIDGET 1 - Analisador Poético
# Baseado na ficha 6.1 (contagem de palavras) e 7 (nuvem de palavras)
# =====================================================================

STOPWORDS = {
    "a", "o", "as", "os", "e", "é", "de", "do", "da", "dos", "das", "em", "no",
    "na", "nos", "nas", "um", "uma", "uns", "umas", "que", "se", "por", "para",
    "com", "ao", "à", "aos", "às", "eu", "tu", "ele", "ela", "me", "te", "lhe",
    "mais", "mas", "como", "este", "esta", "isto", "esse", "essa", "não", "já",
    "meu", "minha", "seu", "sua", "pé",
}

# dicionário de sinónimos poéticos (sugestão gerada com ajuda da IA)
SINONIMOS = {
    # os sinónimos têm o mesmo género da palavra original (o mar -> o oceano)
    "mar": ["oceano", "abismo azul", "infinito azul"],
    "esforço": ["empenho", "labor", "afã"],
    "grande": ["imenso", "vasto", "colossal"],
    "pequeno": ["ínfimo", "breve", "humilde"],
    "homem": ["ser", "mortal", "navegante"],
    "navegador": ["marinheiro", "viajante", "argonauta"],
    "areal": ["areão", "litoral", "arenal"],
    "moreno": ["dourado", "queimado", "trigueiro"],
    "padrão": ["marco", "símbolo", "monumento"],
    "noite": ["escuridão", "treva", "sombra"],
    "dia": ["amanhecer", "alvorecer", "raiar"],
    "sol": ["astro", "astro-rei", "fogo celeste"],
    "amor": ["afeto", "querer", "bem-querer"],
    "triste": ["melancólico", "sombrio", "saudoso"],
    "feliz": ["radiante", "alegre", "sereno"],
    "vida": ["existência", "jornada", "travessia"],
    "morte": ["partida", "despedida", "finitude"],
    "céu": ["firmamento", "éter", "infinito"],
    "terra": ["pátria", "planície", "natureza"],
    "sonho": ["devaneio", "delírio", "anseio"],
    "tempo": ["momento", "instante", "fado"],
    "coração": ["peito", "âmago", "íntimo"],
    "vento": ["sopro", "vendaval", "zéfiro"],
    "luz": ["claridade", "centelha", "aurora"],
}

PALETAS = {
    "viridis": ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
    "oceano": ["#03045e", "#0077b6", "#00b4d8", "#48cae4", "#90e0ef"],
    "fogo": ["#6a040f", "#d00000", "#e85d04", "#faa307", "#ffba08"],
    "pastel": ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff"],
}


def limpar_palavras(texto):
    # tira a pontuação e divide o texto em palavras (como na ficha 6.1)
    for sinal in ".,;:!?«»\"'()—-":
        texto = texto.replace(sinal, " ")
    return texto.lower().split()


def contar_frequencia(palavras):
    frequencia = {}
    for palavra in palavras:
        if palavra not in STOPWORDS:
            frequencia[palavra] = frequencia.get(palavra, 0) + 1
    return frequencia


def desenhar_nuvem(frequencia):
    max_palavras = int(el("nuvem-max").value)
    cores = PALETAS[el("nuvem-paleta").value]

    # ordena da mais frequente para a menos frequente
    ordenadas = sorted(frequencia.items(), key=lambda item: item[1], reverse=True)
    ordenadas = ordenadas[:max_palavras]

    if not ordenadas:
        el("nuvem").innerHTML = '<p class="text-tinta/60">Sem palavras para mostrar.</p>'
        return

    maior = ordenadas[0][1]
    menor = ordenadas[-1][1]
    random.shuffle(ordenadas)  # baralha para parecer uma nuvem

    html = ""
    for palavra, quantidade in ordenadas:
        if maior == menor:
            tamanho = 22
        else:
            tamanho = 14 + (quantidade - menor) / (maior - menor) * 30
        cor = random.choice(cores)
        html += (
            f'<span class="inline-block px-1 font-bold hover:-translate-y-1" '
            f'style="font-size:{tamanho:.0f}px; color:{cor}" '
            f'title="{escape(palavra)}: {quantidade}x">{escape(palavra)}</span> '
        )
    el("nuvem").innerHTML = html


@when("click", "#btn-analisar")
def clicar_analisar(event):
    analisar_poema()


def analisar_poema():
    texto = el("poema").value
    palavras = limpar_palavras(texto)
    frequencia = contar_frequencia(palavras)

    # estatísticas (funções embutidas nas strings - ficha 6)
    linhas = [l for l in texto.split("\n") if l.strip() != ""]
    el("stat-palavras").innerText = str(len(palavras))
    el("stat-versos").innerText = str(len(linhas))
    el("stat-unicas").innerText = str(len(set(palavras)))
    if frequencia:
        mais_usada = max(frequencia, key=frequencia.get)
        el("stat-top").innerText = mais_usada
    else:
        el("stat-top").innerText = "-"

    desenhar_nuvem(frequencia)

    # sinónimos encontrados no poema
    encontrados = [p for p in sorted(set(palavras)) if p in SINONIMOS]
    if encontrados:
        html = ""
        for p in encontrados:
            html += (
                f'<li><span class="font-semibold text-coral">{escape(p)}</span>'
                f' → {", ".join(SINONIMOS[p])}</li>'
            )
        el("sinonimos").innerHTML = html
    else:
        el("sinonimos").innerHTML = '<li class="text-tinta/60">Nenhuma palavra com sinónimos conhecidos.</li>'


@when("click", "#btn-reescrever")
def reescrever_poema(event):
    # troca cada palavra que tem sinónimo por um sinónimo ao calhas
    novas_linhas = []
    for linha in el("poema").value.split("\n"):
        novas = []
        for palavra in linha.split(" "):
            base = limpar_palavras(palavra)
            if len(base) == 1 and base[0] in SINONIMOS:
                sinonimo = random.choice(SINONIMOS[base[0]])
                if palavra[:1].isupper():
                    sinonimo = sinonimo.capitalize()
                palavra = palavra.replace(palavra.strip(".,;:!?«»\"'()"), sinonimo)
            novas.append(palavra)
        novas_linhas.append(" ".join(novas))
    el("poema-novo").innerText = "\n".join(novas_linhas)


# =====================================================================
# WIDGET 2 - Campo Minado
# Usa listas dentro de listas (uma "grelha"), ciclos for/while e if/elif/else
# =====================================================================

# nível: (linhas, colunas, minas)
NIVEIS_MINAS = {
    "1": (8, 8, 10),
    "2": (10, 10, 16),
    "3": (12, 12, 28),
}

# cor de cada número: 1 = azul, 2 = escuro, 3 ou mais = vermelho
CORES_NUMEROS = {1: "text-ceu", 2: "text-tinta"}

campo = {
    "linhas": 0,
    "colunas": 0,
    "total_minas": 0,
    "minas": [],        # grelha com True onde há mina
    "estado": [],       # grelha com "fechada", "aberta" ou "bandeira"
    "primeiro": True,   # as minas só são postas depois do 1.º clique
    "ativo": False,
    "inicio": 0,        # hora do 1.º clique (para o cronómetro)
    "explodiu": None,   # casa onde o jogador perdeu
    "dica": None,       # casa que a dica está a mostrar
}


def criar_grelha(valor):
    # lista de linhas, cada linha é uma lista de casas
    grelha = []
    for l in range(campo["linhas"]):
        grelha.append([valor] * campo["colunas"])
    return grelha


def vizinhos(l, c):
    # devolve as casas à volta de (l, c): até 8, menos nos cantos e bordas
    lista = []
    for dl in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nl = l + dl
            nc = c + dc
            if dl == 0 and dc == 0:
                continue  # é a própria casa
            if 0 <= nl < campo["linhas"] and 0 <= nc < campo["colunas"]:
                lista.append((nl, nc))
    return lista


def contar_minas_perto(l, c):
    total = 0
    for nl, nc in vizinhos(l, c):
        if campo["minas"][nl][nc]:
            total += 1
    return total


def colocar_minas(l, c):
    # a casa do 1.º clique e as vizinhas ficam sempre sem minas
    proibidas = vizinhos(l, c) + [(l, c)]
    livres = []
    for nl in range(campo["linhas"]):
        for nc in range(campo["colunas"]):
            if (nl, nc) not in proibidas:
                livres.append((nl, nc))
    for ml, mc in random.sample(livres, campo["total_minas"]):
        campo["minas"][ml][mc] = True


def mensagem_minas(texto, cor="text-tinta"):
    el("minas-mensagem").className = f"min-h-12 {cor}"
    el("minas-mensagem").innerHTML = texto


def novo_campo():
    linhas, colunas, total = NIVEIS_MINAS[el("minas-nivel").value]
    campo["linhas"] = linhas
    campo["colunas"] = colunas
    campo["total_minas"] = total
    campo["minas"] = criar_grelha(False)
    campo["estado"] = criar_grelha("fechada")
    campo["primeiro"] = True
    campo["ativo"] = True
    campo["explodiu"] = None
    campo["dica"] = None

    el("minas-tempo").innerText = "0"
    el("minas-tabuleiro").style.gridTemplateColumns = f"repeat({colunas}, minmax(0, 1fr))"
    mensagem_minas("Clica numa casa para começar. O primeiro clique é sempre seguro! 🍀")
    desenhar_campo()


@when("click", "#btn-minas-novo")
def clicar_novo_campo(event):
    novo_campo()


@when("change", "#minas-nivel")
def mudar_nivel(event):
    novo_campo()


def abrir_casa(l, c):
    if not campo["ativo"] or campo["estado"][l][c] != "fechada":
        return

    if campo["primeiro"]:
        colocar_minas(l, c)
        campo["primeiro"] = False
        campo["inicio"] = time.time()

    if campo["minas"][l][c]:
        perder(l, c)
        return

    # abre a casa; se não tiver minas à volta, abre também as vizinhas
    # (a "pilha" guarda as casas que ainda faltam abrir)
    pilha = [(l, c)]
    while pilha:
        al, ac = pilha.pop()
        if campo["estado"][al][ac] != "fechada":
            continue
        campo["estado"][al][ac] = "aberta"
        if contar_minas_perto(al, ac) == 0:
            for vizinha in vizinhos(al, ac):
                pilha.append(vizinha)


def abrir_a_volta(l, c):
    # clicar num número já aberto: se já tem as bandeiras todas, abre o resto
    bandeiras = 0
    for nl, nc in vizinhos(l, c):
        if campo["estado"][nl][nc] == "bandeira":
            bandeiras += 1
    if bandeiras == contar_minas_perto(l, c):
        for nl, nc in vizinhos(l, c):
            abrir_casa(nl, nc)


def jogar(l, c):
    if not campo["ativo"]:
        return
    campo["dica"] = None
    if campo["estado"][l][c] == "aberta":
        abrir_a_volta(l, c)
    else:
        abrir_casa(l, c)

    if campo["ativo"] and ganhou():
        vencer()
    desenhar_campo()


def marcar_bandeira(l, c):
    if not campo["ativo"]:
        return
    if campo["estado"][l][c] == "fechada":
        campo["estado"][l][c] = "bandeira"
    elif campo["estado"][l][c] == "bandeira":
        campo["estado"][l][c] = "fechada"
    campo["dica"] = None
    desenhar_campo()


def ganhou():
    # ganha quando todas as casas sem mina estão abertas
    if campo["primeiro"]:
        return False
    for l in range(campo["linhas"]):
        for c in range(campo["colunas"]):
            if not campo["minas"][l][c] and campo["estado"][l][c] != "aberta":
                return False
    return True


def vencer():
    campo["ativo"] = False
    segundos = int(time.time() - campo["inicio"])
    el("minas-tempo").innerText = str(segundos)

    # põe bandeiras em todas as minas
    for l in range(campo["linhas"]):
        for c in range(campo["colunas"]):
            if campo["minas"][l][c]:
                campo["estado"][l][c] = "bandeira"

    if segundos < 30:
        elogio = "Velocidade de profissional! 🏆"
    elif segundos < 90:
        elogio = "Muito bem jogado! 🎉"
    else:
        elogio = "Com calma e paciência também se ganha! 🐢"
    mensagem_minas(
        f"<b>Campo limpo!</b> Demoraste {segundos} segundos. {elogio}",
        "border-2 border-tinta bg-sol p-2",
    )


def perder(l, c):
    campo["ativo"] = False
    campo["explodiu"] = (l, c)
    frase = random.choice([
        "Tão perto... para a próxima corre melhor! 🔁",
        "As minas não perdoam. Tenta outra vez! 💪",
        "Respira fundo e começa outro campo! 😅",
    ])
    mensagem_minas(
        f"<b>BOOM! 💥</b> Pisaste uma mina. {frase}",
        "border-2 border-tinta bg-coral p-2 text-branco",
    )


def desenhar_casa(l, c):
    estado = campo["estado"][l][c]
    mina = campo["minas"][l][c]
    posicao = f'data-celula="{l}-{c}"'
    img_mina = '<img src="Assets/icons/mina.svg" alt="mina">'
    img_bandeira = '<img src="Assets/icons/bandeira.svg" alt="bandeira">'

    # depois de perder: mostra as minas e as bandeiras erradas
    if campo["explodiu"] is not None:
        if campo["explodiu"] == (l, c):
            return f'<div class="celula bg-coral">{img_mina}</div>'
        if mina and estado != "bandeira":
            return f'<div class="celula">{img_mina}</div>'
        if estado == "bandeira" and not mina:
            return '<div class="celula text-coral" title="bandeira errada">X</div>'

    if estado == "fechada":
        extra = " celula-dica" if campo["dica"] == (l, c) else ""
        return f'<button {posicao} class="celula celula-fechada{extra}" aria-label="casa fechada"></button>'
    if estado == "bandeira":
        return f'<button {posicao} class="celula celula-fechada">{img_bandeira}</button>'

    # casa aberta: mostra quantas minas tem à volta (nada se for 0)
    numero = contar_minas_perto(l, c)
    if numero == 0:
        return '<div class="celula"></div>'
    cor = CORES_NUMEROS.get(numero, "text-coral")
    return f'<button {posicao} class="celula {cor}">{numero}</button>'


def desenhar_campo():
    html = ""
    for l in range(campo["linhas"]):
        for c in range(campo["colunas"]):
            html += desenhar_casa(l, c)
    el("minas-tabuleiro").innerHTML = html
    atualizar_contadores()


def atualizar_contadores():
    bandeiras = 0
    abertas = 0
    for l in range(campo["linhas"]):
        for c in range(campo["colunas"]):
            if campo["estado"][l][c] == "bandeira":
                bandeiras += 1
            elif campo["estado"][l][c] == "aberta":
                abertas += 1

    seguras = campo["linhas"] * campo["colunas"] - campo["total_minas"]
    el("minas-restantes").innerText = str(campo["total_minas"] - bandeiras)
    el("minas-limpo").innerText = f"{abertas * 100 // seguras}%"


def atualizar_relogio():
    # corre a cada segundo (ver o fim do ficheiro)
    if campo["ativo"] and not campo["primeiro"]:
        el("minas-tempo").innerText = str(int(time.time() - campo["inicio"]))


def casa_clicada(event):
    # descobre em que casa se clicou (ou None se foi entre as casas)
    botao = event.target.closest("[data-celula]")
    if not botao:
        return None
    l, c = botao.dataset.celula.split("-")
    return int(l), int(c)


@when("click", "#minas-tabuleiro")
def clicar_tabuleiro(event):
    casa = casa_clicada(event)
    if casa is None:
        return
    l, c = casa
    if el("minas-bandeira").checked:
        marcar_bandeira(l, c)
    else:
        jogar(l, c)


@when("contextmenu", "#minas-tabuleiro")
def clicar_direito(event):
    event.preventDefault()  # não abre o menu do browser
    casa = casa_clicada(event)
    if casa is not None:
        marcar_bandeira(casa[0], casa[1])


def procurar_dica():
    # extensão com IA: pensa como um jogador experiente.
    # Para cada número aberto, olha para as casas fechadas e as bandeiras à volta.
    for l in range(campo["linhas"]):
        for c in range(campo["colunas"]):
            if campo["estado"][l][c] != "aberta":
                continue
            numero = contar_minas_perto(l, c)
            if numero == 0:
                continue

            fechadas = []
            bandeiras = 0
            for nl, nc in vizinhos(l, c):
                if campo["estado"][nl][nc] == "fechada":
                    fechadas.append((nl, nc))
                elif campo["estado"][nl][nc] == "bandeira":
                    bandeiras += 1
            if not fechadas:
                continue

            # regra 1: o número já tem as bandeiras todas -> o resto é seguro
            if bandeiras == numero:
                return fechadas[0], (
                    f"Este {numero} já tem {bandeiras} bandeira(s) à volta, "
                    "por isso a casa a piscar é segura (se as tuas bandeiras estiverem certas). ✅"
                )
            # regra 2: só sobram tantas casas como minas em falta -> são todas minas
            if bandeiras + len(fechadas) == numero:
                return fechadas[0], (
                    f"Este {numero} só tem {len(fechadas) + bandeiras} casa(s) livre(s) à volta, "
                    "por isso a casa a piscar é uma mina. Põe lá uma bandeira! 🚩"
                )
    return None, "Não encontrei nenhuma jogada 100% segura... desta vez tens de arriscar! 🎲"


@when("click", "#btn-minas-dica")
def pedir_dica(event):
    if not campo["ativo"]:
        mensagem_minas("Começa um jogo novo primeiro.")
        return
    if campo["primeiro"]:
        mensagem_minas("💡 Podes clicar em qualquer casa: o primeiro clique nunca tem mina.")
        return
    casa, explicacao = procurar_dica()
    campo["dica"] = casa
    mensagem_minas(f"💡 {explicacao}")
    desenhar_campo()


# =====================================================================
# WIDGET 3 - Jogo Adivinha o Número
# Baseado no JOGO DA ADIVINHA da parte 2
# =====================================================================

jogo = {
    "secreto": 0,
    "tentativas": 0,
    "total": 0,
    "minimo": 1,
    "maximo": 100,
    "ativo": False,
    "historico": [],
}


def mostrar_mensagem(texto, cor="text-tinta"):
    el("jogo-mensagem").className = f"min-h-12 {cor}"
    el("jogo-mensagem").innerHTML = texto


def atualizar_jogo():
    restantes = jogo["total"] - jogo["tentativas"]
    el("jogo-restantes").innerText = str(restantes)
    el("jogo-intervalo").innerText = f"{jogo['minimo']} – {jogo['maximo']}"

    percentagem = 0 if jogo["total"] == 0 else restantes / jogo["total"] * 100
    el("jogo-barra").style.width = f"{percentagem}%"

    html = ""
    for numero, cor in jogo["historico"]:
        html += f'<span class="border-2 border-tinta px-2 py-1 text-sm font-semibold {cor}">{numero}</span>'
    el("jogo-historico").innerHTML = html


@when("click", "#btn-comecar")
def comecar_jogo(event):
    nivel = el("jogo-nivel").value
    if nivel == "1":
        jogo["total"] = 20
    elif nivel == "2":
        jogo["total"] = 10
    else:
        jogo["total"] = 5

    jogo["secreto"] = 0  # 0 = ainda não escolhido (só escolhemos depois do 1.º chute)
    jogo["tentativas"] = 0
    jogo["minimo"] = 1
    jogo["maximo"] = 100
    jogo["ativo"] = True
    jogo["historico"] = []

    el("jogo-chute").disabled = False
    el("btn-tentar").disabled = False
    el("jogo-chute").value = ""
    el("jogo-chute").focus()
    mostrar_mensagem(f"Pensei num número entre 1 e 100. Tens {jogo['total']} tentativas. Boa sorte! 🍀")
    atualizar_jogo()


def dica_extra():
    # dicas personalizadas que aparecem depois de errar algumas vezes
    secreto = jogo["secreto"]
    tentativa = jogo["tentativas"]

    if tentativa == 2:
        return "O número é " + ("par." if secreto % 2 == 0 else "ímpar.")
    if tentativa == 3:
        for divisor in (10, 5, 3, 7):
            if secreto % divisor == 0:
                return f"O número é múltiplo de {divisor}."
        return "O número não é múltiplo de 3, 5, 7 nem 10."
    if tentativa == 4 and secreto > 10:
        return f"A soma dos algarismos é {sum(int(a) for a in str(secreto))}."
    return ""


def mensagem_motivacional():
    restantes = jogo["total"] - jogo["tentativas"]
    if restantes == 1:
        return "Última tentativa! Respira fundo... 😬"
    if restantes <= jogo["total"] * 0.3:
        return "Está a apertar, mas ainda dá! 💪"
    if jogo["maximo"] - jogo["minimo"] <= 10:
        return "Já estás mesmo quase! 🔥"
    return random.choice([
        "Continua, vais no bom caminho!",
        "Boa estratégia, não desistas!",
        "Cada erro dá-te mais pistas 🧠",
    ])


@when("click", "#btn-tentar")
def clicar_tentar(event):
    tentar()


def tentar():
    if not jogo["ativo"]:
        return

    try:
        chute = int(el("jogo-chute").value)
    except ValueError:
        mostrar_mensagem("Digita um número inteiro!", "font-semibold text-coral")
        return

    if chute < 1 or chute > 100:
        mostrar_mensagem("Por favor, digita um número entre 1 e 100!", "font-semibold text-coral")
        return

    # no primeiro chute, escolhe o número secreto, mas nunca igual ao chute
    if jogo["secreto"] == 0:
        numero = random.randrange(1, 101)
        while numero == chute:
            numero = random.randrange(1, 101)
        jogo["secreto"] = numero

    jogo["tentativas"] += 1
    secreto = jogo["secreto"]
    el("jogo-chute").value = ""
    el("jogo-chute").focus()

    if chute == secreto:
        jogo["ativo"] = False
        jogo["historico"].append((chute, "bg-tinta text-sol"))
        if jogo["tentativas"] == 1:
            elogio = "À primeira?! És um génio! 🤯"
        elif jogo["tentativas"] <= 4:
            elogio = "Excelente raciocínio! 🏆"
        else:
            elogio = "Conseguiste! 🎉"
        mostrar_mensagem(
            f"<b>UAU, acertaste!</b> O número secreto era {secreto}. "
            f"Precisaste de {jogo['tentativas']} tentativa(s). {elogio}",
            "border-2 border-tinta bg-sol p-2",
        )
        terminar_jogo()
        return

    # atualiza o intervalo onde o número pode estar
    if chute > secreto:
        jogo["maximo"] = min(jogo["maximo"], chute - 1)
        direcao = f"O {chute} é <b>maior</b> que o número secreto. ⬇️"
    else:
        jogo["minimo"] = max(jogo["minimo"], chute + 1)
        direcao = f"O {chute} é <b>menor</b> que o número secreto. ⬆️"

    # quente ou frio
    distancia = abs(chute - secreto)
    if distancia <= 3:
        temperatura = "🔥 A ferver!"
        cor = "bg-coral text-branco"
    elif distancia <= 10:
        temperatura = "♨️ Quente"
        cor = "bg-pessego text-tinta"
    elif distancia <= 25:
        temperatura = "🌤️ Morno"
        cor = "bg-sol text-tinta"
    else:
        temperatura = "❄️ Frio"
        cor = "bg-ceu text-branco"
    jogo["historico"].append((chute, cor))

    if jogo["tentativas"] >= jogo["total"]:
        jogo["ativo"] = False
        mostrar_mensagem(
            f"Perdeste! O número secreto era <b>{secreto}</b>. Tenta outra vez! 🔁",
            "border-2 border-tinta bg-coral p-2 text-branco",
        )
        terminar_jogo()
        return

    dica = dica_extra()
    texto = f"{direcao} {temperatura}<br>"
    if dica:
        texto += f"💡 Dica: {dica}<br>"
    texto += f"<span class='text-tinta/60'>{mensagem_motivacional()}</span>"
    mostrar_mensagem(texto)
    atualizar_jogo()


@when("keydown", "#jogo-chute")
def tecla_enter(event):
    if event.key == "Enter":
        tentar()


def terminar_jogo():
    el("jogo-chute").disabled = True
    el("btn-tentar").disabled = True
    atualizar_jogo()


# =====================================================================
# Arranque: prepara a página e esconde o ecrã de carregamento
# =====================================================================
analisar_poema()
novo_campo()

# o cronómetro do campo minado atualiza a cada 1000 ms (1 segundo)
window.setInterval(create_proxy(atualizar_relogio), 1000)

el("loading").remove()
