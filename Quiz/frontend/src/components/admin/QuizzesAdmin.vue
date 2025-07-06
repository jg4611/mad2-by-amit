<template>
  <AdminLayout>
    <div class="container-fluid py-4 bg-light min-vh-100">
      <div class="card shadow-lg border-0 mx-auto mb-4" style="max-width: 900px">
        <div class="card-body">
          <h2 class="text-center mb-4 fw-bold text-primary">
            Quizzes Management
          </h2>
          <h5 class="fw-semibold mb-3">Add New Quiz</h5>
          <form
            class="row g-3 align-items-end"
            @submit.prevent="createQuizHandler"
          >
            <div class="col-md-4">
              <label class="form-label fw-semibold">Quiz Title</label>
              <input
                v-model="newQuiz.title"
                class="form-control"
                placeholder="Quiz Title"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Subject</label>
              <select v-model="newQuiz.subject_id" class="form-select" required @change="onSubjectChange">
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
            <div class="col-md-3">
              <label class="form-label fw-semibold">Chapter</label>
              <select v-model="newQuiz.chapter_id" class="form-select" required :disabled="!newQuiz.subject_id">
                <option disabled value="">{{ newQuiz.subject_id ? 'Select Chapter' : 'Select Subject First' }}</option>
                <option
                  v-for="chapter in filteredChapters"
                  :key="chapter.id"
                  :value="chapter.id"
                >
                  {{ chapter.name }}
                </option>
              </select>
            </div>
            <div class="col-md-2">
              <label class="form-label fw-semibold">Start Date & Time</label>
              <input
                v-model="newQuiz.start_datetime"
                type="datetime-local"
                class="form-control"
                required
              />
            </div>
            <div class="col-md-2">
              <label class="form-label fw-semibold">Hours</label>
              <input
                v-model.number="newQuiz.duration_hours"
                type="number"
                min="0"
                class="form-control"
                placeholder="Hours"
              />
            </div>
            <div class="col-md-2">
              <label class="form-label fw-semibold">Minutes</label>
              <input
                v-model.number="newQuiz.duration_minutes"
                type="number"
                min="0"
                max="59"
                class="form-control"
                placeholder="Minutes"
              />
            </div>
            <div class="col-md-4 offset-md-8">
              <button
                type="submit"
                class="btn btn-gradient-primary btn-sm w-100 fw-bold mt-3"
              >
                <i class="bi bi-plus-circle me-2"></i>Add Quiz
              </button>
            </div>
          </form>
        </div>
      </div>
      <div class="card shadow-lg border-0 mx-auto" style="max-width: 1400px">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">All Quizzes</h5>
          <div class="table-responsive">
            <table
              class="table table-hover align-middle bg-white rounded shadow-sm"
            >
              <thead class="table-primary sticky-top">
                <tr>
                  <th>Title</th>
                  <th>Subject</th>
                  <th>Chapter</th>
                  <th>Start</th>
                  <th>End</th>
                  <th>Duration</th>
                  <th>Status</th>
                  <th class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in quizzes" :key="quiz.id">
                  <template v-if="editId !== quiz.id">
                    <td class="fw-semibold">{{ quiz.title }}</td>
                    <td>{{ getSubjectNameFromChapter(quiz.chapter_id) }}</td>
                    <td>{{ getChapterName(quiz.chapter_id) }}</td>
                    <td>{{ formatDisplayDateTime(quiz.start_datetime) }}</td>
                    <td>{{ formatDisplayDateTime(quiz.end_datetime) }}</td>
                    <td>{{ quiz.duration_hours }}h {{ quiz.duration_minutes }}m</td>
                    <td><span :class="getStatusBadge(quiz.status).class">{{ getStatusBadge(quiz.status).text }}</span></td>
                    <td class="text-center">
                      <button
                        class="btn btn-outline-primary btn-sm me-2"
                        @click="editQuiz(quiz)"
                      >
                        <i class="bi bi-pencil"></i> 
                      </button>
                      <button
                        class="btn btn-outline-warning btn-sm me-2"
                        @click="toggleQuizHandler(quiz.id)"
                        :title="quiz.status === 'active' ? 'Deactivate Quiz' : 'Activate Quiz'"
                      >
                        <i class="bi" :class="quiz.status === 'active' ? 'bi-pause-circle' : 'bi-play-circle'"></i>
                      </button>
                      <button
                        class="btn btn-outline-danger btn-sm"
                        @click="deleteQuizHandler(quiz.id)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </template>
                  <template v-else>
                    <td>
                      <input
                        v-model="editQuizData.title"
                        class="form-control form-control-sm"
                      />
                    </td>
                    <td>
                      <select
                        v-model="editQuizData.subject_id"
                        class="form-select form-select-sm"
                        @change="onEditSubjectChange"
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
                      <select
                        v-model="editQuizData.chapter_id"
                        class="form-select form-select-sm"
                        :disabled="!editQuizData.subject_id"
                      >
                        <option disabled value="">{{ editQuizData.subject_id ? 'Select Chapter' : 'Select Subject First' }}</option>
                        <option
                          v-for="chapter in filteredEditChapters"
                          :key="chapter.id"
                          :value="chapter.id"
                        >
                          {{ chapter.name }}
                        </option>
                      </select>
                    </td>
                    <td>
                      <input
                        v-model="editQuizData.start_datetime"
                        type="datetime-local"
                        class="form-control form-control-sm"
                      />
                    </td>
                    <td>
                      <div class="row g-1">
                        <div class="col-6">
                          <input
                            v-model.number="editQuizData.duration_hours"
                            type="number"
                            min="0"
                            class="form-control form-control-sm"
                            placeholder="Hours"
                          />
                        </div>
                        <div class="col-6">
                          <input
                            v-model.number="editQuizData.duration_minutes"
                            type="number"
                            min="0"
                            max="59"
                            class="form-control form-control-sm"
                            placeholder="Minutes"
                          />
                        </div>
                      </div>
                    </td>
                    <td>
                      <span :class="getStatusBadge(editQuizData.status).class">
                        {{ getStatusBadge(editQuizData.status).text }}
                      </span>
                    </td>
                    <td class="text-center">
                      <button
                        class="btn btn-success btn-sm me-2"
                        @click="updateQuizHandler(quiz.id)"
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
import { ref, onMounted, computed } from "vue";
import {
  getQuizzes,
  createQuiz,
  updateQuiz,
  deleteQuiz,
  toggleQuiz,
  getChapters,
  getSubjects,
} from "../../api";
import AdminLayout from './AdminLayout.vue';

