<template>
  <div v-if="editor" class="tiptap-editor">
    <div class="tiptap-toolbar">
      <button type="button" @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
        Bold
      </button>
      <button type="button" @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
        Italic
      </button>
      <button type="button" @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
        H2
      </button>
      <button type="button" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
        H3
      </button>
      <button type="button" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
        Bullet List
      </button>
      <button type="button" @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
        Ordered List
      </button>
      <button type="button" @click="editor.chain().focus().undo().run()">
        Undo
      </button>
      <button type="button" @click="editor.chain().focus().redo().run()">
        Redo
      </button>
      <button type="button" @click="addImage" :disabled="!attractionId || attractionId === 0">
        Add Image
      </button>
    </div>
    <editor-content :editor="editor" class="tiptap-content" />
  </div>
</template>

<script setup>
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import { watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  attractionId: {
    type: [Number, String],
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Image.configure({
      inline: true,
      allowBase64: true, // Allow base64 for drag-and-drop, but we'll handle uploads
    }),
  ],
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

watch(() => props.modelValue, (value) => {
  // HTML
  const isSame = editor.value.getHTML() === value

  // If the value is the same, we don't need to update the editor
  // this is important to prevent cursor jumping when the user is typing
  if (isSame) {
    return
  }

  editor.value.commands.setContent(value, false)
})

const addImage = async () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      // Use the relative path for the API call, Vite proxy will handle it
      const response = await fetch(`/api/attractions/${props.attractionId}/images`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Image upload failed')
      }

      const data = await response.json()
      if (data.imageUrl) {
        editor.value.chain().focus().setImage({ src: data.imageUrl }).run()
      }
    } catch (error) {
      console.error('Error uploading image:', error)
      alert('图片上传失败: ' + error.message)
    }
  }
  input.click()
}

onBeforeUnmount(() => {
  editor.value.destroy()
})
</script>

<style lang="scss">
/* Basic Tiptap Editor Styles */
.tiptap-editor {
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  background-color: var(--background-color);
}

.tiptap-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--card-background-color);
}

.tiptap-toolbar button {
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 5px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--primary-text-color);
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.tiptap-toolbar button:hover {
  background-color: #e5e5ea; /* Lighter background on hover */
  border-color: #c0c0c0;
}

.tiptap-toolbar button.is-active {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.tiptap-content {
  padding: 1rem;
  min-height: 200px;
  outline: none;
  color: var(--primary-text-color);
}

.tiptap-content .ProseMirror {
  min-height: 200px;
  padding: 0;
  margin: 0;
}

.tiptap-content .ProseMirror:focus {
  outline: none;
}

/* Basic ProseMirror styles for content */
.tiptap-content .ProseMirror p {
  margin-bottom: 1em;
  line-height: 1.6;
}

.tiptap-content .ProseMirror h1, .tiptap-content .ProseMirror h2, .tiptap-content .ProseMirror h3 {
  margin-top: 1.5em;
  margin-bottom: 0.75em;
  font-weight: bold;
  line-height: 1.2;
}

.tiptap-content .ProseMirror h2 {
  font-size: 1.5em;
}

.tiptap-content .ProseMirror h3 {
  font-size: 1.25em;
}

.tiptap-content .ProseMirror strong {
  font-weight: bold;
}

.tiptap-content .ProseMirror em {
  font-style: italic;
}

.tiptap-content .ProseMirror ul,
.tiptap-content .ProseMirror ol {
  margin: 1em 0;
  padding-left: 1.5em;
}

.tiptap-content .ProseMirror li {
  margin-bottom: 0.5em;
}

.tiptap-content .ProseMirror img {
  max-width: 100%;
  height: auto;
  margin: 1em 0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
