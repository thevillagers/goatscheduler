<template>
    <div class="TaskWrapper" v-bind:style="block.state == 'SUCCESS' ? 'background-color: green;' : 'background-color: #cbcbcb;'">
        <div class="Task">
            <h5><b>{{ block.name }}</b></h5>
            <p>{{ block.state }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Task',
    props: {
        block: Object
    }
}
</script>


<style scoped>
.TaskWrapper {
    margin: 10px;
    width: 250px;
    height: 100px;
    border: solid 1px black;
}


/* nothin yet */
</style>
