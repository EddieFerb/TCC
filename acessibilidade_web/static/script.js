document.addEventListener('DOMContentLoaded', function () {
  // Tour guiado para leitores de tela
  const tourSteps = [
    "Bem-vindo ao sistema de análise de dados educacionais.",
    "Use as setas do teclado para navegar entre seções.",
    "Pressione Enter para acessar detalhes de cada gráfico."
  ];

  let currentStep = 0;

  function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-BR';
    speechSynthesis.speak(utterance);
  }

  function startTour() {
    if ('speechSynthesis' in window) {
      speak(tourSteps[currentStep]);
    }
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') {
      currentStep = (currentStep + 1) % tourSteps.length;
      speak(tourSteps[currentStep]);
    }
  });

  // Botões acessíveis
  const accessibleButtons = document.querySelectorAll('button');
  accessibleButtons.forEach(button => {
    if (!button.hasAttribute('aria-label')) {
      const label = button.textContent.trim() || 'Botão';
      button.setAttribute('aria-label', label);
      button.setAttribute('title', label);
    }
  });

  // Descrição dinâmica de gráficos (com aria-live)
  const graficoDescricao = document.createElement('div');
  graficoDescricao.setAttribute('id', 'grafico-descricao');
  graficoDescricao.setAttribute('aria-live', 'polite');
  graficoDescricao.setAttribute('role', 'status');
  graficoDescricao.className = 'sr-only';
  document.body.appendChild(graficoDescricao);

  function atualizarDescricaoGrafico(texto) {
    graficoDescricao.textContent = texto;
  }

  // Exemplo: descrição fictícia inicial
  atualizarDescricaoGrafico("Gráfico inicial: evasão nos cursos superiores de 2015 a 2023.");

  // Expandir com descrições geradas dinamicamente se necessário

  // Carregar gráfico com base nos filtros
  const botaoFiltrar = document.getElementById('filtrar-btn');
  if (botaoFiltrar) {
    botaoFiltrar.addEventListener('click', function () {
      const curso = document.getElementById('curso-select').value;
      const ano = document.getElementById('ano-input').value;
      const ies = document.getElementById('ies-input').value;

      fetch('/gerar-grafico', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ curso, ano, ies })
      })
        .then(res => {
          if (res.ok) {
            document.querySelector("img[alt^='Gráfico']").src = "/static/graficos/grafico_taxas.png?" + new Date().getTime();
            atualizarDescricaoGrafico(`Gráfico atualizado para o curso ${curso}, ano ${ano}, instituição ${ies}.`);
          } else {
            alert("Nenhum dado encontrado para os filtros informados.");
          }
        })
        .catch(error => {
          console.error('Erro ao buscar gráfico:', error);
          alert("Erro na comunicação com o servidor.");
        });
    });
  }
