<script setup>
import { ref } from "vue";

const version = "Alpha 0.01";
const buildType = "quantum";
</script>

<template>
  <nav class="main_navigation">
    <h2 class="main_navigation__header">QuantumAI</h2>
    <span class="main_navigation__version"
      >Version {{ version }} {{ buildType }} Build</span
    >
  </nav>
</template>

<style scoped lang="scss">
.main_navigation {
  display: flex;
  align-items: center;

  padding: 0.6rem 2.4rem;

  background-color: #ff6b6b;
  width: 100%;
  transition: all 0.2s;
  margin-bottom: 7.4rem;
  box-shadow: 0 1rem 1rem rgba(0, 0, 0, 0.05);

  &__header {
    color: #fff;
    font-weight: 300;
    font-size: 2.4rem;
    margin: 0;
    margin-right: auto;
  }

  &__version {
    font-weight: 300;
    font-size: 1.2rem;
    text-transform: uppercase;

    color: #fff;
  }
}
</style>
