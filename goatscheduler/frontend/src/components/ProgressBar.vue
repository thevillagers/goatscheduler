<template>
    <div class="progress">
        <div
            class="progress-bar"
            role="progressbar"
            :style="'width: ' + percent+'%;'"
            :aria-valuenow="percent"
            aria-valuemin="0"
            aria-valuemax="100">.</div>
        <p>{{ percent }}%</p>
        <p>{{ APIData }}</p>
    </div>
</template>

<script>
export default {
    name: 'ProgressBar',
    props: {
        percent: {default: 0}
    },
    methods: {
        startInterval: function() {
            setInterval( () => {
                if (this.percent < 100) {
                    this.percent = this.percent + 1
                }
            }, 250);
        },
    },
    created () {
        this.startInterval()
    }
}
</script>


<style scoped>
.progress-bar {
    color: black;
    background-color: black;
}
</style>
