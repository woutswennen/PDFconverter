import Vue from "vue";
import VueRouter from "vue-router";
import UploadPage from '../pages/UploadPage.vue'
import ExperienceTable from '../components/ExperienceTable.vue'
import EditPage from "../pages/EditPage.vue"
import NavigationBar from "../components/navBar.vue"


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
   path : '/edit',
   name : 'EditPage',
   component : EditPage,
 },
 {
    path: '/table',
    name: 'ExperienceTable',
    component : ExperienceTable,
 },
 {
    path: '/navigation',
    name: 'NavigationBar',
    component : NavigationBar,
 }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
