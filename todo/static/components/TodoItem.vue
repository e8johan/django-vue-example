<template>
    <p>
        <span v-if="item.done" v-on:click="$emit('clear', item.id);">[x]</span>
        <span v-else="" v-on:click="$emit('check', item.id);">[&nbsp;]</span>
        {{ item.text }}
        <img v-bind:src="static_url_trashcan" v-on:click="$emit('delete', item.id);" />
    </p>
</template>

<script>
export default {
    name: "todo-item",
    components: {},
    props: [ 'item' ],
    data: function() { 
        return {
            'static_url_trashcan': context_static_url_trashcan,
        };
    },
    methods: {
    },
    mounted() {
    },
}
</script>
