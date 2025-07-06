<template>
  <div class="quiz-container">
    <!-- Header -->
    <header class="quiz-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">📝</div>
          <h1 class="logo-text">QuizMaster</h1>
        </div>
        <div class="user-section">
          <div class="user-info">
            <span class="user-name">{{ userFullName || 'Student' }}</span>
            <span class="user-role">Student</span>
          </div>
          <button @click="logout" class="logout-btn">
            <span>🚪</span> Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="quiz-main">
      <div class="quiz-layout">
        <!-- Left Side - Quiz List -->
        <div class="quiz-list-section">
          <div class="section-header">
            <h2>Available Quizzes</h2>
            <p>Select a quiz to begin your assessment</p>
          </div>
          
          <div class="quiz-list">
            <div v-if="quizzes.length === 0" class="loading-state">
              <div class="loading-spinner">⏳</div>
              <p>Loading quizzes...</p>
            </div>
            <div 
              v-else
              v-for="quiz in quizzes" 
              :key="quiz.id"
              class="quiz-item"
              :class="{ 
                'selected': selectedQuiz?.id === quiz.id,
                'completed': completedQuizzes.includes(quiz.id),
                'disabled': completedQuizzes.includes(quiz.id) || quiz.status !== 'active'
              }"
              @click="selectQuiz(quiz)"
            >
              <div class="quiz-item-header">
                <h3>{{ quiz.title }}</h3>
                <div class="quiz-badges">
                  <span :class="getStatusBadge(quiz.status).class">
                    {{ getStatusBadge(quiz.status).text }}
                  </span>
                  <span v-if="completedQuizzes.includes(quiz.id)" class="badge bg-info">
                    Completed
                  </span>
                </div>
              </div>
              <div class="quiz-item-body">
                <p class="quiz-subject">{{ getSubjectNameFromChapter(quiz.chapter_id) }}</p>
                <p class="quiz-chapter">{{ getChapterName(quiz.chapter_id) }}</p>
                <div class="quiz-meta">
                  <span class="meta-item">
                    <span class="meta-icon">⏱️</span>
                    {{ quiz.duration_hours }}h {{ quiz.duration_minutes }}m
                  </span>
                  <span class="meta-item">
                    <span class="meta-icon">📅</span>
                    {{ formatDate(quiz.start_datetime) }}
                  </span>
                </div>
              </div>
              <div class="quiz-item-actions">
                <button 
                  v-if="!completedQuizzes.includes(quiz.id) && quiz.status === 'active'"
                  @click.stop="selectQuiz(quiz)"
                  class="btn btn-primary btn-sm"
                >
                  Take Quiz
                </button>
                <button 
                  v-else-if="completedQuizzes.includes(quiz.id)"
                  class="btn btn-secondary btn-sm"
                  disabled
                >
                  Already Completed
                </button>
                <button 
                  v-else
                  class="btn btn-secondary btn-sm"
                  disabled
                >
                  Not Available
                </button>
              </div>
            </div>
          </div>

          <div v-if="quizzes.length === 0" class="no-quizzes">
            <div class="no-quizzes-icon">📚</div>
            <h3>No Quizzes Available</h3>
            <p>There are currently no quizzes available.</p>
          </div>
        </div>

        <!-- Middle Section - Quiz Taking Section -->
        <div class="quiz-taking-section">
          <div v-if="!selectedQuiz" class="quiz-placeholder">
            <div class="placeholder-content">
              <div class="placeholder-icon">📝</div>
              <h3>Select a Quiz</h3>
              <p>Choose a quiz from the list on the left to begin your assessment</p>
            </div>
          </div>

          <!-- Quiz Interface -->
          <div v-else class="quiz-interface">
            <div class="quiz-header-bar">
              <div class="quiz-info">
                <h2>{{ selectedQuiz.title }}</h2>
                <p>{{ getSubjectNameFromChapter(selectedQuiz.chapter_id) }} - {{ getChapterName(selectedQuiz.chapter_id) }}</p>
              </div>
              <div class="quiz-timer" v-if="timeRemaining > 0">
                <span class="timer-icon">⏰</span>
                <span class="timer-text">{{ formatTime(timeRemaining) }}</span>
              </div>
              <button @click="exitQuiz" class="exit-btn">
                <span>❌</span> Exit Quiz
              </button>
            </div>

            <div class="quiz-progress">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: `${Object.keys(selectedAnswers).length / quizQuestions.length * 100}%` }"
                ></div>
              </div>
              <span class="progress-text">{{ Object.keys(selectedAnswers).length }} of {{ quizQuestions.length }} questions answered</span>
            </div>

            <div class="questions-container" v-if="!showResults">
              <div 
                v-for="(question, index) in quizQuestions" 
                :key="question.id"
                class="question-container"
              >
                <div class="question-header">
                  <span class="question-number">Question {{ index + 1 }}</span>
                  <span :class="getDifficultyBadge(question.difficulty).class">
                    {{ getDifficultyBadge(question.difficulty).text }}
                  </span>
                </div>
                
                <div class="question-text">
                  {{ question.question_text }}
                </div>

                <div class="options-container">
                  <div 
                    v-for="(option, optionIndex) in ['A', 'B', 'C', 'D']" 
                    :key="option"
                    class="option-item"
                    :class="{ 
                      selected: selectedAnswers[index] === option
                    }"
                    @click="selectAnswer(option, index)"
                  >
                    <div class="option-letter">{{ option }}</div>
                    <div class="option-text">
                      {{ question[`option${optionIndex + 1}`] }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="quiz-submit-section">
                <button 
                  @click="submitQuiz" 
                  class="btn btn-success btn-large"
                  :disabled="Object.keys(selectedAnswers).length < quizQuestions.length"
                >
                  Submit Quiz ({{ Object.keys(selectedAnswers).length }}/{{ quizQuestions.length }})
                </button>
              </div>
            </div>

            <!-- Results Modal -->
            <div v-if="showResults" class="results-modal">
              <div class="results-content">
                <div class="results-header">
                  <h2>Quiz Results</h2>
                  <div class="score-display">
                    <div class="score-circle">
                      <span class="score-number">{{ correctAnswers }}</span>
                      <span class="score-total">/ {{ quizQuestions.length }}</span>
                    </div>
                    <div class="score-percentage">
                      {{ Math.round((correctAnswers / quizQuestions.length) * 100) }}%
                    </div>
                  </div>
                </div>
                
                <div class="results-summary">
                  <div class="summary-item">
                    <span class="summary-label">Correct Answers:</span>
                    <span class="summary-value correct">{{ correctAnswers }}</span>
                  </div>
                  <div class="summary-item">
                    <span class="summary-label">Incorrect Answers:</span>
                    <span class="summary-value incorrect">{{ quizQuestions.length - correctAnswers }}</span>
                  </div>
                  <div class="summary-item">
                    <span class="summary-label">Time Taken:</span>
                    <span class="summary-value">{{ formatTime(quizDuration - timeRemaining) }}</span>
                  </div>
                </div>

                <div class="results-actions">
                  <button @click="finishQuiz" class="btn btn-primary">
                    Back to Dashboard
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side - Quiz History Section -->
        <div class="quiz-history-section">
          <div class="section-header">
            <h2>Quiz History</h2>
            <p>Your past quiz attempts and scores</p>
          </div>
          
          <div class="history-list">
            <div v-if="quizHistory.length === 0" class="no-history">
              <div class="no-history-icon">📊</div>
              <h3>No Quiz History</h3>
              <p>You haven't taken any quizzes yet. Start with an available quiz!</p>
            </div>
            <div 
              v-else
              v-for="attempt in quizHistory" 
              :key="`${attempt.quiz_id}-${attempt.date_taken}`"
              class="history-item"
            >
              <div class="history-item-header">
                <h3>{{ attempt.quiz_title }}</h3>
                <div class="score-badge" :class="getScoreClass(attempt.score, attempt.total_questions)">
                  {{ Math.round((attempt.score / attempt.total_questions) * 100) }}%
                </div>
              </div>
              <div class="history-item-body">
                <div class="history-meta">
                  <span class="meta-item">
                    <span class="meta-icon">📊</span>
                    Score: {{ attempt.score }}/{{ attempt.total_questions }}
                  </span>
                  <span class="meta-item">
                    <span class="meta-icon">📅</span>
                    {{ formatHistoryDate(attempt.date_taken) }}
                  </span>
                </div>
                <div class="performance-indicator">
                  <div class="performance-bar">
                    <div 
                      class="performance-fill" 
                      :style="{ width: `${(attempt.score / attempt.total_questions) * 100}%` }"
                      :class="getScoreClass(attempt.score, attempt.total_questions)"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Performance Summary -->
          <div v-if="quizHistory.length > 0" class="performance-summary">
            <h3>Performance Summary</h3>
            <div class="summary-stats">
              <div class="stat-item">
                <span class="stat-label">Total Quizzes Taken:</span>
                <span class="stat-value">{{ quizHistory.length }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Average Score:</span>
                <span class="stat-value">{{ averageScore }}%</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Best Score:</span>
                <span class="stat-value">{{ bestScore }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import { getQuizzes, getQuestions, getChapters, getSubjects } from "../api";

const router = useRouter();
const userFullName = ref("");
const quizzes = ref([]);
const questions = ref([]);
const chapters = ref([]);
const subjects = ref([]);

// Quiz state
const selectedQuiz = ref(null);
const quizQuestions = ref([]);
const currentQuestionIndex = ref(0);
const selectedAnswers = ref({});
const timeRemaining = ref(0);
const quizDuration = ref(0);
const showResults = ref(false);
const correctAnswers = ref(0);
const completedQuizzes = ref([]);
const quizHistory = ref([]);
let timer = null;

const activeQuizzes = computed(() => {
  return quizzes.value.filter(quiz => quiz.status === 'active');
});

const currentQuestion = computed(() => {
  return quizQuestions.value[currentQuestionIndex.value] || null;
});

const averageScore = computed(() => {
  if (quizHistory.value.length === 0) return 0;
  const totalPercentage = quizHistory.value.reduce((sum, attempt) => {
    return sum + (attempt.score / attempt.total_questions) * 100;
  }, 0);
  return Math.round(totalPercentage / quizHistory.value.length);
});

const bestScore = computed(() => {
  if (quizHistory.value.length === 0) return 0;
  const bestPercentage = Math.max(...quizHistory.value.map(attempt => {
    return (attempt.score / attempt.total_questions) * 100;
  }));
  return Math.round(bestPercentage);
});

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
};

const fetchData = async () => {
  try {
    console.log('Fetching all data...');
    
    // Fetch quizzes first - this is the most important
    try {
      quizzes.value = await getQuizzes();
      console.log('Quizzes loaded:', quizzes.value.length);
    } catch (error) {
      console.error('Error loading quizzes:', error);
      quizzes.value = [];
    }
    
    // Fetch other data (these are less critical)
    try {
      questions.value = await getQuestions();
    } catch (error) {
      console.error('Error loading questions:', error);
      questions.value = [];
    }
    
    try {
      chapters.value = await getChapters();
    } catch (error) {
      console.error('Error loading chapters:', error);
      chapters.value = [];
    }
    
    try {
      subjects.value = await getSubjects();
    } catch (error) {
      console.error('Error loading subjects:', error);
      subjects.value = [];
    }
    
    // Fetch quiz history
    try {
      await fetchQuizHistory();
    } catch (error) {
      console.error('Error loading quiz history:', error);
    }
    
    console.log('All data loaded successfully');
  } catch (error) {
    console.error("Error in fetchData:", error);
  }
};

const fetchQuizHistory = async () => {
  try {
    console.log('Fetching quiz history...');
    const response = await fetch('http://127.0.0.1:5006/api/quiz-history', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const history = await response.json();
      quizHistory.value = history;
      completedQuizzes.value = history.map(score => score.quiz_id);
      console.log('Quiz history loaded. Completed quizzes:', completedQuizzes.value);
    } else {
      console.error('Failed to fetch quiz history:', response.status);
    }
  } catch (error) {
    console.error("Error fetching quiz history:", error);
  }
};

const getStatusBadge = (status) => {
  const statusMap = {
    active: { class: "badge bg-success", text: "Active" },
    upcoming: { class: "badge bg-warning", text: "Upcoming" },
    expired: { class: "badge bg-danger", text: "Expired" }
  };
  return statusMap[status] || { class: "badge bg-secondary", text: "Unknown" };
};

const getSubjectNameFromChapter = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  if (!chapter) return "Unknown";
  const subject = subjects.value.find(s => s.id === chapter.subject_id);
  return subject ? subject.name : "Unknown";
};

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  return chapter ? chapter.name : "Unknown";
};

