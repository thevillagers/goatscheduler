<template>
    <div class="ScheduleWrapper" v-bind:style="block.state == 'SUCCESS' ? 'background-color: green;' : 'background-color: #cbcbcb;'">
        <div class="Schedule">
            <h5><b>Schedule: {{ block.name }}</b></h5>
            <p>{{ block.state }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Schedule',
    props: {
        block: Object
    }
}
</script>


<style scoped>
.ScheduleWrapper {
    margin: 10px;
    width: 250px;
    height: 100px;
    border: solid 1px black;
}


/* nothin yet */
</style>
