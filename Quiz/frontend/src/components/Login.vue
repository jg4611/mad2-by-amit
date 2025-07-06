<template>
  <div class="login-container">
    <form class="login-form" @submit.prevent="handleLogin">
      <h2>{{ isAdmin ? "Admin Login" : "User Login" }}</h2>
      <input v-model="email" placeholder="Email" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
      <p v-if="error" class="error-msg">{{ error }}</p>
      <div class="login-links">
        <a href="#" @click.prevent="toggleMode">
          {{ isAdmin ? "Switch to User Login" : "Switch to Admin Login" }}
        </a>
        <router-link v-if="!isAdmin" to="/register">Register</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const error = ref("");
const isAdmin = ref(true);
const router = useRouter();

const toggleMode = () => {
  isAdmin.value = !isAdmin.value;
  error.value = "";
};

const handleLogin = async () => {
  error.value = "";
  try {
    // Always use /login for both admin and user
    const url = "http://127.0.0.1:5006/login";
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });
    if (res.status === 401) {
      error.value = "Invalid credentials.";
      return;
    }
    if (!res.ok) {
      error.value = "Login failed. Please try again.";
      return;
    }
    const data = await res.json();
    if (data && data.access_token) {
      localStorage.setItem("token", data.access_token);
      if (data.user && data.user.role) {
        localStorage.setItem("role", data.user.role);
      }
      if (data.user && data.user.full_name) {
        localStorage.setItem("userFullName", data.user.full_name);
      }
      
      // Redirect based on user role
      if (data.user && data.user.role === "admin") {
        router.push("/admin");
      } else {
        router.push("/");
      }
    } else {
      error.value = "Login failed. No token received.";
    }
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
  padding: 2.5em 2em 2em 2em;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.2em;
  min-width: 320px;
}
.login-form h2 {
  text-align: center;
  color: #2d3748;
  margin-bottom: 0.5em;
  font-weight: 700;
  letter-spacing: 1px;
}
.login-form input {
  padding: 0.7em 1em;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1em;
  background: #f9fafb;
  transition: border 0.2s;
}
.login-form input:focus {
  border: 1.5px solid #3182ce;
  outline: none;
}
.login-form button {
  background: linear-gradient(90deg, #3182ce 0%, #63b3ed 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7em 1.5em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.login-form button:hover {
  background: linear-gradient(90deg, #2563eb 0%, #4299e1 100%);
}
.error-msg {
  color: #c53030;
  text-align: center;
  margin-top: 0.5em;
  font-size: 1em;
}
.login-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -0.5em;
}
.login-links a,
.login-links .router-link-active {
  color: #3182ce;
  font-size: 0.98em;
  text-decoration: underline;
  cursor: pointer;
}
</style>
