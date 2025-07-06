<template>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              <path d="M19 15L19.74 17.74L22.5 18.5L19.74 19.26L19 22L18.26 19.26L15.5 18.5L18.26 17.74L19 15Z" fill="currentColor"/>
              <path d="M5 6L5.5 7.5L7 8L5.5 8.5L5 10L4.5 8.5L3 8L4.5 7.5L5 6Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="logo-text">QuizMaster</h1>
        </div>
        <div class="user-section">
          <div class="user-info">
            <span class="user-name">{{ userFullName || 'User' }}</span>
            <span class="user-role">{{ isAdmin ? 'Administrator' : 'Student' }}</span>
          </div>
          <button @click="logout" class="logout-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 17L21 12L16 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <div class="dashboard-content">
      <!-- Sidebar -->
      <aside class="dashboard-sidebar" v-if="isAdmin">
        <nav class="sidebar-nav">
          <button 
            @click="navigateToAdminDashboard" 
            class="nav-item"
          >
            <span>👨‍💼</span>
            Admin Dashboard
          </button>
          <button 
            @click="navigateToUsers" 
            class="nav-item"
          >
            <span>👥</span>
            User Management
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="dashboard-main">
        <template v-if="isAdmin">
          <div class="content-wrapper">
            <div class="welcome-message">
              <h2>Welcome to QuizMaster Admin</h2>
              <p>Use the navigation buttons to access different admin functions.</p>
            </div>
          </div>
        </template>
        <template v-else>
          <QuizView />
        </template>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import QuizView from "./QuizView.vue";


const router = useRouter();
const isAdmin = ref(false);
const userFullName = ref("");

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
};

const navigateToAdminDashboard = () => {
  router.push("/admin");
};

const navigateToUsers = () => {
  router.push("/admin/users");
};

onMounted(() => {
  if (!localStorage.getItem("token")) {
    router.push("/login");
  }
  isAdmin.value = localStorage.getItem("role") === "admin";
  // Get user info from localStorage or set default
  userFullName.value = localStorage.getItem("userFullName") || "User";
});
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  padding: 0.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.95rem;
}

.user-role {
  font-size: 0.8rem;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #e53e3e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #c53030;
  transform: translateY(-1px);
}

.dashboard-content {
  display: flex;
  flex: 1;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  gap: 2rem;
}

.dashboard-sidebar {
  width: 300px;
  flex-shrink: 0;
}

.sidebar-nav {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border: none;
  background: transparent;
  color: #4a5568;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;
}

.nav-item:hover {
  background: rgba(66, 153, 225, 0.1);
  color: #3182ce;
  transform: translateX(4px);
}

.nav-item.active {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
}

.dashboard-main {
  flex: 1;
  min-width: 0;
}

.content-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  min-height: calc(100vh - 200px);
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.welcome-message {
  text-align: center;
  padding: 3rem 1rem;
}

.welcome-message h2 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.welcome-message p {
  font-size: 1.1rem;
  color: #718096;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .dashboard-content {
    flex-direction: column;
    padding: 1rem;
  }
  
  .dashboard-sidebar {
    width: 100%;
  }
  
  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 1rem;
  }
  
  .nav-item {
    white-space: nowrap;
    min-width: 120px;
  }
}

@media (min-width: 1400px) {
  .dashboard-content {
    padding: 2rem 3rem;
  }
  
  .content-wrapper {
    padding: 3rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .user-section {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .user-info {
    align-items: center;
  }
  
  .dashboard-content {
    padding: 0.5rem;
  }
  
  .content-wrapper {
    padding: 1rem;
  }
}

/* Animation for page transitions */
.content-wrapper > * {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
