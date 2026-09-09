<template>
  <div>
    <button data-cy="increment" @click="count++">+</button>
    <span data-cy="count">{{ count }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ initial?: number }>()
const count = ref(props.initial ?? 0)
</script>
