<template>
    <todo-list 
        v-bind:items="items"
        
        v-on:clear="on_clear"
        v-on:check="on_check"
    ></todo-list>
</template>

<script>
import TodoList from './TodoList.vue'

export default {
    name: "todoapp",
    components: { TodoList },
    data: function() { 
        return {
            'items': []
        };
    },
    methods: {
        /* Event handlers */
        
        'on_clear': function(id) {
            const index = this.index_from_id(id);
            if (index != -1) {
                this.items[index].done = false;
            }
        },
        'on_check': function(id) {
            const index = this.index_from_id(id);
            if (index != -1) {
                this.items[index].done = true;
            }
        },
        
        /* Functions */
        'index_from_id': function(id) {
            for (var ii=0; ii<this.items.length; ++ii) {
                if (this.items[ii].id == id) {
                    return ii;
                }
            }
            
            return -1;
        },
    },
    mounted() {
        this.items = context_items;
    },
}
</script>
