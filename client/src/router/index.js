import { createRouter, createWebHistory } from "vue-router";
import UserLogin from "@/views/User/Login.vue";
import Register from "@/views/User/Register.vue";
import UserLayout from "@/views/User/Layout.vue";
import UserDashboard from "@/views/User/Dashboard.vue";
import UserViewIssues from "@/views/User/ViewIssues.vue";
import UserSummary from "@/views/User/Summary.vue";
import UserReviewBook from "@/views/User/ReviewBook.vue";

import AdminLogin from "@/views/Admin/Login.vue";
import AdminDashboard from "@/views/Admin/Dashboard.vue";
import AdminViewSection from "@/views/Admin/ViewSection.vue";
import AdminCreateBook from "@/views/Admin/CreateBook.vue";
import AdminCreateSection from "@/views/Admin/CreateSection.vue";
import AdminEditBook from "@/views/Admin/EditBook.vue";
import AdminEditSection from "@/views/Admin/EditSection.vue";
import AdminViewRequests from "@/views/Admin/ViewRequests.vue";
import AdminViewIssues from "@/views/Admin/ViewIssues.vue";
import AdminLayout from "@/views/Admin/Layout.vue";
import AdminSummary from "@/views/Admin/Summary.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/admin",
      name: "admin_index",
      component: AdminLayout,
      children: [
        {
          path: "board",
          name: "adminboard",
          component: AdminDashboard,
        },
        {
          path: "section/create",
          name: "section_create",
          component: AdminCreateSection,
        },
        {
          path: "section/:section_name/view",
          name: "section_view",
          component: AdminViewSection,
          props: true,
        },
        {
          path: "section/:section_id/edit",
          name: "section_edit",
          component: AdminEditSection,
          props: true,
        },
        {
          path: "book/create",
          name: "book_create",
          component: AdminCreateBook,
        },
        {
          path: "book/:book_id/edit",
          name: "book_edit",
          component: AdminEditBook,
          props: true,
        },
        {
          path: "requests/view",
          name: "requests_view",
          component: AdminViewRequests,
        },
        {
          path: "issues/view",
          name: "admin_issues_view",
          component: AdminViewIssues,
        },
        {
          path: "summary",
          name: "admin_summary",
          component: AdminSummary,
        },
      ],
    },
    {
      path: "/user",
      name: "user_index",
      component: UserLayout,
      children: [
        {
          path: "board",
          name: "userboard",
          component: UserDashboard,
          props: true,
        },
        {
          path: "issues/view",
          name: "user_issues_view",
          component: UserViewIssues,
        },
        {
          path: "summary",
          name: "user_summary",
          component: UserSummary,
        },
        {
          path: "book/:book_id/review",
          name: "book_review",
          component: UserReviewBook,
          props: true,
        },
      ],
    },
    {
      path: "/admin/login",
      name: "adminlogin",
      component: AdminLogin,
    },
    {
      path: "/user/login",
      name: "userlogin",
      component: UserLogin,
    },
    {
      path: "/user/register",
      name: "user_registration",
      component: Register,
    },
  ],
});

export default router;
