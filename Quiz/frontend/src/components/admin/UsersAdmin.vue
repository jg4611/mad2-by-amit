<template>
  <AdminLayout>
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">User Management</h1>
          <p class="page-subtitle">Manage all users in the system</p>
        </div>
        <div class="header-right">
          <button @click="showCreateModal = true" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New User
          </button>
        </div>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="filters-section">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search users by name or email..."
          class="search-input"
        />
        <i class="fas fa-search search-icon"></i>
      </div>
      <div class="filter-options">
        <select v-model="roleFilter" class="filter-select">
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="user">User</option>
        </select>
      </div>
    </div>

    <!-- Users Table -->
    <div class="table-container">
      <div class="table-header">
        <h3>All Users ({{ filteredUsers.length }})</h3>
        <button @click="refreshUsers" class="btn btn-secondary btn-sm">
          <i class="fas fa-sync-alt"></i> Refresh
        </button>
      </div>
      
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading users...</p>
      </div>
      
      <div v-else-if="filteredUsers.length === 0" class="empty-state">
        <div class="empty-icon"><i class="fas fa-users"></i></div>
        <h3>No Users Found</h3>
        <p>{{ searchQuery || roleFilter ? 'Try adjusting your search or filters.' : 'No users have been created yet.' }}</p>
      </div>
      
      <div v-else class="users-table">
        <table class="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Qualification</th>
              <th>Date of Birth</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id" class="user-row">
              <td>
                <div class="user-info">
                  <div class="user-avatar">{{ getUserInitials(user.full_name) }}</div>
                  <div class="user-details">
                    <div class="user-name">{{ user.full_name || 'N/A' }}</div>
                    <div class="user-id">ID: {{ user.id }}</div>
                  </div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span class="role-badge" :class="getRoleBadgeClass(user.role)">
                  {{ user.role }}
                </span>
              </td>
              <td>{{ user.qualification || 'N/A' }}</td>
              <td>{{ formatDate(user.date_of_birth) }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="viewUser(user)" class="btn btn-sm btn-info" title="View Details">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button @click="editUser(user)" class="btn btn-sm btn-warning" title="Edit User">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="deleteUser(user.id)" class="btn btn-sm btn-danger" title="Delete User">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="filteredUsers.length > itemsPerPage" class="pagination">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="btn btn-secondary btn-sm"
        >
          ← Previous
        </button>
        <span class="page-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="btn btn-secondary btn-sm"
        >
          Next →
        </button>
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Create New User</h3>
          <button @click="showCreateModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="createUser" class="modal-body">
          <div class="form-group">
            <label>Full Name *</label>
            <input v-model="newUser.full_name" type="text" required class="form-control" />
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="newUser.email" type="email" required class="form-control" />
          </div>
          <div class="form-group">
            <label>Password *</label>
            <input v-model="newUser.password" type="password" required class="form-control" />
          </div>
          <div class="form-group">
            <label>Role *</label>
            <select v-model="newUser.role" required class="form-control">
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="form-group">
            <label>Qualification</label>
            <input v-model="newUser.qualification" type="text" class="form-control" />
          </div>
          <div class="form-group">
            <label>Date of Birth</label>
            <input v-model="newUser.date_of_birth" type="date" class="form-control" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="creating">
              {{ creating ? 'Creating...' : 'Create User' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Edit User</h3>
          <button @click="showEditModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="updateUser" class="modal-body">
          <div class="form-group">
            <label>Full Name *</label>
            <input v-model="editingUser.full_name" type="text" required class="form-control" />
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="editingUser.email" type="email" required class="form-control" />
          </div>
          <div class="form-group">
            <label>New Password (leave blank to keep current)</label>
            <input v-model="editingUser.password" type="password" class="form-control" />
          </div>
          <div class="form-group">
            <label>Role *</label>
            <select v-model="editingUser.role" required class="form-control">
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="form-group">
            <label>Qualification</label>
            <input v-model="editingUser.qualification" type="text" class="form-control" />
          </div>
          <div class="form-group">
            <label>Date of Birth</label>
            <input v-model="editingUser.date_of_birth" type="date" class="form-control" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="updating">
              {{ updating ? 'Updating...' : 'Update User' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- View User Modal -->
    <div v-if="showViewModal" class="modal-overlay" @click="showViewModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>User Details</h3>
          <button @click="showViewModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="user-profile">
            <div class="profile-avatar">{{ getUserInitials(viewingUser.full_name) }}</div>
            <div class="profile-info">
              <h4>{{ viewingUser.full_name || 'N/A' }}</h4>
              <p class="user-email">{{ viewingUser.email }}</p>
              <span class="role-badge" :class="getRoleBadgeClass(viewingUser.role)">
                {{ viewingUser.role }}
              </span>
            </div>
          </div>
          <div class="user-details-grid">
            <div class="detail-item">
              <label>User ID</label>
              <span>{{ viewingUser.id }}</span>
            </div>
            <div class="detail-item">
              <label>Qualification</label>
              <span>{{ viewingUser.qualification || 'Not specified' }}</span>
            </div>
            <div class="detail-item">
              <label>Date of Birth</label>
              <span>{{ formatDate(viewingUser.date_of_birth) || 'Not specified' }}</span>
            </div>
            <div class="detail-item">
              <label>Account Created</label>
              <span>{{ formatDate(viewingUser.created_at) || 'Unknown' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { createUser as createUserAPI, updateUser as updateUserAPI, deleteUser as deleteUserAPI, listUsers } from '../../api';
import AdminLayout from './AdminLayout.vue';

// Reactive data
const users = ref([]);
const loading = ref(false);
const creating = ref(false);
const updating = ref(false);
const searchQuery = ref('');
const roleFilter = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);

// Modal states
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showViewModal = ref(false);

// Form data
const newUser = ref({
  full_name: '',
  email: '',
  password: '',
  role: 'user',
  qualification: '',
  date_of_birth: ''
});

const editingUser = ref({});
const viewingUser = ref({});

// Computed properties
const filteredUsers = computed(() => {
  let filtered = users.value;
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(user => 
      user.full_name?.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    );
  }
  
  if (roleFilter.value) {
    filtered = filtered.filter(user => user.role === roleFilter.value);
  }
  
  return filtered;
});

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage.value));

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredUsers.value.slice(start, end);
});

// Methods
const fetchUsers = async () => {
  loading.value = true;
  try {
    users.value = await listUsers();
  } catch (error) {
    console.error('Error fetching users:', error);
  } finally {
    loading.value = false;
  }
};

const refreshUsers = () => {
  fetchUsers();
};

const createUser = async () => {
  creating.value = true;
  try {
    await createUserAPI(newUser.value);
    showCreateModal.value = false;
    newUser.value = {
      full_name: '',
      email: '',
      password: '',
      role: 'user',
      qualification: '',
      date_of_birth: ''
    };
    fetchUsers();
  } catch (error) {
    console.error('Error creating user:', error);
  } finally {
    creating.value = false;
  }
};

const editUser = (user) => {
  editingUser.value = { ...user };
  showEditModal.value = true;
};

const updateUser = async () => {
  updating.value = true;
  try {
    const payload = { ...editingUser.value };
    if (!payload.password) {
      delete payload.password;
    }
    await updateUserAPI(editingUser.value.id, payload);
    showEditModal.value = false;
    fetchUsers();
  } catch (error) {
    console.error('Error updating user:', error);
  } finally {
    updating.value = false;
  }
};

const deleteUser = async (userId) => {
  if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
    try {
      await deleteUserAPI(userId);
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  }
};

const viewUser = (user) => {
  viewingUser.value = { ...user };
  showViewModal.value = true;
};

const getUserInitials = (name) => {
  if (!name) return '?';
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
};

const getRoleBadgeClass = (role) => {
  return role === 'admin' ? 'role-admin' : 'role-user';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};

// Watch for filter changes
const watchFilters = () => {
  currentPage.value = 1;
};

// Lifecycle
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

.page-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
}

