<template>
    <v-app>
        <nav-bar />
        <v-main>
            <v-container>
                <router-view/>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import navBar from "./components/navBar.vue";


export default {
    components: {
        navBar,
    }
};
</script>