const quizzes = ref([]);
const chapters = ref([]);
const subjects = ref([]);
const newQuiz = ref({
  title: "",
  subject_id: "",
  chapter_id: "",
  start_datetime: "",
  end_datetime: "",
  duration_hours: 0,
  duration_minutes: 30,
});
const editId = ref(null);
const editQuizData = ref({});

const fetchQuizzes = async () => {
  quizzes.value = await getQuizzes();
};
const fetchChapters = async () => {
  chapters.value = await getChapters();
};
const fetchSubjects = async () => {
  subjects.value = await getSubjects();
};

// Computed property for filtered chapters based on selected subject
const filteredChapters = computed(() => {
  if (!newQuiz.value.subject_id) return [];
  return chapters.value.filter(chapter => chapter.subject_id === newQuiz.value.subject_id);
});

// Computed property for filtered chapters in edit mode
const filteredEditChapters = computed(() => {
  if (!editQuizData.value.subject_id) return [];
  return chapters.value.filter(chapter => chapter.subject_id === editQuizData.value.subject_id);
});

const formatDateTime = (dt) => {
  // Converts 'YYYY-MM-DDTHH:MM' to 'YYYY-MM-DD HH:MM'
  if (!dt) return "";
  return dt.replace("T", " ");
};

const formatDateTimeForInput = (isoString) => {
  // Converts ISO string to datetime-local input format
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toISOString().slice(0, 16); // Format: YYYY-MM-DDTHH:MM
};

