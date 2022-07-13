import Vue from "vue";
import VueRouter from "vue-router";
import UploadPage from '../pages/UploadPage.vue'

import CandidatePage from '../pages/CandidatePage.vue'
import ProfessionalPage from '../pages/ProfessionalPage.vue'
import SkillPage from '../pages/SkillPage.vue'

Vue.use(VueRouter);

const routes = [
 {
   path : '/upload',
   name : 'Upload',
   component : UploadPage,
 },
  {
   path : '/',
   name : 'Upload',
   component : UploadPage,
 },
 {
   path : '/personal',
   name : 'CandidatePage',
   component : CandidatePage,
 },
 {
    path: '/professional',
    name: 'ProfessionalPage',
    component : ProfessionalPage,
 },
 {
    path: '/skills',
    name: 'SkillPage',
    component : SkillPage,
 }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
