<template>
    <svg v-bind:x="x" v-bind:y="y" width="200" height="100" viewBox="0 0 200 100" class="ScheduleWrapper">
        <g>
            <rect width="200" height="100" v-bind:fill="block.state == 'SUCCESS' ? 'green' : 'none'" stroke="black" />
            <text x="50%" y="20" dominant-baseline="middle" text-anchor="middle">SCHEDULE:</text>
            <text x="50%" y="40" dominant-baseline="middle" text-anchor="middle">{{ block.name }}</text>
            <text x="50%" y="80" dominant-baseline="middle" text-anchor="middle">STATUS: {{ block.state }}</text>
        </g>
    </svg>
</template>

<script>
export default {
    name: 'Schedule',
    props: {
        block: Object,
        x: Number,
        y: Number
    }
}
</script>


<style scoped>
.ScheduleWrapper {
    margin: 10px;
    width: 200px;
    height: 100px;
    border: solid 1px black;
}

/* nothin yet */
</style>
