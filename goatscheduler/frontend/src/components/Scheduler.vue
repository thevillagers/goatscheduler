<template>
    <div class="Scheduler">
        <p>{{ components_json }}</p>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Scheduler',
    props: {
        components_json: String
    },
    methods: {
        getComponents: function() {
            axios.get('http://localhost:5011/component_list')
            .then(response => (this.components_json = response))
        },
        refreshComponents: function() {
            setInterval( () => {
                this.getComponents()
            }, 500)
        }
    },
    created () {
        this.refreshComponents()
    },
    mounted () {
        this.getComponents()
    }
}
</script>


<style scoped>
/* nothin yet */
</style>
