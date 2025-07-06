// Centralized API utility for admin dashboard
const API_BASE = "http://127.0.0.1:5006";

function getToken() {
  return localStorage.getItem("token");
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiFetch(path, options = {}) {
  const token = getToken();
  if (!token) {
    window.location.href = "/login";
    throw new Error("No token");
  }
  const headers = { ...(options.headers || {}), ...authHeaders() };
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const error = new Error(
      errorData.message || `HTTP error! status: ${res.status}`
    );
    error.status = res.status;
    error.response = { data: errorData };
    throw error;
  }

  return res.json();
}

// Subjects
export const getSubjects = () => apiFetch("/api/subjects");
export const createSubject = (data) =>
  apiFetch("/create_subjects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const updateSubject = (id, data) =>
  apiFetch(`/update_subjects/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const deleteSubject = (id) =>
  apiFetch(`/delete_subjects/${id}`, { method: "DELETE" });

// Chapters
export const getChapters = () => apiFetch("/api/chapters");
export const createChapter = (data) =>
  apiFetch("/create_chapters", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const updateChapter = (id, data) =>
  apiFetch(`/update_chapters/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const deleteChapter = (id) =>
  apiFetch(`/delete_chapters/${id}`, { method: "DELETE" });

// Quizzes
export const getQuizzes = () => apiFetch("/api/quizzes");
export const createQuiz = (data) =>
  apiFetch("/create_quizzes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const updateQuiz = (id, data) =>
  apiFetch(`/update_quizzes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const deleteQuiz = (id) =>
  apiFetch(`/delete_quizzes/${id}`, { method: "DELETE" });
export const toggleQuiz = (id) =>
  apiFetch(`/toggle_quiz/${id}`, { method: "POST" });
export const getAvailableQuizzes = () => apiFetch("/available_quizzes");
export const getQuizDetails = (quizId) => apiFetch(`/api/quizzes/${quizId}`);
export const submitQuiz = (payload) =>
  apiFetch("/api/submit-quiz", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
export const getQuizHistory = () => apiFetch("/api/quiz-history");

// Questions
export const getQuestions = () => apiFetch("/api/questions");
export const createQuestion = (data) =>
  apiFetch("/create_questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const updateQuestion = (id, data) =>
  apiFetch(`/update_questions/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const deleteQuestion = (id) =>
  apiFetch(`/delete_questions/${id}`, { method: "DELETE" });

// Users
export const listUsers = () => apiFetch("/list_users");
export const createUser = (data) =>
  apiFetch("/create_users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const updateUser = (id, data) =>
  apiFetch(`/update_users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
export const deleteUser = (id) =>
  apiFetch(`/delete_users/${id}`, { method: "DELETE" });
