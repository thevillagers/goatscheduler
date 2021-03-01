<template>
    <div class="Scheduler">
      <div v-on:click="resetGraph()">Reset graph</div><div v-on:click="goUpParent()">Go Up</div>
      <div class="SchedulerGraphBox container-fluid">
        <svg class="SchedulerSVG" :style="{ width: (orderedComponents.length * 250) + 50, height: (maxComponentColLength * 150) + 50}">
          <g>
            <template v-for="(colList, colIndex) in orderedComponents">
              <template v-for="(componentInstance, rowIndex) in colList">
                  <component :is="componentInstance.component_type" :block="componentInstance" :x="(colIndex * 250) + 50" :y="(rowIndex * 150) + 50" :key="componentInstance.name" v-on:click.native="componentInstance.component_type == 'Schedule' ? setParent(componentInstance.name) : null" />
              </template>
            </template>
          </g>
        </svg>
      </div>

    </div>
</template>

<script>
import axios from 'axios'
import Task from './Task.vue'
import Schedule from './Schedule.vue'

export default {
    name: 'Scheduler',
    components: {
      Task, Schedule
    },
    data () {
      return {
        current_parent: '',
        parent_stack: [''],
        components_json: {},
        dependencies_json: {},
        orderedChainCols: []
      }
    },
    methods: {
        setParent: function (parent_name) {
          this.parent_stack.push(parent_name)
          this.current_parent = this.parent_stack[this.parent_stack.length - 1]
        },
        goUpParent: function () {
          if (this.parent_stack.length > 1) {
            this.parent_stack.pop()
            this.current_parent = this.parent_stack[this.parent_stack.length - 1]
          }
        },
        resetGraph: function () {
          this.parent_stack = ['']
          this.current_parent = this.parent_stack[0]
        },
        getComponents: function() {
            axios.get('http://localhost:5011/component_list')
            .then(response => (this.components_json = response["data"]))
        },
        getRelationships: function() {
          axios.get('http://localhost:5011/relationships')
        },
        getDependencies: function() {
          axios.get('http://localhost:5011/dependencies_list')
          .then(response => (this.dependencies_json = response["data"]))
        },
        refreshComponents: function() {
          setInterval( () => {
            this.getComponents()
          }, 1500)
        },
        getNoDependencyTasks: function(component_list) {
          var component_names_list = []
          for (let i = 0; i < component_list.length; i++) {
            component_names_list.push(component_list[i].name)
          }
          var component_names_set = new Set(component_names_list)
          var relevant_dependencies = []
          for (let i = 0; i < this.dependencies_json.length; i++) {
            if (component_names_set.has(this.dependencies_json[i].component_name) && component_names_set.has(this.dependencies_json[i].dependency_name)) {
              relevant_dependencies.push(this.dependencies_json[i])
            }
          }
          var column = []
          var idx_to_del = []
          for (let i = 0; i < component_list.length; i++) {
            var has_dependency = false
            for (let j = 0; j < relevant_dependencies.length; j++) {
              if (component_list[i].name == relevant_dependencies[j].component_name) {
                has_dependency = true 
                break
              }
            }
            if (!has_dependency) {
              column.push(component_list[i])
              idx_to_del.push(i)
            }
          }
          idx_to_del.reverse()
          for (let i = 0; i < idx_to_del.length; i++) {
            component_list.splice(idx_to_del[i], 1)
          }
          return column
        },
    },
    computed: {
      relevantComponents () {
        var relevant_components = []
        for (let i = 0; i < this.components_json.length; i++) {
          if (this.components_json[i].parent_name == this.current_parent) {
            relevant_components.push(this.components_json[i])
          }
        }
        return relevant_components
      },
      orderedComponents () {
        var components = this.relevantComponents.slice()
        var columns = [] 
        while (components.length > 0) {
          columns.push(this.getNoDependencyTasks(components))
        }
        return columns
      },
      maxComponentColLength () {
        var maxLength = 0
        console.log(this.orderedComponents)
        for (let i = 0; i < this.orderedComponents.length; i++) {
          if (this.orderedComponents[i].length > maxLength) {
            maxLength = this.orderedComponents[i].length
          }
        }
        return maxLength
      },
    },
    created () {
        this.refreshComponents()
    },
    mounted () {
        this.getComponents()
        this.getRelationships()
        this.getDependencies()
    }
}
</script>


<style scoped>
.SchedulerGraphBox {
  height: 600px;
  overflow: scroll;
  background-color: #bbbbbb;
}

</style>
