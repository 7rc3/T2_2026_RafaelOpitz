# Projeto_Multimedia_2026_T2
Projeto Multimédia de Programação com Inteligência Artificial

- **Nome da Aplicação / Dashboard Web:** Dashboard Multimédia
- **Disciplina:** Oficina de Multimédia - 12.º Ano - CRSI
- **Ano Letivo:** 2026/2027
- **Autor:** Rafael Goto Opitz
- **Turma:** A3
- **Link da Aplicação Web:** https://7rc3.github.io/T2_2026_RafaelOpitz/
- **Repositório:** https://github.com/7rc3/T2_2026_RafaelOpitz

## 1. Visão Geral do Projeto

**Descrição:** Dashboard Web com aspeto de um pequeno "sistema operativo retro em pixel art", que reúne três widgets feitos em Python: um analisador poético, um jogo de campo minado (minesweeper) e o jogo da adivinha. O Python corre diretamente no browser, por isso a aplicação funciona como uma página estática no GitHub Pages.

**Proposta Escolhida:** Proposta 1

## 2. Estrutura do Código e Funcionalidades Integradas

Reutilização de dois widgets feitos em aula. Porte do Python para a web com PyScript, integração do código na web com ajuda da documentação do PyScript. UI inicial gerado com IA mas depois refeito manualmente; pop-ups e assets criados com auxílio da inteligência artificial. Neste projeto foi utilizado HTML, JavaScript e Tailwind CSS a substituir a maior parte do CSS.

### Widgets

| Widget | Base nas fichas | Extensão com IA |
|---|---|---|
| **Analisador Poético** | Fichas 6.1 e 7: contagem de palavras, strings, listas e dicionários | Nuvem de palavras com paletas de cores, sugestão de sinónimos poéticos e botão para reescrever o poema com sinónimos |
| **Campo Minado** | Listas dentro de listas (grelha), ciclos `for`/`while` e `if/elif/else` | Primeiro clique sempre seguro, abertura automática das casas vazias e botão de dica que encontra uma jogada 100% segura por lógica |
| **Jogo da Adivinha** | JOGO DA ADIVINHA (parte 2) | Níveis de dificuldade, dicas extra (par/ímpar, múltiplos, soma dos algarismos), histórico de tentativas e mensagens motivacionais |

Notas técnicas:
- Todo o código Python está em `app.py`. Lê e altera a página através de `pyscript.document` (pelo `id` dos elementos) e liga os botões às funções com `@when("click", "#id")`.
- O Pyodide não tem a biblioteca `wordcloud`, por isso a nuvem de palavras é feita com elementos HTML (`<span>`) com tamanhos diferentes conforme a frequência de cada palavra.
- As "extensões com IA" são código escrito com ajuda da IA. A página não faz pedidos a uma IA em tempo real, porque um site estático não consegue esconder uma chave de API.
- O pequeno script em JavaScript no fim do `index.html` só trata do "sistema operativo": abrir e fechar janelas, relógio, definições (guardadas no `localStorage`), scanlines e som de clique.

### Como executar

Online: abrir o link da aplicação web (GitHub Pages).

No computador: o `index.html` carrega o `app.py`, por isso não funciona se for aberto diretamente com duplo clique. É preciso servir a pasta com um servidor local:

```
python -m http.server 8000
```

Depois abrir http://localhost:8000 no browser. Na primeira vez demora alguns segundos a carregar, porque o browser descarrega o Python (Pyodide).

## 3. Registo de Utilização da IA

IA utilizada: Claude (Claude Code)

- **Prompt para conversão Web/HTML:**
  ver [prompts/conversaohtml.md](prompts/conversaohtml.md)
- **Prompt para ampliação e construção de funcionalidades:**
  Resumo:
  - arranque do projeto com a Proposta 1, PyScript, Tailwind CSS e GitHub Pages: a IA criou os três widgets iniciais a partir das fichas;
  - jogo da adivinha: o número secreto só é escolhido depois do primeiro palpite;
  - substituição do Validador Multimédia por um campo minado com o tema do site, incluindo o botão de dica;
  - pedidos de explicação do código (campo minado e cursor a piscar) para preparar a apresentação.
- **Dificuldades e erros corrigidos com a IA:**
  Optimização dos widegets e correção da expansão com auxilio da IA
- **Otimização de Layout:**
  No prompt de conversão pedi à IA um estilo de "sistema operativo retro em pixel art": paleta limitada de cerca de 8 cores (azul-arroxeado escuro, ciano claro, pêssego, coral, azul-céu, amarelo e branco), sem gradientes nem cantos arredondados, contornos sólidos e sombras "duras", fontes pixel do Google Fonts, ícones pixel art em SVG, animações aos "saltos" com `steps()`, barra de tarefas com data e definições (scanlines, som e dois temas de cor).

## 4. Estrutura de Ficheiros do Repositório

- `index.html`: página principal do Dashboard / Web App (estrutura, estilos com Tailwind CSS e o script do "sistema operativo")
- `app.py`: ficheiro principal da aplicação, com a lógica dos três widgets em Python
- `README.md`: este relatório de projeto
- `Assets/icons/`: ícones pixel art em SVG (ambiente de trabalho, barra de tarefas, mina e bandeira do campo minado)
- `prompts/`: prompts utilizados com a IA

Não há `style.css`: os estilos são feitos com classes do Tailwind CSS e um bloco `<style>` dentro do `index.html`.

## 5. Reflexão Crítica e Aprendizagem

Estou satisfeito com a estética do projeto. A inteligência articifial ajudou-me a optimizar e caçar erros inicialmente feitos a produzir os widgets. Também ajudou-me a integrar o codigo python na web.

- O que correu melhor durante o desenvolvimento?
- Qual foi a maior dificuldade?
- Como é que a Inteligência Artificial mudou a tua forma de programar?
