<template>
  <AdminLayout>
    <div class="container-fluid py-4 bg-light min-vh-100">
      <div class="card shadow-lg border-0 mx-auto mb-4" style="max-width: 900px">
        <div class="card-body">
          <h2 class="text-center mb-4 fw-bold text-primary">
            Subjects Management
          </h2>
          <h5 class="fw-semibold mb-3">Add New Subject</h5>
          <form
            class="row g-3 align-items-end"
            @submit.prevent="createSubjectHandler"
          >
            <div class="col-md-6">
              <label class="form-label fw-semibold">Subject Name</label>
              <input
                v-model="newSubject.name"
                class="form-control"
                placeholder="Subject Name"
                required
              />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Description</label>
              <input
                v-model="newSubject.description"
                class="form-control"
                placeholder="Subject Description"
              />
            </div>
            <div class="col-md-2">
              <button
                type="submit"
                class="btn btn-gradient-primary btn-sm w-100 fw-bold"
              >
                <i class="bi bi-plus-circle me-2"></i>Add Subject
              </button>
            </div>
          </form>
        </div>
      </div>
      <div class="card shadow-lg border-0 mx-auto" style="max-width: 1400px">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">All Subjects</h5>
          <div class="table-responsive">
            <table
              class="table table-hover align-middle bg-white rounded shadow-sm"
            >
              <thead class="table-primary sticky-top">
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Chapters</th>
                  <th class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="subject in subjects" :key="subject.id">
                  <template v-if="editId !== subject.id">
                    <td class="fw-semibold">{{ subject.name }}</td>
                    <td>{{ subject.description || 'No description' }}</td>
                    <td>{{ subject.chapters?.length || 0 }} chapters</td>
                    <td class="text-center">
                      <button
                        class="btn btn-outline-primary btn-sm me-2"
                        @click="editSubject(subject)"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                        class="btn btn-outline-danger btn-sm"
                        @click="deleteSubjectHandler(subject.id)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </template>
                  <template v-else>
                    <td>
                      <input
                        v-model="editSubjectData.name"
                        class="form-control form-control-sm"
                      />
                    </td>
                    <td>
                      <input
                        v-model="editSubjectData.description"
                        class="form-control form-control-sm"
                      />
                    </td>
                    <td>{{ subject.chapters?.length || 0 }} chapters</td>
                    <td class="text-center">
                      <button
                        class="btn btn-success btn-sm me-2"
                        @click="updateSubjectHandler(subject.id)"
                      >
                        <i class="bi bi-check-circle"></i> Save
                      </button>
                      <button
                        class="btn btn-secondary btn-sm"
                        @click="cancelEdit"
                      >
                        <i class="bi bi-x-circle"></i> Cancel
                      </button>
                    </td>
                  </template>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getSubjects,
  createSubject,
  updateSubject,
  deleteSubject,
} from "../../api";
import AdminLayout from './AdminLayout.vue';

const subjects = ref([]);
const newSubject = ref({ name: "", description: "" });
const editId = ref(null);
const editSubjectData = ref({ name: "", description: "" });

const fetchSubjects = async () => {
  subjects.value = await getSubjects();
};

const createSubjectHandler = async () => {
  await createSubject(newSubject.value);
  newSubject.value = { name: "", description: "" };
  fetchSubjects();
};

const deleteSubjectHandler = async (id) => {
  await deleteSubject(id);
  fetchSubjects();
};

const updateSubjectHandler = async (id) => {
  await updateSubject(id, editSubjectData.value);
  editId.value = null;
  fetchSubjects();
};

const editSubject = (subject) => {
  editId.value = subject.id;
  editSubjectData.value = { ...subject };
};

const cancelEdit = () => {
  editId.value = null;
};

onMounted(fetchSubjects);
</script>

<style scoped>
@import "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css";
@import "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css";

.btn-gradient-primary {
  background: linear-gradient(90deg, #3182ce 0%, #63b3ed 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7em 1.7em;
  font-weight: 600;
  transition: background 0.2s;
}
.btn-gradient-primary:hover {
  background: linear-gradient(90deg, #2563eb 0%, #4299e1 100%);
}
.card {
  border-radius: 1.5rem;
}
.table {
  border-radius: 1rem;
  overflow: hidden;
}
.table thead th {
  vertical-align: middle;
  font-size: 1.08em;
}
.table tbody td {
  vertical-align: middle;
}
.sticky-top {
  position: sticky;
  top: 0;
  z-index: 2;
}
</style>
