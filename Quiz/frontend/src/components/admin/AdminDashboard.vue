<template>
  <div class="admin-dashboard">
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
        <!-- Stats Overview -->
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-value">{{ stats.totalUsers }}</div>
            <div class="stat-label">Total Users</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-value">{{ stats.totalQuizzes }}</div>
            <div class="stat-label">Total Quizzes</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📚</div>
            <div class="stat-value">{{ stats.totalSubjects }}</div>
            <div class="stat-label">Total Subjects</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📖</div>
            <div class="stat-value">{{ stats.totalChapters }}</div>
            <div class="stat-label">Total Chapters</div>
          </div>
        </div>

        <!-- Navigation Cards -->
        <div class="nav-cards">
          <div class="nav-card" @click="navigateTo('/admin/users')">
            <div class="nav-icon">👥</div>
            <h3>User Management</h3>
            <p>Manage users, view details, and control access</p>
          </div>
          <div class="nav-card" @click="navigateTo('/admin/quizzes')">
            <div class="nav-icon">📝</div>
            <h3>Quiz Management</h3>
            <p>Create, edit, and manage quizzes</p>
          </div>
          <div class="nav-card" @click="navigateTo('/admin/subjects')">
            <div class="nav-icon">📚</div>
            <h3>Subject Management</h3>
            <p>Manage subjects and chapters</p>
          </div>
          <div class="nav-card" @click="navigateTo('/admin/questions')">
            <div class="nav-icon">❓</div>
            <h3>Question Management</h3>
            <p>Create and manage quiz questions</p>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="recent-activity">
          <h2>Recent Activity</h2>
          <div class="activity-list">
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon">{{ activity.icon }}</div>
              <div class="activity-content">
                <div class="activity-text">{{ activity.text }}</div>
                <div class="activity-time">{{ formatTime(activity.time) }}</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { listUsers, getQuizzes, getSubjects, getChapters } from '../../api';

const router = useRouter();

// Reactive data
const stats = ref({
  totalUsers: 0,
  totalQuizzes: 0,
  totalSubjects: 0,
  totalChapters: 0
});

const recentActivities = ref([
  {
    id: 1,
    icon: '👤',
    text: 'New user registered: John Doe',
    time: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
  },
  {
    id: 2,
    icon: '📝',
    text: 'Quiz "Mathematics Basics" created',
    time: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 hours ago
  },
  {
    id: 3,
    icon: '📚',
    text: 'New subject "Physics" added',
    time: new Date(Date.now() - 1000 * 60 * 60 * 4) // 4 hours ago
  }
]);

// User data (you might want to get this from your auth store)
const user = ref({
  full_name: 'Admin User'
});

// Methods
const fetchStats = async () => {
  try {
    const [users, quizzes, subjects, chapters] = await Promise.all([
      listUsers(),
      getQuizzes(),
      getSubjects(),
      getChapters()
    ]);

    stats.value = {
      totalUsers: users.length,
      totalQuizzes: quizzes.length,
      totalSubjects: subjects.length,
      totalChapters: chapters.length
    };
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
};

const navigateTo = (path) => {
  router.push(path);
};

const logout = () => {
  // Implement logout logic
  localStorage.removeItem('token');
  router.push('/login');
};

const formatTime = (time) => {
  const now = new Date();
  const diff = now - time;
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (minutes < 60) return `${minutes} minutes ago`;
  if (hours < 24) return `${hours} hours ago`;
  return `${days} days ago`;
};

onMounted(() => {
  fetchStats();
});
</script>

<style scoped>
.admin-dashboard {
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
  width: calc(100vw - 250px);
  max-width: none;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  text-align: center;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.nav-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  text-align: center;
}

.nav-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  background: rgba(66, 153, 225, 0.05);
}

.nav-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.nav-card h3 {
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.nav-card p {
  color: #718096;
  margin: 0;
  font-size: 0.9rem;
}

.recent-activity {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.recent-activity h2 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateX(5px);
}

.activity-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(66, 153, 225, 0.1);
  border-radius: 8px;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #2d3748;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.activity-time {
  color: #718096;
  font-size: 0.8rem;
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
  
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .nav-cards {
    grid-template-columns: 1fr;
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