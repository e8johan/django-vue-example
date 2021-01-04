<template>
    <div>
        <input v-model="textentry" placeholder="Enter todo"> <button v-on:click="on_add_click">Add</button>
        <hr />
        <todo-list 
            v-bind:items="items"
            
            v-on:clear="on_clear"
            v-on:check="on_check"
            v-on:delete="on_delete"
        ></todo-list>
        <hr />
        <button v-on:click='on_reload_click'>Reload</button>
    </div>
</template>

<script>
import axios from 'axios';

import TodoList from './TodoList.vue'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

export default {
    name: "todoapp",
    components: { TodoList },
    data: function() { 
        return {
            'textentry': '',
            'items': []
        };
    },
    methods: {
        /* Event handlers */
        
        'on_clear': function(id) {
            const index = this.index_from_id(id);
            if (index != -1) {
                this.items[index].done = false;
                axios.patch('/api/todo/' + id + '/', { done: false })
                    .then((response) => {
                        if (response.data.id == id) {
                            this.items[index].done = response.data.done;
                        }                        
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
        },
        'on_check': function(id) {
            const index = this.index_from_id(id);
            if (index != -1) {
                this.items[index].done = true;
                axios.patch('/api/todo/' + id + '/', { done: true })
                    .then((response) => {
                        if (response.data.id == id) {
                            this.items[index].done = response.data.done;
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
        },
        'on_delete': function(id) {
            const index = this.index_from_id(id);
            if (index != -1) {
                axios.delete('/api/todo/' + id + '/')
                    .then((response) => {
                        this.items.splice(index,1);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
        },
        'on_add_click': function() {
            axios.post('/api/todo', { text: this.textentry })
                .then((response) => {
                    this.items.push(response.data);
                })
                .catch((error) => {
                    console.log(error);
                });

            this.textentry = '';
        },
        'on_reload_click': function() {
            this.items = [];
            axios.get('/api/todo')
                .then((response) => {
                    this.items = response.data;
                })
                .catch((error) => {
                    console.log(error);
                });
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
