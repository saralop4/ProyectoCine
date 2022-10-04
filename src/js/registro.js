import { $ } from './utils.js'

const register = $('#formRegister')
const btn = $('#btnRegister')


const registerUser = (event) => { 
    event.preventDefault()

    const formData = Object.fromEntries(new FormData(event.target))
    
    console.log({formData})
    btn.disabled = true
 }

register?.addEventListener("submit", registerUser )
