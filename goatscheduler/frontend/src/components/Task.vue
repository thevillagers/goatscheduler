<template>
    <div class="TaskWrapper" v-bind:style="block.state == 'SUCCESS' ? 'background-color: green;' : 'background-color: #cbcbcb;'">
        <svg width="200" height="100" viewBox="0 0 200 100">
            <g fill="none" stroke="black">
                <text x="50%" y="20" dominant-baseline="middle" text-anchor="middle">TASK:</text>
                <text x="50%" y="40" dominant-baseline="middle" text-anchor="middle">{{ block.name }}</text>
                <text x="50%" y="80" dominant-baseline="middle" text-anchor="middle">STATUS: {{ block.state }}</text>
            </g>
        </svg>
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
    width: 200px;
    height: 100px;
    border: solid 1px black;
}


/* nothin yet */
</style>
