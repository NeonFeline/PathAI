<script setup>
import { ref } from "vue";

const version = "Alpha 0.01";
const buildType = "Prototype";
</script>

<template>
  <nav class="main_navigation">
    <span class="main_navigation__version"
      >Version {{ version }} {{ buildType }} Build</span
    >
  </nav>
</template>

<style scoped lang="scss">
.main_navigation {
  display: flex;
  align-items: center;

  padding: 1.2rem 2.4rem;

  background-color: var(--main-color);
  transition: all 0.2s;

  &__logo {
    height: 2.8rem;
    margin-right: auto;
  }

  &__version {
    font-weight: 300;
    font-size: 2.4rem;
    text-transform: uppercase;

    color: #fff;
  }
}
</style>
