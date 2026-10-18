const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");
menuToggle.addEventListener("click", () => {
  const open = navLinks.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(open));
});
navLinks.querySelectorAll("a").forEach(a => a.addEventListener("click", () => {
  navLinks.classList.remove("open");
  menuToggle.setAttribute("aria-expanded", "false");
}));
document.getElementById("year").textContent = new Date().getFullYear();

const chatBody = document.getElementById("chatBody");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatStatus = document.getElementById("chatStatus");

function addMessage(text, role) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}
async function sendChat(text) {
  if (!text.trim()) return;
  addMessage(text, "user");
  chatStatus.textContent = "Asking the backend...";
  document.querySelectorAll(".suggestions").forEach(el => el.remove());
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Request failed.");
    addMessage(data.reply, "bot");
    chatStatus.textContent = "Connected to Flask backend · Demo replies";
  } catch (error) {
    addMessage("Could not reach the backend. Please make sure the Flask app is running.", "bot");
    chatStatus.textContent = error.message;
  }
}
chatForm.addEventListener("submit", event => {
  event.preventDefault();
  const value = chatInput.value.trim();
  if (!value) return;
  chatInput.value = "";
  sendChat(value);
});
document.querySelectorAll(".suggestions button").forEach(button => {
  button.addEventListener("click", () => sendChat(button.dataset.message));
});

const contactForm = document.getElementById("contactForm");
const contactStatus = document.getElementById("contactStatus");
contactForm.addEventListener("submit", async event => {
  event.preventDefault();
  contactStatus.textContent = "Sending...";
  const form = new FormData(contactForm);
  const payload = {
    name: form.get("name"),
    email: form.get("email"),
    message: form.get("message")
  };
  try {
    const response = await fetch("/api/contact", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not send message.");
    contactStatus.textContent = data.message;
    contactForm.reset();
  } catch (error) {
    contactStatus.textContent = error.message;
  }
});
