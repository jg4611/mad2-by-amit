<template>
  <div class="login-container">
    <form class="login-form" @submit.prevent="handleRegister">
      <h2>User Register</h2>
      <input v-model="name" placeholder="Name" required />
      <input v-model="email" placeholder="Email" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />
      <button type="submit">Register</button>
      <p v-if="error" class="error-msg">{{ error }}</p>
      <p v-if="success" class="success-msg">{{ success }}</p>
      <div v-if="success" class="login-links">
        <router-link to="/login" class="login-link">Go to Login</router-link>
      </div>
      <div class="register-links">
        <span>Already have an account? </span>
        <router-link to="/login" class="login-link">Login here</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const success = ref("");
const router = useRouter();

const handleRegister = async () => {
  error.value = "";
  success.value = "";
  try {
    const res = await fetch("http://127.0.0.1:5006/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: name.value,
        email: email.value,
        password: password.value,
      }),
    });
    if (!res.ok) {
      const data = await res.json();
      error.value = data.message || "Registration failed.";
      return;
    }
    success.value = "Registration successful! You can now log in.";
    name.value = "";
    email.value = "";
    password.value = "";
    
    // Optionally auto-redirect to login after 2 seconds
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (e) {
    error.value = "Network error. Please try again.";
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
}
.login-form {
  background: #fff;
  padding: 2.5rem 2rem;
  border-radius: 1.2rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  width: 340px;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}
.login-form h2 {
  margin-bottom: 0.5rem;
  color: #3182ce;
  font-weight: 700;
}
.login-form input {
  padding: 0.7rem;
  border-radius: 0.5rem;
  border: 1px solid #cbd5e1;
  font-size: 1rem;
}
.login-form button {
  background: linear-gradient(90deg, #3182ce 0%, #63b3ed 100%);
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  padding: 0.7rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.login-form button:hover {
  background: linear-gradient(90deg, #2563eb 0%, #4299e1 100%);
}
.error-msg {
  color: #e53e3e;
  font-size: 0.95em;
  margin-top: -0.5rem;
}
.success-msg {
  color: #38a169;
  font-size: 0.95em;
  margin-top: -0.5rem;
}
.login-links {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}
.register-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  font-size: 0.9em;
  color: #64748b;
}
.login-link {
  color: #3182ce;
  font-size: 0.98em;
  text-decoration: underline;
  cursor: pointer;
  font-weight: 600;
}
.login-link:hover {
  color: #2563eb;
}
</style>
