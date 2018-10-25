<template>
  <v-container fluid>
      <v-layout column align-center>
        <img src="@/assets/logo.png" alt="Vuetify.js" class="mb-5">
        <blockquote>
          &#8220;Do not pray for tasks equal to your powers. Pray for powers equal to your tasks.&#8221;
          <footer>
            <small>
              <em>&mdash;Phillips Brooks</em>
            </small>
          </footer>
        </blockquote>
        <v-btn class='mt-5' outline color="indigo" large :to="{path: '/tasks'}">Go to Tasks</v-btn>
      </v-layout>
  </v-container>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
