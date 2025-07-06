<template>
  <div class="admin-layout">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">👨‍💼</div>
          <h1 class="logo-text">Admin Dashboard</h1>
        </div>
        <div class="user-section">
          <div class="user-info">
            <div class="user-name">{{ user?.full_name || 'Admin' }}</div>
            <div class="user-role">Administrator</div>
          </div>
          <button @click="logout" class="logout-btn">
            <span>🚪</span> Logout
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content with Sidebar -->
    <div class="dashboard-content">
      <!-- Fixed Sidebar -->
      <aside class="admin-sidebar">
        <nav class="sidebar-nav">
          <button 
            @click="navigateTo('/admin')" 
            class="nav-item"
            :class="{ active: $route.path === '/admin' }"
          >
            <span>📊</span>
            Dashboard
          </button>
          <button 
            @click="navigateTo('/admin/users')" 
            class="nav-item"
            :class="{ active: $route.path === '/admin/users' }"
          >
            <span>👥</span>
            User Management
          </button>
          <button 
            @click="navigateTo('/admin/subjects')" 
            class="nav-item"
            :class="{ active: $route.path === '/admin/subjects' }"
          >
            <span>📚</span>
            Subject Management
          </button>
          <button 
            @click="navigateTo('/admin/chapters')" 
            class="nav-item"
            :class="{ active: $route.path === '/admin/chapters' }"
          >
            <span>📖</span>
            Chapter Management
          </button>
          <button 
            @click="navigateTo('/admin/quizzes')" 
            class="nav-item"
            :class="{ active: $route.path === '/admin/quizzes' }"
          >
            <span>📝</span>
            Quiz Management
          </button>
          <button 
            @click="navigateTo('/admin/questions')" 
            class="nav-item"
            :class="{ active: $route.path === '/admin/questions' }"
          >
            <span>❓</span>
            Question Management
          </button>
        </nav>
      </aside>

      <!-- Main Content Area -->
      <main class="admin-main">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// User data (you might want to get this from your auth store)
const user = ref({
  full_name: 'Admin User'
});

const navigateTo = (path) => {
  router.push(path);
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  router.push('/login');
};
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
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
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
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
  font-size: 1.5rem;
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
  flex: 1;
  display: flex;
}

.admin-sidebar {
  width: 250px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 80px);
  overflow-y: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.admin-main {
  flex: 1;
  padding: 2rem;
  margin-left: 250px;
  margin-top: 80px;
  width: calc(100vw - 250px);
  max-width: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .dashboard-content {
    flex-direction: column;
  }
  
  .admin-sidebar {
    position: relative;
    width: 100%;
    height: auto;
    margin-left: 0;
  }
  
  .admin-main {
    margin-left: 0;
    width: 100vw;
    max-width: 100vw;
    padding: 1rem;
  }
  
  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem;
  }
  
  .nav-item {
    white-space: nowrap;
    min-width: 120px;
    flex-shrink: 0;
  }
}
</style> 