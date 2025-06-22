<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router"
import HelloWorld from "./components/HelloWorld.vue"
import { computed, ref } from "vue"


interface Note {
  id: string
  title: string
  content: string
  createdAt: Date
  updatedAt: Date
}

const notes = ref<Note[]>([])
const activeNoteId = ref<string | null>(null)

const addNewNote = (): void => {
  const newNote: Note = {
    id: Date.now().toString(),
    title: '',
    content: '',
    createdAt: new Date(),
    updatedAt: new Date()
  }
  notes.value.unshift(newNote)
  activeNoteId.value = newNote.id
  saveNotes()
}


const saveNotes = (): void => {
  if (activeNote.value) {
    activeNote.value.updatedAt = new Date()
  }
  localStorage.setItem('notes', JSON.stringify(notes.value))
}


const deleteNote = (noteId: String) => {
}


const selectNote = (noteId: String) => {

}


const formatDate = (date: Date): string => {
  return date?.toLocaleString() || ''
}


const activeNote = computed(() => {
  return notes.value.find(note => note.id === activeNoteId.value)
})
</script>

<template>
  <div class="notes-app">
    <div class="notes-sidebar">
      <h2 class="sidebar-title">Мои заметки</h2>
      <button class="add-note-btn" @click="addNewNote">+ Новая заметка</button>
      <ul class="notes-list">
        <li
          v-for="note in notes"
          :key="note.id"
          :class="{ active: activeNoteId === note.id }"
          @click="selectNote(note.id)"
        >
          <div class="note-title">{{ note.title || 'Без названия' }}</div>
          <div class="note-preview">{{ note.content.substring(0, 30) }}...</div>
          <button class="delete-note-btn" @click.stop="deleteNote(note.id)">×</button>
        </li>
      </ul>
    </div>
    
    <div class="notes-content">
      <template v-if="activeNote">
        <input
          v-model="activeNote.title"
          class="note-title-input"
          placeholder="Введите заголовок"
        />
        <textarea
          v-model="activeNote.content"
          class="note-content-input"
          placeholder="Начните писать заметку..."
        ></textarea>
        <div class="note-meta">
          Последнее изменение: {{ formatDate(activeNote.updatedAt) }}
        </div>
      </template>
      <div v-else class="no-note-selected">
        <p>Выберите заметку или создайте новую</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.notes-app {
  display: flex;
  height: 100vh;
  font-family: 'Arial', sans-serif;
}

.notes-sidebar {
  width: 300px;
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  padding: 20px;
  overflow-y: auto;
}

.sidebar-title {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.add-note-btn {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.add-note-btn:hover {
  background-color: #45a049;
}

.notes-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notes-list li {
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
  position: relative;
}

.notes-list li:hover {
  background-color: #ebebeb;
}

.notes-list li.active {
  background-color: #e0e0e0;
}

.note-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.note-preview {
  color: #666;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-note-btn {
  position: absolute;
  right: 10px;
  top: 10px;
  background: none;
  border: none;
  color: #999;
  font-size: 20px;
  cursor: pointer;
  padding: 0 5px;
}

.delete-note-btn:hover {
  color: #f44336;
}

.notes-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.note-title-input {
  width: 100%;
  padding: 10px;
  font-size: 24px;
  border: none;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 20px;
  outline: none;
}

.note-content-input {
  flex: 1;
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  resize: none;
  outline: none;
  line-height: 1.6;
}

.note-meta {
  margin-top: 10px;
  color: #999;
  font-size: 14px;
}

.no-note-selected {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #999;
}
</style>