const getDifficultyBadge = (difficulty) => {
  const difficultyMap = {
    easy: { class: "badge bg-success", text: "Easy" },
    medium: { class: "badge bg-warning", text: "Medium" },
    hard: { class: "badge bg-danger", text: "Hard" }
  };
  return difficultyMap[difficulty] || { class: "badge bg-secondary", text: "Unknown" };
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};

const formatHistoryDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getScoreClass = (score, totalQuestions) => {
  const percentage = (score / totalQuestions) * 100;
  if (percentage >= 70) return 'bg-success';
  if (percentage >= 50) return 'bg-warning';
  return 'bg-danger';
};

const selectQuiz = async (quiz) => {
  // Check if quiz is already completed
  if (completedQuizzes.value.includes(quiz.id)) {
    alert("You have already completed this quiz. You cannot take it again.");
    return;
  }
  
  // Check if quiz is active
  if (quiz.status !== 'active') {
    alert("This quiz is not currently active. Please select an active quiz.");
    return;
  }
  
  try {
    selectedQuiz.value = quiz;
    
    // Fetch questions for this specific quiz
    const quizQuestionsResponse = await fetch(`http://127.0.0.1:5006/api/quizzes/${quiz.id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (quizQuestionsResponse.ok) {
      const quizData = await quizQuestionsResponse.json();
      quizQuestions.value = quizData.questions || [];
    } else {
      // Fallback to filtering from all questions
      quizQuestions.value = questions.value.filter(q => q.quiz_id === quiz.id);
    }
    
    selectedAnswers.value = {};
    currentQuestionIndex.value = 0;
    showResults.value = false;
    
    // Set timer
    quizDuration.value = (quiz.duration_hours * 3600) + (quiz.duration_minutes * 60);
    timeRemaining.value = quizDuration.value;
    
    startTimer();
  } catch (error) {
    console.error("Error fetching quiz questions:", error);
    alert("Error loading quiz questions. Please try again.");
  }
};

const startTimer = () => {
  timer = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    } else {
      submitQuiz();
    }
  }, 1000);
};

const selectAnswer = (option, index) => {
  if (!showResults.value) {
    selectedAnswers.value[index] = option;
  }
};

const submitQuiz = async () => {
  clearInterval(timer);
  showResults.value = true;
  
  // Calculate correct answers - backend uses correct_option (1,2,3,4) and option1,option2,etc.
  correctAnswers.value = quizQuestions.value.reduce((count, question, index) => {
    const selectedAnswer = selectedAnswers.value[index];
    const correctOption = question.correct_option; // Backend returns 1,2,3,4
    
    // Convert selected answer (A,B,C,D) to number (1,2,3,4) for comparison
    const selectedOptionNumber = selectedAnswer === 'A' ? 1 : 
                                 selectedAnswer === 'B' ? 2 : 
                                 selectedAnswer === 'C' ? 3 : 4;
    
    return count + (selectedOptionNumber === correctOption ? 1 : 0);
  }, 0);
  
  // Submit score to backend
  try {
    const scoreData = {
      quizId: selectedQuiz.value.id,
      score: correctAnswers.value,
      totalQuestions: quizQuestions.value.length
    };
    
    const response = await fetch('http://127.0.0.1:5006/api/submit-quiz', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(scoreData)
    });
    
    if (response.ok) {
      // Immediately add the quiz to completed list to prevent retaking
      if (selectedQuiz.value && !completedQuizzes.value.includes(selectedQuiz.value.id)) {
        completedQuizzes.value.push(selectedQuiz.value.id);
      }
      console.log('Quiz submitted successfully. Quiz ID:', selectedQuiz.value.id, 'added to completed list');
    } else {
      console.error('Failed to submit quiz score');
    }
  } catch (error) {
    console.error('Error submitting quiz score:', error);
  }
};

const finishQuiz = async () => {
  console.log('Finishing quiz. Current completed quizzes:', completedQuizzes.value);
  
  // Add the completed quiz to the list if not already there
  if (selectedQuiz.value && !completedQuizzes.value.includes(selectedQuiz.value.id)) {
    completedQuizzes.value.push(selectedQuiz.value.id);
    console.log('Added quiz ID', selectedQuiz.value.id, 'to completed list');
  }
  
  selectedQuiz.value = null;
  quizQuestions.value = [];
  selectedAnswers.value = {};
  currentQuestionIndex.value = 0;
  showResults.value = false;
  timeRemaining.value = 0;
  
  // Refresh quiz history from server to ensure consistency
  await fetchQuizHistory();
  
  console.log('Final completed quizzes list:', completedQuizzes.value);
};

const exitQuiz = () => {
  if (confirm("Are you sure you want to exit the quiz? Your progress will be lost.")) {
    clearInterval(timer);
    finishQuiz();
  }
};



onMounted(() => {
  if (!localStorage.getItem("token")) {
    router.push("/login");
  }
  userFullName.value = localStorage.getItem("userFullName") || "Student";
  console.log('Component mounted, fetching data...');
  fetchData().then(() => {
    console.log('Data fetch completed. Quizzes count:', quizzes.value.length);
    console.log('Quizzes:', quizzes.value);
  });
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});
</script>

<style scoped>
.quiz-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  display: flex;
  flex-direction: column;
}

.quiz-header {
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

.quiz-main {
  flex: 1;
  margin-top: 80px;
  padding: 2rem;
  width: 100vw;
  max-width: 100vw;
}

.quiz-layout {
  display: flex;
  gap: 2rem;
  height: calc(100vh - 80px);
  max-width: 100vw;
  overflow-x: auto;
}

/* Left Side - Quiz List */
.quiz-list-section {
  flex: 0 0 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.section-header {
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.section-header p {
  font-size: 1.1rem;
  color: #718096;
}

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.quiz-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 1rem;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.quiz-item:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-color: rgba(66, 153, 225, 0.3);
}

.quiz-item.selected {
  border-color: #4299e1;
  background: rgba(66, 153, 225, 0.1);
}

.quiz-item.completed {
  background: rgba(72, 187, 120, 0.1);
  border-color: #48bb78;
}

.quiz-item.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.quiz-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.quiz-item-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
  flex: 1;
}

.quiz-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.quiz-item-body {
  margin-bottom: 1rem;
}

.quiz-subject {
  font-size: 0.9rem;
  color: #4299e1;
  font-weight: 500;
  margin: 0 0 0.25rem 0;
}

.quiz-chapter {
  font-size: 0.85rem;
  color: #718096;
  margin: 0 0 0.5rem 0;
}

.quiz-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #718096;
}

.meta-icon {
  font-size: 0.9rem;
}

.quiz-item-actions {
  display: flex;
  justify-content: center;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

/* Middle Section - Quiz History */
.quiz-history-section {
  flex: 0 0 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 1rem;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.history-item:hover:not(.no-history) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-color: rgba(66, 153, 225, 0.3);
}

.history-item.no-history {
  opacity: 0.6;
  cursor: not-allowed;
}

.history-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.history-item-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
  flex: 1;
}

.score-badge {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.history-item-body {
  margin-top: 0.5rem;
}

.history-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
  color: #718096;
}

.performance-indicator {
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.performance-bar {
  height: 100%;
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  transition: width 0.3s ease;
}

.performance-bar.bg-success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
}

.performance-bar.bg-warning {
  background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
}

.performance-bar.bg-danger {
  background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
}

.performance-fill {
  height: 100%;
  border-radius: 4px;
}

.performance-fill.bg-success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
}

.performance-fill.bg-warning {
  background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
}

.performance-fill.bg-danger {
  background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
}

.performance-summary {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

.performance-summary h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1.5rem;
}

.summary-stats {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #718096;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
}

/* Right Side - Quiz Taking Section */
.quiz-taking-section {
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.quiz-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 2rem;
}

.placeholder-content {
  text-align: center;
  max-width: 400px;
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.placeholder-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.placeholder-content p {
  color: #718096;
  line-height: 1.5;
}

.quiz-interface {
  max-width: 1000px;
  margin: 0 auto;
}

.quiz-header-bar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-info h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.quiz-info p {
  color: #718096;
  margin: 0;
}

.quiz-timer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-weight: 600;
}

.timer-icon {
  font-size: 1.25rem;
}

.exit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #e53e3e;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.exit-btn:hover {
  background: #c53030;
  transform: translateY(-1px);
}

.quiz-progress {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.9rem;
  color: #718096;
  text-align: center;
}

.questions-container {
  max-width: 800px;
  margin: 0 auto;
}

.question-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.question-number {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
}

.question-text {
  font-size: 1.25rem;
  font-weight: 500;
  color: #2d3748;
  line-height: 1.6;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f7fafc;
  border-radius: 12px;
  border-left: 4px solid #4299e1;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.option-item:hover {
  border-color: #4299e1;
  background: #ebf8ff;
}

.option-item.selected {
  border-color: #4299e1;
  background: #ebf8ff;
}

.option-item.correct {
  border-color: #48bb78;
  background: #f0fff4;
}

.option-item.incorrect {
  border-color: #f56565;
  background: #fff5f5;
}

.option-letter {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #4299e1;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 1.125rem;
}

.option-item.correct .option-letter {
  background: #48bb78;
}

.option-item.incorrect .option-letter {
  background: #f56565;
}

.option-text {
  flex: 1;
  font-size: 1rem;
  color: #2d3748;
  line-height: 1.5;
}

.quiz-submit-section {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
}

/* Results Modal */
.results-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.results-content {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  max-width: 500px;
  width: 90%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.results-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 2rem;
}

.score-display {
  margin-bottom: 2rem;
}

.score-circle {
  display: inline-flex;
  align-items: baseline;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.score-number {
  font-size: 3rem;
  font-weight: 700;
  color: #4299e1;
}

.score-total {
  font-size: 1.5rem;
  color: #718096;
}

.score-percentage {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.results-summary {
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  color: #718096;
}

.summary-value {
  font-weight: 600;
}

.summary-value.correct {
  color: #48bb78;
}

.summary-value.incorrect {
  color: #f56565;
}

.results-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .quiz-main {
    padding: 1rem;
  }
  
  .quiz-layout {
    flex-direction: column;
    height: auto;
    gap: 1rem;
  }
  
  .quiz-list-section {
    flex: none;
    max-height: 300px;
  }

  .quiz-history-section {
    flex: none;
    max-height: 300px;
  }
  
  .quiz-taking-section {
    min-height: 500px;
  }
  
  .quiz-header-bar {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .question-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .results-actions {
    flex-direction: column;
  }
  
  .results-content {
    padding: 2rem;
  }
  
  .quiz-item-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .quiz-badges {
    justify-content: flex-start;
  }
}

/* Badge Styles */
.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.bg-success {
  background-color: #48bb78;
  color: white;
}

.bg-warning {
  background-color: #ed8936;
  color: white;
}

.bg-danger {
  background-color: #f56565;
  color: white;
}

.bg-secondary {
  background-color: #718096;
  color: white;
}

.bg-info {
  background-color: #4299e1;
  color: white;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #718096;
}

.loading-spinner {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.no-quizzes {
  text-align: center;
  padding: 3rem 1rem;
  color: #718096;
}

.no-quizzes-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-quizzes h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #4a5568;
}

.no-quizzes p {
  font-size: 0.9rem;
  line-height: 1.5;
}

.no-history {
  text-align: center;
  padding: 3rem 1rem;
  color: #718096;
}

.no-history-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-history h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #4a5568;
}

.no-history p {
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>
