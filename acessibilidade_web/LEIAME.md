# 🌐 Interface Acessível Web – Dashboard de Evasão em IES

Este módulo tem como objetivo oferecer uma **interface web acessível** e responsiva para visualização das taxas de **ingresso, conclusão e evasão** em Instituições de Ensino Superior (IES) públicas brasileiras, com base nos dados tratados pelo pipeline `app_evasao.py` desenvolvido em Python com Streamlit.

## 🎯 Objetivos

- Aplicar princípios de **UX/UI** e **acessibilidade (WCAG)** na camada de visualização.
- Incorporar **as 10 heurísticas de usabilidade de Nielsen**.
- Permitir o acesso por usuários com **deficiência visual, baixa visão ou daltonismo**.
- Viabilizar a futura conversão para **Progressive Web App (PWA)**.
- Tornar o sistema utilizável tanto no modo claro quanto no modo escuro (automático).

## 🛠️ Tecnologias Utilizadas

- **HTML5** e **CSS3** com fontes da Google Fonts (`Roboto`)
- Acessibilidade via `aria-label`, `role`, `tooltip`, `alt`, `aria-describedby`
- Paleta e estilo inspirado no site da Apple (contraste alto)
- Responsividade e legibilidade aprimorada
- Exportação de gráficos via Python (`matplotlib`) como imagens PNG
- Integração futura opcional via iframe (Streamlit app) ou backend (Flask/FastAPI)

## ♿ Acessibilidade Aplicada

- Alto contraste (modo escuro/claro)
- Leitores de tela (VoiceOver, NVDA, JAWS) suportados
- Tooltips explicativos e linguagem simples
- Fontes responsivas e escaláveis
- Suporte visual para filtros e botões (exportar, resetar)
- Descrição textual alternativa para gráficos
- Estrutura semântica HTML clara (uso de `main`, `section`, `aria-*`, etc)

## 🔗 Integração com `app_evasao.py`

O script `app_evasao.py` gera o gráfico de forma automatizada:

```python
fig.savefig("acessibilidade_web/graficos/grafico_taxas.png")


Estrutura de Arquivos

/acessibilidade_web
│
├── index.html              ← Interface acessível com modo escuro e gráficos
├── LEIA.md                 ← Este documento explicativo
├── graficos/
│   └── grafico_taxas.png   ← Gráfico exportado via matplotlib (app_evasao.py)
├── scripts/
│   └── app_evasao.py       ← Pipeline de análise e geração de gráficos
├── dados/
│   └── processado/         ← Dados tratados pelo pipeline (CSV final)
└── style/
    └── custom.css          ← Estilos visuais adicionais (separado do inline)


    Futuras Extensões
	•	Transformar em PWA com manifest.json e Service Workers
	•	Adicionar navegação por teclado (tabindex) aprimorada
	•	Gerar gráficos interativos com Chart.js (opcional)
	•	Implementar backend leve com Flask/FastAPI para gerar dados sob demanda
	•	Armazenar comentários e feedback de usuários via blog ou formulário

⸻

Desenvolvido por Eduardo Fernandes Bueno — Mestrado em Ciência da Computação – UEL (2025), disciplina de Interface Homem-Computador.