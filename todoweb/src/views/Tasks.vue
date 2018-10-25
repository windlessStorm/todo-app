<template>
<v-layout align-center justify-center row wrap>
      <v-flex xs12>
      <v-toolbar
        transparent
        tabs
      >
        <v-spacer/>
        <v-toolbar-title v-if="!search">Tasks</v-toolbar-title>
      <v-btn v-if="search" dark @click="clearSearch">
          clear search result
        </v-btn>
      <v-dialog v-model="dialog" persistent max-width="500px" v-if="!search">
       <v-btn icon slot="activator">
          <v-icon color='blue' large>add_circle_outline</v-icon>
        </v-btn>
      <v-card>
        <v-card-title>
          <span class="headline">Create Task</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field label="Title" required v-model="taskTitle"></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Description" v-model="taskDescription"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-menu
                  ref="menu2"
                  :close-on-content-click="false"
                  v-model="menu2"
                  :nudge-right="40"
                  :return-value.sync="taskDate"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="290px"
                >
                  <v-text-field
                    slot="activator"
                    v-model="taskDate"
                    label="Due date"
                    prepend-icon="event"
                    readonly
                  ></v-text-field>
                  <v-date-picker v-model="taskDate" @input="$refs.menu2.save(taskDate)" color="green lighten-1"></v-date-picker>
                </v-menu>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click.native="createTask()">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
<!--
        <v-btn icon @click="showModal()">
          <v-icon color='blue' large>add_circle_outline</v-icon>
        </v-btn>
    -->
        <v-spacer/>
        <v-text-field
            v-model="searchTerm"
            label="Search"
            clearable
            small
            @keyup.enter.native="searchTask(searchTerm)"
        ></v-text-field>
      </v-toolbar>
      <v-tabs fixed-tabs grow icons-and-text v-model="selectedTab" v-if="!search">
        <v-tab href="#todo" @click="selectTab('todo')">
          To Do
          <v-icon>alarm</v-icon>
        </v-tab>
        <v-tab href="#completed" @click="selectTab('completed')">
          Completed
          <v-icon>done_all</v-icon>
        </v-tab>
      </v-tabs>
      <v-toolbar
        transparent
        flat
         v-if="selectedTab==='todo'"
      >
      <v-spacer/>
      <v-radio-group v-model="currentFilter" row>
              <v-radio
                v-for="(filter, i) in filterlist"
                :key="i"
                :label="filter"
                :value="filter"
              ></v-radio>
            </v-radio-group>
      </v-toolbar>
  </v-flex>
<div v-if="this.displaylist">
        <v-flex xs12>
          <v-card
          color="transparent"
          width="40vw"
          class="my-3 mx-2 elevation-3"
          style="padding:1px 0 1px 0"
          v-for="task in displaylist" :key="task.id"
          >
            <div class="my-2 mx-2">
              <v-layout row wrap>
                <v-flex xs8>
                  <div class="title font-weight-regular ml-2" >
                    {{task.title}}
                  </div>
                </v-flex>

                <v-flex xs4>
                  <div class='text-xs-right caption font-weight-regular mr-3'>
                    Due Date:
                    <div>
                     {{task.due_date}}
                    </div>
                  </div>
                </v-flex>
                <v-flex xs4>
                  <div class="caption py-1">
                    <div class="text-xs-left body-1 ml-2">
                      {{task.description}}
                    </div>
                  </div>
                </v-flex>
              </v-layout>
            </div>
            <v-divider class="mx-3" light></v-divider>
            <v-card-actions v-if="task.status==='Pending'">
              <v-btn block color="green" class='mx-5' @click.native="completeTask(task.resource_uri)">Mark Complete</v-btn>
                        <v-btn block color="red" class='mx-5' @click.native="deleteTask(task.resource_uri)">Delete</v-btn>
            </v-card-actions>
            <v-card-actions v-if="task.status==='Completed'">
              <v-btn block color="blue" class='mx-5' @click.native="reopenTask(task.resource_uri)">Re-open</v-btn>
            <v-btn block color="red" class='mx-5' @click.native="deleteTask(task.resource_uri)">Delete</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
</div>
        </v-layout>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
import addTask from '@/components/addTask'

// let backendUrl = 'https://todo-app-django.herokuapp.com'
let backendUrl = 'http://localhost:8000'

