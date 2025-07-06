function lerDescricaoGrafico() {
  const texto = document.getElementById('grafico-descricao').textContent;
  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(texto);
  utter.lang = 'pt-BR';
  synth.speak(utter);
}