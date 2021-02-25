<template>
    <div class="Scheduler">
      <div class="SchedulerGraphBox container-fluid">
        <p v-on:click="setParent('')">Reset graph</p>
        <div class="row">
          <div class="col" v-for="component_data in relevantComponents" :key="component_data.name">
            <component :is="component_data.component_type" :block="component_data" :key="component_data.name" v-on:click.native="component_data.component_type == 'Schedule' ? setParent(component_data.name) : null" />
          </div>
        </div>
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
        components_json: {},
        dependencies_json: {}
      }
    },
    methods: {
        setParent: function (parent_name) {
          this.current_parent = parent_name
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
      orderedChain () {
        var components = this.relevantComponents
        var component_names = new Set(components)
        var relevant_dependencies = []
        for (let i = 0; i < this.dependencies_json.length; i++) {
          if (component_names.has(this.dependencies_json[i].component_name) && component_names.has(this.dependencies_json[i].dependency_name)) {
            relevant_dependencies.push(this.dependencies_json[i])
          }
        }

        var columns = []
        var baseColumn = []
        var idx_to_del = []
        for (let i = 0; i < components.length; i++) {
          var has_dependency = false
          for (let j = 0; j < relevant_dependencies.length; j++) {
            if (components[i].name == relevant_dependencies[j].component_name) {
              has_dependency = true 
              break
            }
          }
          if (!has_dependency) {
            baseColumn.push(components[i])
            idx_to_del.push(i)
          }
        }
        idx_to_del.reverse()
        for (let i = 0; i < idx_to_del.length; i++) {
          components.splice(idx_to_del[i], 1)
        }
        columns.push(baseColumn)

        while (components.length > 0) {
          console.log(components.length)
          var remaining_components = new Set(components)
          relevant_dependencies = []
          for (let i = 0; i < this.dependencies_json.length; i++) {
            if (remaining_components.has(this.dependencies_json[i].component_name) && remaining_components.has(this.dependencies_json[i].dependency_name)) {
              relevant_dependencies.push(this.dependencies_json[i])
            }
          }
          var column = []
          idx_to_del = []
          for (let i = 0; i < components.length; i++) {
            has_dependency = false
            for (let j = 0; j < relevant_dependencies.length; j++) {
              if (components[i].name == relevant_dependencies[j].component_name) {
                has_dependency = true 
                break
              }
            }
            if (!has_dependency) {
              column.push(components[i])
              idx_to_del.push(i)
            }
          }
          idx_to_del.reverse()
          for (let i = 0; i < idx_to_del.length; i++) {
            components.splice(idx_to_del[i], 1)
          }
          columns.push(column)
        }
        return columns
      }
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
  background-color: #aaaaaa;
  overflow: scroll;
}
</style>