export default {
  components: {
    addTask
  },
  data: () => ({
    tasklist: [],
    displaylist: [],
    selectedTab: 'todo',
    currentFilter: 'All',
    filterlist: ['All', 'Due Today', 'Due this week', 'Due next week', 'Overdue'],
    dialog: false,
    taskDate: null,
    menu: false,
    modal: false,
    menu2: false,
    taskTitle: null,
    taskDescription: null,
    search: false,
    searchTerm: null
  }),
  created () {
    axios.get(backendUrl + '/api/v1/task/?format=json')
      .then((response) => {
        console.log(response.data.objects)
        this.tasklist = response.data.objects
        this.selectTab('todo')
      })
  },
  methods: {
    selectFilter () {
      let filter = this.currentFilter
      if (filter === 'All') {
        this.showTodo()
      } else if (filter === 'Due Today') {
        this.dueToday()
      } else if (filter === 'Due this week') {
        this.dueThisWeek()
      } else if (filter === 'Due next week') {
        this.dueNextWeek()
      } else if (filter === 'Overdue') {
        this.overdue()
      }
      console.log('Display list created: ', this.displaylist)
    },
    selectTab (tabname) {
      this.selectedTab = tabname
      if (this.selectedTab === 'todo') {
        this.selectFilter()
        console.log(this.displaylist)
      } else if (this.selectedTab === 'completed') {
        this.showCompleted()
      }
    },
    showAll () {
      this.displaylist = this.tasklist.filter(
        task => task.soft_deleted === false
      )
    },
    showTodo () {
      this.displaylist = this.tasklist.filter(
        task => task.status === 'Pending' && task.soft_deleted === false
      )
    },
    showCompleted () {
      this.displaylist = this.tasklist.filter(
        task => task.status === 'Completed' && task.soft_deleted === false
      )
    },
    showDeleted () {
      this.displaylist = this.tasklist.filter(
        task => task.soft_deleted === true
      )
    },
    dueToday () {
      let today = moment()
      this.displaylist = this.tasklist.filter(
        task => task.status === 'Pending' &&
        task.soft_deleted === false &&
        today.diff(moment(task.due_date, 'YYYY-MM-DD'), 'days') === 0
      )
    },
    dueThisWeek () {
      let today = moment()
      this.displaylist = this.tasklist.filter(
        task => task.status === 'Pending' &&
        task.soft_deleted === false &&
        today.diff(moment(task.due_date, 'YYYY-MM-DD'), 'days') <= 0 &&
        today.diff(moment(task.due_date, 'YYYY-MM-DD'), 'days') >= -7
      )
      /*
      for (let task of this.tasklist) {
        console.log('Diff of due date for all tasks', today.diff(moment(task.due_date, 'YYYY-MM-DD')))
      }
      */
    },
    dueNextWeek () {
      let today = moment()
      this.displaylist = this.tasklist.filter(
        task => task.status === 'Pending' &&
        task.soft_deleted === false &&
        today.diff(moment(task.due_date, 'YYYY-MM-DD'), 'days') <= 0 &&
        today.diff(moment(task.due_date, 'YYYY-MM-DD'), 'days') >= -14
      )
    },
    overdue () {
      let today = moment()
      this.displaylist = this.tasklist.filter(
        task => task.status === 'Pending' &&
        task.soft_deleted === false &&
        today.diff(moment(task.due_date, 'YYYY-MM-DD'), 'days') > 0
      )
    },
    completeTask (resourceUri) {
      axios.put(
        backendUrl + resourceUri,
        {
          status: 'Completed'
        }
      ).then(
        this.getAllTasks()
      )
    },
    reopenTask (resourceUri) {
      axios.put(
        backendUrl + resourceUri,
        {
          status: 'Pending'
        }
      ).then(
        this.getAllTasks()
      )
    },
    deleteTask (resourceUri) {
      axios.put(
        backendUrl + resourceUri,
        {
          soft_deleted: true,
          delete_time: moment().format('YYYY-MM-DD')
        }
      ).then(
        this.getAllTasks()
      )
    },
    createTask () {
      let data = {
        'title': this.taskTitle,
        'description': this.taskDescription,
        'delete_time': null,
        'due_date': this.taskDate,
        'parent': null,
        'soft_deleted': false,
        'status': 'Pending'
      }
      axios.post(
        backendUrl + '/api/v1/task/',
        data
      ).then(
        this.dialog = false,
        this.getAllTasks()
      )
    },
    getAllTasks () {
      axios.get(backendUrl + '/api/v1/task/?format=json')
        .then((response) => {
          // console.log(response.data.objects)
          this.tasklist = response.data.objects
          if (this.selectedTab === 'todo') {
            this.selectTab('todo')
          } else if (this.selectedTab === 'completed') {
            this.selectTab('completed')
          }
        })
    },
    searchTask (searchTerm) {
      axios.get(backendUrl + '/api/v1/task/?format=json&title__contains=' + searchTerm)
        .then((response) => {
          console.log(response.data.objects)
          this.tasklist = response.data.objects
          this.displaylist = this.tasklist
          this.search = true
        })
    },
    clearSearch () {
      this.searchTerm = null
      this.search = false
      this.getAllTasks()
    }
  },
  watch: {
    currentFilter (value) {
      this.selectFilter(value)
    }
  }
}
</script>