const formatDisplayDateTime = (isoString) => {
  if (!isoString) return "Not set";
  const date = new Date(isoString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
};

const getStatusBadge = (status) => {
  const statusConfig = {
    'active': { text: '🟢 Active', class: 'badge bg-success' },
    'upcoming': { text: '🟡 Upcoming', class: 'badge bg-warning' },
    'expired': { text: '🔴 Expired', class: 'badge bg-danger' },
    'inactive': { text: '⚪ Inactive', class: 'badge bg-secondary' }
  };
  return statusConfig[status] || statusConfig['inactive'];
};

const createQuizHandler = async () => {
  try {
    const payload = {
      title: newQuiz.value.title,
      chapter_id: Number(newQuiz.value.chapter_id),
      duration_hours: Number(newQuiz.value.duration_hours),
      duration_minutes: Number(newQuiz.value.duration_minutes),
      start_datetime: formatDateTime(newQuiz.value.start_datetime),
    };
    await createQuiz(payload);
    newQuiz.value = {
      title: "",
      subject_id: "",
      chapter_id: "",
      start_datetime: "",
      end_datetime: "",
      duration_hours: 0,
      duration_minutes: 30,
    };
    await fetchQuizzes();
  } catch (error) {
    console.error("Error creating quiz:", error);
    alert("Error creating quiz. Please try again.");
  }
};

const deleteQuizHandler = async (id) => {
  console.log("Delete button clicked for quiz ID:", id);
  
  if (confirm("Are you sure you want to delete this quiz? This action cannot be undone.")) {
    try {
      console.log("User confirmed deletion. Proceeding to delete quiz with ID:", id);
      const result = await deleteQuiz(id);
      console.log("Delete result:", result);
      await fetchQuizzes();
      alert("Quiz deleted successfully!");
    } catch (error) {
      console.error("Error deleting quiz:", error);
      console.error("Error details:", {
        message: error.message,
        status: error.status,
        response: error.response
      });
      
      let errorMessage = "Error deleting quiz. Please try again.";
      
      if (error.message) {
        errorMessage = error.message;
      } else if (error.response && error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message;
      }
      
      alert(errorMessage);
    }
  } else {
    console.log("User cancelled deletion");
  }
};

const editQuiz = (quiz) => {
  console.log("Editing quiz:", quiz);
  editId.value = quiz.id;
  editQuizData.value = { ...quiz };
  // Set the subject_id based on the chapter's subject
  const chapter = chapters.value.find(ch => ch.id === quiz.chapter_id);
  if (chapter) {
    editQuizData.value.subject_id = chapter.subject_id;
  }
  // Format datetime for input fields
  editQuizData.value.start_datetime = formatDateTimeForInput(quiz.start_datetime);
  editQuizData.value.end_datetime = formatDateTimeForInput(quiz.end_datetime);
  console.log("Edit data set:", editQuizData.value);
};

const updateQuizHandler = async (id) => {
  try {
    console.log("Updating quiz with ID:", id);
    console.log("Update data:", editQuizData.value);
    
    const payload = {
      title: editQuizData.value.title,
      chapter_id: Number(editQuizData.value.chapter_id),
      duration_hours: Number(editQuizData.value.duration_hours),
      duration_minutes: Number(editQuizData.value.duration_minutes),
      start_datetime: formatDateTime(editQuizData.value.start_datetime),
    };
    
    console.log("Payload being sent:", payload);
    const result = await updateQuiz(id, payload);
    console.log("Update result:", result);
    
    editId.value = null;
    await fetchQuizzes();
    alert("Quiz updated successfully!");
  } catch (error) {
    console.error("Error updating quiz:", error);
    alert(`Error updating quiz: ${error.message || 'Unknown error'}`);
  }
};

const cancelEdit = () => {
  editId.value = null;
};

const getChapterName = (id) => {
  const chapter = chapters.value.find((ch) => ch.id === id);
  return chapter ? chapter.name : "";
};

const getSubjectName = (id) => {
  const subject = subjects.value.find((s) => s.id === id);
  return subject ? subject.name : "";
};

const getSubjectNameFromChapter = (chapterId) => {
  const chapter = chapters.value.find((ch) => ch.id === chapterId);
  return chapter ? getSubjectName(chapter.subject_id) : "";
};

const onSubjectChange = () => {
  // Reset chapter selection when subject changes
  newQuiz.value.chapter_id = "";
};

const onEditSubjectChange = () => {
  // Reset chapter selection when subject changes in edit mode
  editQuizData.value.chapter_id = "";
};

const toggleQuizHandler = async (id) => {
  try {
    await toggleQuiz(id);
    await fetchQuizzes();
  } catch (error) {
    console.error("Error toggling quiz:", error);
    alert("Error toggling quiz status. Please try again.");
  }
};

// Temporary test function to debug delete issue
const testDelete = async (id) => {
  console.log("=== DELETE TEST ===");
  console.log("Quiz ID:", id);
  console.log("Current quizzes:", quizzes.value);
  console.log("Quiz to delete:", quizzes.value.find(q => q.id === id));
  
  try {
    console.log("Testing API call...");
    const result = await deleteQuiz(id);
    console.log("API call successful:", result);
  } catch (error) {
    console.error("API call failed:", error);
  }
};

onMounted(() => {
  fetchQuizzes();
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

.badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.5rem;
  border-radius: 6px;
  font-weight: 600;
}

.badge.bg-success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
}

.badge.bg-warning {
  background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
  color: white !important;
}

.badge.bg-danger {
  background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
}

.badge.bg-secondary {
  background: linear-gradient(135deg, #718096 0%, #4a5568 100%) !important;
}

.btn-outline-warning {
  color: #ed8936;
  border-color: #ed8936;
}

.btn-outline-warning:hover {
  background-color: #ed8936;
  border-color: #ed8936;
  color: white;
}

.btn-outline-warning:focus {
  box-shadow: 0 0 0 0.2rem rgba(237, 137, 54, 0.25);
}

.table-responsive {
  border-radius: 1rem;
  overflow: hidden;
}

.form-control-sm, .form-select-sm {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