.page-subtitle {
  color: #718096;
  margin: 0;
}

.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
}

.search-box {
  position: relative;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.9);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #718096;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
}

.table-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.table-header h3 {
  color: #2d3748;
  margin: 0;
}

.users-table {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.table th {
  background: rgba(66, 153, 225, 0.1);
  font-weight: 600;
  color: #2d3748;
}

.user-row:hover {
  background: rgba(66, 153, 225, 0.05);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.user-name {
  font-weight: 600;
  color: #2d3748;
}

.user-id {
  font-size: 0.8rem;
  color: #718096;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.role-admin {
  background: rgba(245, 101, 101, 0.1);
  color: #c53030;
}

.role-user {
  background: rgba(72, 187, 120, 0.1);
  color: #38a169;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
}

.btn-secondary {
  background: rgba(113, 128, 150, 0.1);
  color: #4a5568;
}

.btn-info {
  background: rgba(66, 153, 225, 0.1);
  color: #3182ce;
}

.btn-warning {
  background: rgba(237, 137, 54, 0.1);
  color: #dd6b20;
}

.btn-danger {
  background: rgba(245, 101, 101, 0.1);
  color: #e53e3e;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.page-info {
  color: #718096;
  font-weight: 500;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #718096;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(66, 153, 225, 0.1);
  border-left: 4px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: #2d3748;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #2d3748;
}

.modal-body {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2d3748;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

/* User Profile Styles */
.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.profile-avatar {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.2rem;
}

.profile-info h4 {
  margin: 0 0 0.25rem 0;
  color: #2d3748;
}

.user-email {
  color: #718096;
  margin: 0 0 0.5rem 0;
}

.user-details-grid {
  display: grid;
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item label {
  font-weight: 600;
  color: #2d3748;
}

.detail-item span {
  color: #718096;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .table-container {
    padding: 1rem;
  }
  
  .users-table {
    font-size: 0.9rem;
  }
  
  .table th,
  .table td {
    padding: 0.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .modal-content {
    margin: 1rem;
  }
}
</style> 