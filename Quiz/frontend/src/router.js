// Simple Vue router for login and dashboard
import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import AdminDashboard from "./components/admin/AdminDashboard.vue";
import UsersAdmin from "./components/admin/UsersAdmin.vue";
import SubjectsAdmin from "./components/admin/SubjectsAdmin.vue";
import ChaptersAdmin from "./components/admin/ChaptersAdmin.vue";
import QuizzesAdmin from "./components/admin/QuizzesAdmin.vue";
import QuestionsAdmin from "./components/admin/QuestionsAdmin.vue";
import Register from "./components/Register.vue";
import QuizView from "./components/QuizView.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/", component: QuizView }, // Default landing page for regular users
  { path: "/dashboard", component: Dashboard },
  { path: "/quiz", component: QuizView },
  // Admin routes
  { path: "/admin", component: AdminDashboard },
  { path: "/admin/adminDashboard", redirect: "/admin" }, // Redirect for consistency
  { path: "/admin/users", component: UsersAdmin },
  { path: "/admin/subjects", component: SubjectsAdmin },
  { path: "/admin/chapters", component: ChaptersAdmin },
  { path: "/admin/quizzes", component: QuizzesAdmin },
  { path: "/admin/questions", component: QuestionsAdmin },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const publicPages = ["/login", "/register"];
  const adminPages = [
    "/admin",
    "/admin/adminDashboard",
    "/admin/users",
    "/admin/subjects",
    "/admin/chapters",
    "/admin/quizzes",
    "/admin/questions",
  ];
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  // Check if user is not authenticated
  if (!publicPages.includes(to.path) && !token) {
    return next("/login");
  }

  // If user is authenticated and trying to access login/register, redirect based on role
  if (token && publicPages.includes(to.path)) {
    if (role === "admin") {
      return next("/admin");
    } else {
      return next("/");
    }
  }

  // Check admin access
  if (adminPages.includes(to.path) && role !== "admin") {
    return next("/");
  }

  next();
});

export default router;
