<template>
  <v-app-bar
      app
      color="primary"
      dark
  >
    <div class="d-flex align-center">
      <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
      />
      <h1>Online store</h1>
    </div>
    <v-spacer></v-spacer>
    <v-btn to="/login">Login</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header',
  props: {
    showAddTask: Boolean,
  }
}
</script>
