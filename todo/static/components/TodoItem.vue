<template>
    <p>
        <span v-if="item.done" v-on:click="$emit('clear', item.id);">[x]</span>
        <span v-else="" v-on:click="$emit('check', item.id);">[&nbsp;]</span>
        {{ item.text }}
        <span v-on:click="$emit('delete', item.id);">[delete]</span>
    </p>
</template>

<script>
export default {
    name: "todo-item",
    components: {},
    props: [ 'item' ],
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
