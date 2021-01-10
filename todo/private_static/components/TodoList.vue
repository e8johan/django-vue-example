<template>
    <div>
        <todo-item v-for="item in items" v-bind:item="item" v-on="$listeners"></todo-item>
    </div>
</template>

<script>
import TodoItem from './TodoItem.vue'

export default {
    name: "todo-list",
    components: { TodoItem },
    props: [ 'items' ],
    data: function() { 
        return {
        };
    },
    methods: {
    },
    mounted() {
    },
}
</script>
