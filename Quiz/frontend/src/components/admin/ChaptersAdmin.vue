<template>
  <AdminLayout>
    <div class="container-fluid py-4 bg-light min-vh-100">
      <div class="card shadow-lg border-0 mx-auto mb-4" style="max-width: 900px">
        <div class="card-body">
          <h2 class="text-center mb-4 fw-bold text-primary">
            Chapters Management
          </h2>
          <h5 class="fw-semibold mb-3">Add New Chapter</h5>
          <form
            class="row g-3 align-items-end"
            @submit.prevent="createChapterHandler"
          >
            <div class="col-md-4">
              <label class="form-label fw-semibold">Subject</label>
              <select v-model="newChapter.subject_id" class="form-select" required>
                <option disabled value="">Select Subject</option>
                <option
                  v-for="subject in subjects"
                  :key="subject.id"
                  :value="subject.id"
                >
                  {{ subject.name }}
                </option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Chapter Name</label>
              <input
                v-model="newChapter.name"
                class="form-control"
                placeholder="Chapter Name"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Description</label>
              <input
                v-model="newChapter.description"
                class="form-control"
                placeholder="Chapter Description"
              />
            </div>
            <div class="col-md-1">
              <button
                type="submit"
                class="btn btn-gradient-primary btn-sm w-100 fw-bold"
              >
                <i class="bi bi-plus-circle me-2"></i>Add
              </button>
            </div>
          </form>
        </div>
      </div>
      <div class="card shadow-lg border-0 mx-auto" style="max-width: 1400px">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-semibold mb-0">All Chapters</h5>
            <div class="d-flex align-items-center">
              <div class="input-group" style="width: 300px;">
                <span class="input-group-text bg-white border-end-0">
                  <i class="bi bi-search text-muted"></i>
                </span>
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control border-start-0"
                  placeholder="Search chapters..."
                  @input="filterChapters"
                />
              </div>
              <button
                v-if="searchQuery"
                @click="clearSearch"
                class="btn btn-outline-secondary btn-sm ms-2"
                title="Clear search"
              >
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
          </div>
          <div class="table-responsive">
            <table
              class="table table-hover align-middle bg-white rounded shadow-sm"
            >
              <thead class="table-primary sticky-top">
                <tr>
                  <th>Subject</th>
                  <th>Chapter Name</th>
                  <th>Description</th>
                  <th>Quizzes</th>
                  <th class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in filteredChapters" :key="chapter.id">
                  <template v-if="editId !== chapter.id">
                    <td class="fw-semibold">{{ getSubjectName(chapter.subject_id) }}</td>
                    <td>{{ chapter.name }}</td>
                    <td>{{ chapter.description || 'No description' }}</td>
                    <td>{{ chapter.quizzes?.length || 0 }} quizzes</td>
                    <td class="text-center">
                      <button
                        class="btn btn-outline-primary btn-sm me-2"
                        @click="editChapter(chapter)"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                        class="btn btn-outline-danger btn-sm"
                        @click="deleteChapterHandler(chapter.id)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </template>
                  <template v-else>
                    <td>
                      <select
                        v-model="editChapterData.subject_id"
                        class="form-select form-select-sm"
                      >
                        <option
                          v-for="subject in subjects"
                          :key="subject.id"
                          :value="subject.id"
                        >
                          {{ subject.name }}
                        </option>
                      </select>
                    </td>
                    <td>
                      <input
                        v-model="editChapterData.name"
                        class="form-control form-control-sm"
                      />
                    </td>
                    <td>
                      <input
                        v-model="editChapterData.description"
                        class="form-control form-control-sm"
                      />
                    </td>
                    <td>{{ chapter.quizzes?.length || 0 }} quizzes</td>
                    <td class="text-center">
                      <button
                        class="btn btn-success btn-sm me-2"
                        @click="updateChapterHandler(chapter.id)"
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
                <tr v-if="filteredChapters.length === 0">
                  <td colspan="5" class="text-center text-muted py-4">
                    <i class="bi bi-search display-4 d-block mb-2"></i>
                    {{ searchQuery ? 'No chapters found matching your search.' : 'No chapters available.' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="searchQuery && filteredChapters.length > 0" class="text-muted small mt-2">
            Showing {{ filteredChapters.length }} of {{ chapters.length }} chapters
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import {
  getChapters,
  createChapter,
  updateChapter,
  deleteChapter,
  getSubjects,
} from "../../api";
import AdminLayout from './AdminLayout.vue';

const chapters = ref([]);
const subjects = ref([]);
const newChapter = ref({ name: "", description: "", subject_id: "" });
const editId = ref(null);
const editChapterData = ref({ name: "", description: "", subject_id: "" });
const searchQuery = ref("");

// Computed property for filtered chapters
const filteredChapters = computed(() => {
  if (!searchQuery.value.trim()) {
    return chapters.value;
  }
  
  const query = searchQuery.value.toLowerCase().trim();
  return chapters.value.filter(chapter => {
    const subjectName = getSubjectName(chapter.subject_id).toLowerCase();
    const chapterName = chapter.name.toLowerCase();
    const description = (chapter.description || '').toLowerCase();
    
    return subjectName.includes(query) ||
           chapterName.includes(query) ||
           description.includes(query);
  });
});

const fetchChapters = async () => {
  chapters.value = await getChapters();
};
const fetchSubjects = async () => {
  subjects.value = await getSubjects();
};

const createChapterHandler = async () => {
  await createChapter(newChapter.value);
  newChapter.value = { name: "", description: "", subject_id: "" };
  fetchChapters();
};

const editChapter = (chapter) => {
  editId.value = chapter.id;
  editChapterData.value = { ...chapter };
};

const updateChapterHandler = async (id) => {
  await updateChapter(id, editChapterData.value);
  editId.value = null;
  fetchChapters();
};

const deleteChapterHandler = async (id) => {
  await deleteChapter(id);
  fetchChapters();
};

const cancelEdit = () => {
  editId.value = null;
};

const getSubjectName = (id) => {
  const subj = subjects.value.find((s) => s.id === id);
  return subj ? subj.name : "Unknown";
};

const clearSearch = () => {
  searchQuery.value = "";
};

onMounted(() => {
  fetchChapters();
  fetchSubjects();
});
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
