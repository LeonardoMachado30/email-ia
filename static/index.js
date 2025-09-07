const form = document.getElementById("emailForm");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const email_file = document.getElementById("email_file");
const email_content = document.getElementById("email_content");
const btnRemoveFile = document.getElementById("btnRemoveFile");
const resultadoContainer = document.getElementById("resultadoContainer");
const clearAllBtn = document.getElementById("clearAllBtn");

const clearRemetente = document.getElementById("clearRemetente");
const clearTitulo = document.getElementById("clearTitulo");
const clearTextareaBtn = document.getElementById("clearTextareaBtn");

const historyBtn = document.getElementById("historyBtn");
const historyModal = document.getElementById("historyModal");
const historyList = document.getElementById("historyList");
const closeHistory = document.getElementById("closeHistory");

function toggleClearButtons() {
  clearRemetente.disabled = !document.getElementById("remetente").value;
  clearTitulo.disabled = !document.getElementById("titulo").value;
  clearTextareaBtn.disabled = !email_content.value;
}

document
  .getElementById("remetente")
  .addEventListener("input", toggleClearButtons);
document.getElementById("titulo").addEventListener("input", toggleClearButtons);
email_content.addEventListener("input", toggleClearButtons);

clearRemetente.addEventListener("click", () => {
  document.getElementById("remetente").value = "";
  toggleClearButtons();
});
clearTitulo.addEventListener("click", () => {
  document.getElementById("titulo").value = "";
  toggleClearButtons();
});
clearTextareaBtn.addEventListener("click", () => {
  email_content.value = "";
  toggleClearButtons();
});

email_file.addEventListener("change", (e) => {
  if (e.target.value) {
    email_content.disabled = true;
    email_content.value = "";
    btnRemoveFile.disabled = false;
  } else {
    email_content.disabled = false;
    btnRemoveFile.disabled = true;
  }
  toggleClearButtons();
});

btnRemoveFile.addEventListener("click", (e) => {
  e.preventDefault();
  email_file.value = null;
  const event = new Event("change");
  email_file.dispatchEvent(event);
});

function loadHistory() {
  const history = JSON.parse(localStorage.getItem("history") || "[]");
  historyList.innerHTML = "";
  history.forEach((item, index) => {
    const div = document.createElement("div");
    div.classList.add("history-item");
    div.innerHTML = `
            <span>${item.categoria} - ${item.resposta_sugerida.substring(
      0,
      50
    )}...</span>
            <span class="history-remove" data-index="${index}">X</span>
          `;
    div.addEventListener("click", (e) => {
      if (e.target.classList.contains("history-remove")) return;
      document.getElementById("remetente").value = item.remetente || "";
      document.getElementById("titulo").value = item.titulo || "";
      email_content.value = item.email_content || "";
      resultadoContainer.innerHTML = `
              <div class="resultado">
                <h2>Resultado da Análise</h2>
                <p><strong>Categoria:</strong> ${item.categoria}</p>
                <p><strong>Resposta Sugerida:</strong></p>
                <p>${item.resposta_sugerida}</p>
              </div>
            `;
      toggleClearButtons();
      historyModal.style.display = "none";
    });
    historyList.appendChild(div);
  });
  document.querySelectorAll(".history-remove").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = e.target.dataset.index;
      let history = JSON.parse(localStorage.getItem("history") || "[]");
      history.splice(idx, 1);
      localStorage.setItem("history", JSON.stringify(history));
      loadHistory();
    });
  });
}

historyBtn.addEventListener("click", () => {
  loadHistory();
  historyModal.style.display = "flex";
});

closeHistory.addEventListener("click", () => {
  historyModal.style.display = "none";
});

clearAllBtn.addEventListener("click", () => {
  localStorage.removeItem("history");
  loadHistory();
  resultadoContainer.innerHTML = "";
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  submitBtn.disabled = true;
  btnText.innerHTML = `<div class="loader"></div>`;

  const formData = new FormData(form);

  const jsonData = Object.fromEntries(formData);
  const jsonString = JSON.stringify(jsonData);

  console.log(jsonData); // Objeto JavaScript
  console.log(jsonString); // String JSON

  clearAllBtn.disabled = true;
  document.getElementById("remetente").disabled = true;
  document.getElementById("titulo").disabled = true;
  email_content.disabled = true;
  try {
    const response = await fetch("/processar", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Erro na requisição");

    const result = await response.json();

    const history = JSON.parse(localStorage.getItem("history") || "[]");
    history.push({
      categoria: result.categoria,
      resposta_sugerida: result.resposta_sugerida,
      email_content: result.email_content,
      remetente: result.remetente,
      titulo: result.titulo,
    });
    localStorage.setItem("history", JSON.stringify(history));

    // Limpa o container antes de adicionar novo resultado
    resultadoContainer.innerHTML = "";

    // Cria o elemento principal do resultado
    const resultadoDiv = document.createElement("div");
    resultadoDiv.className = "resultado";
    resultadoDiv.style.position = "relative";

    // Título
    const titulo = document.createElement("h2");
    titulo.textContent = "Resultado da Análise";
    resultadoDiv.appendChild(titulo);

    // Categoria
    const categoriaP = document.createElement("p");
    categoriaP.innerHTML = `<strong>Categoria:</strong> ${result.categoria}`;
    resultadoDiv.appendChild(categoriaP);

    // Resposta Sugerida label
    const respostaLabel = document.createElement("p");
    respostaLabel.innerHTML = "<strong>Resposta Sugerida:</strong>";
    resultadoDiv.appendChild(respostaLabel);

    // Resposta Sugerida texto
    const respostaTexto = document.createElement("p");
    respostaTexto.textContent = result.resposta_sugerida;
    respostaTexto.style.whiteSpace = "pre-line";
    respostaTexto.id = "respostaSugeridaTexto";
    resultadoDiv.appendChild(respostaTexto);

    // Botão flutuante de copiar
    const copiarBtn = document.createElement("button");
    copiarBtn.textContent = "Copiar";
    copiarBtn.title = "Copiar resposta sugerida";
    copiarBtn.style.position = "absolute";
    copiarBtn.style.top = "10px";
    copiarBtn.style.right = "10px";
    copiarBtn.style.padding = "6px 12px";
    copiarBtn.style.background = "#5e02b4";
    copiarBtn.style.color = "#fff";
    copiarBtn.style.border = "none";
    copiarBtn.style.borderRadius = "4px";
    copiarBtn.style.cursor = "pointer";
    copiarBtn.style.zIndex = "10";
    copiarBtn.style.fontSize = "13px";
    copiarBtn.style.boxShadow = "0 2px 6px rgba(0,0,0,0.08)";

    copiarBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(result.resposta_sugerida);
        copiarBtn.textContent = "Copiado!";
        setTimeout(() => {
          copiarBtn.textContent = "Copiar";
        }, 1200);
      } catch (e) {
        copiarBtn.textContent = "Erro ao copiar";
        setTimeout(() => {
          copiarBtn.textContent = "Copiar";
        }, 1200);
      }
    });

    resultadoDiv.appendChild(copiarBtn);

    // Adiciona o resultado ao container
    resultadoContainer.appendChild(resultadoDiv);
    toggleClearButtons();
  } catch (err) {
    resultadoContainer.innerHTML = `<p style="color:red;">${err}</p>`;
  } finally {
    submitBtn.disabled = false;
    btnText.innerHTML = "Gerar E-mail";
    clearAllBtn.disabled = false;
    document.getElementById("remetente").disabled = false;
    document.getElementById("titulo").disabled = false;
    email_content.disabled = false;
    toggleClearButtons();
  }
});
