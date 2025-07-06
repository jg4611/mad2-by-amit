<template>
  <AdminLayout>
    <div class="container-fluid py-4 bg-light min-vh-100">
      <div class="card shadow-lg border-0 mx-auto mb-4" style="max-width: 1400px">
        <div class="card-body">
          <h2 class="text-center mb-4 fw-bold text-primary">
            Questions Management
          </h2>
          <h5 class="fw-semibold mb-3">Create Quiz with Multiple Questions</h5>
          
          <!-- Quiz Selection Section -->
          <div class="quiz-selection-section mb-4 p-3 bg-light rounded">
            <h6 class="fw-semibold mb-3">Quiz Details</h6>
            <div class="row g-3">
              <div class="col-md-3">
                <label class="form-label fw-semibold">Subject</label>
                <select v-model="selectedSubject" class="form-select" required @change="onSubjectChange">
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
                <select v-model="selectedChapter" class="form-select" required :disabled="!selectedSubject" @change="onChapterChange">
                  <option disabled value="">{{ selectedSubject ? 'Select Chapter' : 'Select Subject First' }}</option>
                  <option
                    v-for="chapter in filteredChapters"
                    :key="chapter.id"
                    :value="chapter.id"
                  >
                    {{ chapter.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label fw-semibold">Quiz</label>
                <select v-model="selectedQuiz" class="form-select" required :disabled="!selectedChapter">
                  <option disabled value="">{{ selectedChapter ? 'Select Quiz' : 'Select Chapter First' }}</option>
                  <option
                    v-for="quiz in filteredQuizzes"
                    :key="quiz.id"
                    :value="quiz.id"
                  >
                    {{ quiz.title }}
                  </option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label fw-semibold">Difficulty</label>
                <select v-model="selectedDifficulty" class="form-select" required>
                  <option disabled value="">Select Difficulty</option>
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Questions Section -->
          <div class="questions-section">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="fw-semibold mb-0">Questions ({{ questionsToCreate.length }})</h6>
              <button 
                @click="addQuestion" 
                class="btn btn-success btn-sm"
                :disabled="!canAddQuestion"
              >
                <i class="bi bi-plus-circle me-2"></i>Add Question
              </button>
            </div>

            <!-- Question Forms -->
            <div v-for="(question, index) in questionsToCreate" :key="index" class="question-form mb-4 p-3 border rounded">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-semibold mb-0">Question {{ index + 1 }}</h6>
                <button 
                  @click="removeQuestion(index)" 
                  class="btn btn-danger btn-sm"
                  :disabled="questionsToCreate.length === 1"
                >
                  <i class="bi bi-trash"></i> Remove
                </button>
              </div>

              <div class="row g-3">
                <div class="col-md-12">
                  <label class="form-label fw-semibold">Question Text</label>
                  <textarea
                    v-model="question.question_text"
                    class="form-control"
                    placeholder="Enter question text"
                    rows="3"
                    required
                  ></textarea>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold">Option A</label>
                  <div class="input-group">
                    <input
                      v-model="question.option_a"
                      class="form-control"
                      placeholder="Option A"
                      required
                    />
                    <button 
                      @click="setCorrectAnswer(index, 'A')" 
                      class="btn btn-outline-success"
                      :class="{ 'btn-success': question.correct_answer === 'A' }"
                      type="button"
                    >
                      ✓
                    </button>
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold">Option B</label>
                  <div class="input-group">
                    <input
                      v-model="question.option_b"
                      class="form-control"
                      placeholder="Option B"
                      required
                    />
                    <button 
                      @click="setCorrectAnswer(index, 'B')" 
                      class="btn btn-outline-success"
                      :class="{ 'btn-success': question.correct_answer === 'B' }"
                      type="button"
                    >
                      ✓
                    </button>
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold">Option C</label>
                  <div class="input-group">
                    <input
                      v-model="question.option_c"
                      class="form-control"
                      placeholder="Option C"
                      required
                    />
                    <button 
                      @click="setCorrectAnswer(index, 'C')" 
                      class="btn btn-outline-success"
                      :class="{ 'btn-success': question.correct_answer === 'C' }"
                      type="button"
                    >
                      ✓
                    </button>
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold">Option D</label>
                  <div class="input-group">
                    <input
                      v-model="question.option_d"
                      class="form-control"
                      placeholder="Option D"
                      required
                    />
                    <button 
                      @click="setCorrectAnswer(index, 'D')" 
                      class="btn btn-outline-success"
                      :class="{ 'btn-success': question.correct_answer === 'D' }"
                      type="button"
                    >
                      ✓
                    </button>
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold">Correct Answer</label>
                  <select v-model="question.correct_answer" class="form-select" required>
                    <option disabled value="">Select Answer</option>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                  </select>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold">Difficulty</label>
                  <select v-model="question.difficulty" class="form-select" required>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Create Quiz Button -->
            <div class="text-center mt-4">
              <button
                @click="createAllQuestions"
                class="btn btn-primary btn-lg px-5"
                :disabled="!canCreateQuiz"
              >
                <i class="bi bi-plus-circle me-2"></i>Create Quiz with {{ questionsToCreate.length }} Questions
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Existing Questions Table -->
      <div class="card shadow-lg border-0 mx-auto" style="max-width: 1400px">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">All Questions</h5>
          <div class="table-responsive">
            <table
              class="table table-hover align-middle bg-white rounded shadow-sm"
            >
              <thead class="table-primary sticky-top">
                <tr>
                  <th>Quiz</th>
                  <th>Subject</th>
                  <th>Chapter</th>
                  <th>Question</th>
                  <th>Options</th>
                  <th>Correct</th>
                  <th>Difficulty</th>
                  <th class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="question in questions" :key="question.id">
                  <template v-if="editId !== question.id">
                    <td class="fw-semibold">{{ getQuizTitle(question.quiz_id) }}</td>
                    <td>{{ getSubjectNameFromQuiz(question.quiz_id) }}</td>
                    <td>{{ getChapterNameFromQuiz(question.quiz_id) }}</td>
                    <td>{{ question.question_text }}</td>
                    <td>
                      <small>
                        A: {{ question.option1 }}<br>
                        B: {{ question.option2 }}<br>
                        C: {{ question.option3 }}<br>
                        D: {{ question.option4 }}
                      </small>
                    </td>
                    <td><span class="badge bg-success">{{ question.correct_option === 1 ? 'A' : question.correct_option === 2 ? 'B' : question.correct_option === 3 ? 'C' : 'D' }}</span></td>
                    <td><span :class="getDifficultyBadge(question.difficulty).class">{{ getDifficultyBadge(question.difficulty).text }}</span></td>
                    <td class="text-center">
                      <button
                        class="btn btn-outline-primary btn-sm me-2"
                        @click="editQuestion(question)"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                        class="btn btn-outline-danger btn-sm"
                        @click="deleteQuestionHandler(question.id)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </template>
                  <template v-else>
                    <td>
                      <select
                        v-model="editQuestionData.quiz_id"
                        class="form-select form-select-sm"
                      >
                        <option
                          v-for="quiz in quizzes"
                          :key="quiz.id"
                          :value="quiz.id"
                        >
                          {{ quiz.title }}
                        </option>
                      </select>
                    </td>
                    <td>{{ getSubjectNameFromQuiz(editQuestionData.quiz_id) }}</td>
                    <td>{{ getChapterNameFromQuiz(editQuestionData.quiz_id) }}</td>
                    <td>
                      <textarea
                        v-model="editQuestionData.question_text"
                        class="form-control form-control-sm"
                        rows="2"
                      ></textarea>
                    </td>
                    <td>
                      <input
                        v-model="editQuestionData.option_a"
                        class="form-control form-control-sm mb-1"
                        placeholder="A"
                      />
                      <input
                        v-model="editQuestionData.option_b"
                        class="form-control form-control-sm mb-1"
                        placeholder="B"
                      />
                      <input
                        v-model="editQuestionData.option_c"
                        class="form-control form-control-sm mb-1"
                        placeholder="C"
                      />
                      <input
                        v-model="editQuestionData.option_d"
                        class="form-control form-control-sm"
                        placeholder="D"
                      />
                    </td>
                    <td>
                      <select
                        v-model="editQuestionData.correct_answer"
                        class="form-select form-select-sm"
                      >
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                      </select>
                    </td>
                    <td>
                      <select
                        v-model="editQuestionData.difficulty"
                        class="form-select form-select-sm"
                      >
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                      </select>
                    </td>
                    <td class="text-center">
                      <button
                        class="btn btn-success btn-sm me-2"
                        @click="updateQuestionHandler(question.id)"
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
  getQuestions,
  createQuestion,
  updateQuestion,
  deleteQuestion,
  getQuizzes,
  getChapters,
  getSubjects,
} from "../../api";
import AdminLayout from './AdminLayout.vue';

const questions = ref([]);
const quizzes = ref([]);
const chapters = ref([]);
const subjects = ref([]);

// Quiz selection state
const selectedSubject = ref("");
const selectedChapter = ref("");
const selectedQuiz = ref("");
const selectedDifficulty = ref("");

// Questions to create
const questionsToCreate = ref([{
  question_text: "",
  option_a: "",
  option_b: "",
  option_c: "",
  option_d: "",
  correct_answer: "A",
  difficulty: "easy",
}]);

// Edit state
const editId = ref(null);
const editQuestionData = ref({
  quiz_id: "",
  question_text: "",
  option_a: "",
  option_b: "",
  option_c: "",
  option_d: "",
  correct_answer: "A",
  difficulty: "easy",
});

const filteredChapters = computed(() => {
  if (!selectedSubject.value) return [];
  return chapters.value.filter(chapter => chapter.subject_id === selectedSubject.value);
});

const filteredQuizzes = computed(() => {
  if (!selectedChapter.value) return [];
  return quizzes.value.filter(quiz => quiz.chapter_id === selectedChapter.value);
});

const canAddQuestion = computed(() => {
  return selectedSubject.value && selectedChapter.value && selectedQuiz.value;
});

const canCreateQuiz = computed(() => {
  if (!selectedQuiz.value || questionsToCreate.value.length === 0) return false;
  
  return questionsToCreate.value.every(question => 
    question.question_text.trim() && 
    question.option_a.trim() && 
    question.option_b.trim() && 
    question.option_c.trim() && 
    question.option_d.trim() && 
    question.correct_answer
  );
});

const fetchQuestions = async () => {
  questions.value = await getQuestions();
};

const fetchQuizzes = async () => {
  quizzes.value = await getQuizzes();
};

const fetchChapters = async () => {
  chapters.value = await getChapters();
};

const fetchSubjects = async () => {
  subjects.value = await getSubjects();
};

const addQuestion = () => {
  questionsToCreate.value.push({
    question_text: "",
    option_a: "",
    option_b: "",
    option_c: "",
    option_d: "",
    correct_answer: "A",
    difficulty: selectedDifficulty.value || "easy",
  });
};

const removeQuestion = (index) => {
  if (questionsToCreate.value.length > 1) {
    questionsToCreate.value.splice(index, 1);
  }
};

const setCorrectAnswer = (questionIndex, answer) => {
  questionsToCreate.value[questionIndex].correct_answer = answer;
};

const createAllQuestions = async () => {
  try {
    console.log("Creating questions for quiz:", selectedQuiz.value);
    console.log("Questions to create:", questionsToCreate.value);
    
    const results = [];
    const errors = [];
    
    // Create questions one by one to handle individual errors
    for (let i = 0; i < questionsToCreate.value.length; i++) {
      const question = questionsToCreate.value[i];
      
      // Transform the data to match backend expectations
      const questionData = {
        quiz_id: selectedQuiz.value,
        question_text: question.question_text,
        option1: question.option_a,
        option2: question.option_b,
        option3: question.option_c,
        option4: question.option_d,
        correct_option: question.correct_answer === 'A' ? 1 : 
                        question.correct_answer === 'B' ? 2 : 
                        question.correct_answer === 'C' ? 3 : 4
      };
      
      console.log(`Creating question ${i + 1}:`, questionData);
      
      try {
        const result = await createQuestion(questionData);
        results.push(result);
        console.log(`Question ${i + 1} created successfully:`, result);
      } catch (error) {
        console.error(`Error creating question ${i + 1}:`, error);
        errors.push({
          questionIndex: i + 1,
          error: error.message || 'Unknown error',
          data: questionData
        });
      }
    }
    
    // Report results
    if (errors.length === 0) {
      // All questions created successfully
      alert(`Successfully created ${results.length} questions!`);
      
      // Reset form
      questionsToCreate.value = [{
        question_text: "",
        option_a: "",
        option_b: "",
        option_c: "",
        option_d: "",
        correct_answer: "A",
        difficulty: "easy",
      }];
      
      // Refresh questions list
      await fetchQuestions();
    } else if (results.length > 0) {
      // Some questions created, some failed
      const errorDetails = errors.map(e => `Question ${e.questionIndex}: ${e.error}`).join('\n');
      alert(`Created ${results.length} questions successfully, but ${errors.length} failed:\n\n${errorDetails}`);
      
      // Refresh questions list to show the ones that were created
      await fetchQuestions();
    } else {
      // All questions failed
      const errorDetails = errors.map(e => `Question ${e.questionIndex}: ${e.error}`).join('\n');
      alert(`Failed to create any questions:\n\n${errorDetails}`);
    }
    
  } catch (error) {
    console.error("Error in createAllQuestions:", error);
    alert(`Error creating questions: ${error.message || 'Unknown error occurred'}`);
  }
};

const updateQuestionHandler = async (id) => {
  // Transform the data to match backend expectations
  const updateData = {
    question_text: editQuestionData.value.question_text,
    option1: editQuestionData.value.option_a,
    option2: editQuestionData.value.option_b,
    option3: editQuestionData.value.option_c,
    option4: editQuestionData.value.option_d,
    correct_option: editQuestionData.value.correct_answer === 'A' ? 1 : 
                    editQuestionData.value.correct_answer === 'B' ? 2 : 
                    editQuestionData.value.correct_answer === 'C' ? 3 : 4
  };
  
  await updateQuestion(id, updateData);
  editId.value = null;
  fetchQuestions();
};

const deleteQuestionHandler = async (id) => {
  if (confirm("Are you sure you want to delete this question?")) {
    await deleteQuestion(id);
    fetchQuestions();
  }
};

const editQuestion = (question) => {
  editId.value = question.id;
  editQuestionData.value = {
    quiz_id: question.quiz_id,
    question_text: question.question_text,
    option_a: question.option1,
    option_b: question.option2,
    option_c: question.option3,
    option_d: question.option4,
    correct_answer: question.correct_option === 1 ? 'A' : 
                   question.correct_option === 2 ? 'B' : 
                   question.correct_option === 3 ? 'C' : 'D',
    difficulty: "easy", // Backend doesn't have difficulty field, so default to easy
  };
};

const cancelEdit = () => {
  editId.value = null;
};

const onSubjectChange = () => {
  selectedChapter.value = "";
  selectedQuiz.value = "";
};

const onChapterChange = () => {
  selectedQuiz.value = "";
};

const getQuizTitle = (quizId) => {
  const quiz = quizzes.value.find((q) => q.id === quizId);
  return quiz ? quiz.title : "Unknown";
};

const getSubjectNameFromQuiz = (quizId) => {
  const quiz = quizzes.value.find((q) => q.id === quizId);
  if (!quiz) return "Unknown";
  const chapter = chapters.value.find((c) => c.id === quiz.chapter_id);
  if (!chapter) return "Unknown";
  const subject = subjects.value.find((s) => s.id === chapter.subject_id);
  return subject ? subject.name : "Unknown";
};

const getChapterNameFromQuiz = (quizId) => {
  const quiz = quizzes.value.find((q) => q.id === quizId);
  if (!quiz) return "Unknown";
  const chapter = chapters.value.find((c) => c.id === quiz.chapter_id);
  return chapter ? chapter.name : "Unknown";
};

const getDifficultyBadge = (difficulty) => {
  const difficultyMap = {
    easy: { class: "badge bg-success", text: "Easy" },
    medium: { class: "badge bg-warning", text: "Medium" },
    hard: { class: "badge bg-danger", text: "Hard" },
  };
  return difficultyMap[difficulty] || { class: "badge bg-secondary", text: "Unknown" };
};

onMounted(() => {
  fetchSubjects();
  fetchChapters();
  fetchQuizzes();
  fetchQuestions();
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
.badge.bg-success {
  font-size: 1em;
  padding: 0.5em 1em;
  border-radius: 1em;
}
.sticky-top {
  position: sticky;
  top: 0;
  z-index: 2;
}

.question-form {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
}

.input-group .btn {
  border-left: 0;
}

.input-group .btn.btn-success {
  background-color: #198754;
  border-color: #198754;
  color: white;
}

.input-group .btn.btn-outline-success:hover {
  background-color: #198754;
  border-color: #198754;
  color: white;
}
</style>
