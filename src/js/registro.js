import { $, isNumber, sanitizeString, validateEmail } from './utils.js'

const register = $('#formRegister')
const btn = $('#btnRegister')
const alert = $('#alertRegister')

const response = {
    error: true,
    body: ''
}

const validarFormData = (event) => {
    alert.innerHTML = ''
    let nombre = event.target[0].value
    let apellido = event.target[1].value
    const genero = event.target[2].value
    const identificacion = Number(event.target[3].value)
    const celular = Number(event.target[4].value)
    const ciudad = event.target[5].value
    const email = event.target[6].value
    const confirmEmail = event.target[7].value
    const password = event.target[8].value
    const confirmPassword = event.target[9].value

    if (nombre === '') response.body += `<li>El campo nombre esta vacio.</li>`
    else nombre = sanitizeString(nombre)

    if (apellido === '') response.body += `<li>El campo apellido esta vacio.</li>`
    else apellido = sanitizeString(apellido)

    if (!isNumber(identificacion) || identificacion === 0) response.body += `<li>La identifiación esta incorrecta.</li>`
    if (!isNumber(celular) || celular === 0) response.body += `<li>En el campo celular solo se permiten números.</li>`
    if (!validateEmail(email)) response.body += `<li>En correo electrónico es invalido.</li>`
    if (ciudad.length === 0) response.body += `<li>Debe elegir una ciudad.</li>`
    if (!validateEmail(confirmEmail)) response.body += `<li>El correo electrónico de confirmación es invalido.</li>`
    if ((email.trim() !== confirmEmail.trim()) || (email.length === 0 || confirmEmail.length === 0)) response.body += `<li>Los correos no coinciden</li>`
    if ((password.trim() !== confirmPassword.trim()) || (password.length === 0 || confirmPassword.length === 0)) response.body += `<li>Las contraseñas no coinciden</li>`

    return response
}

const clearAlert = () => {
    document.querySelector('#alertRegister').innerHTML = ""
    alert.classList.remove('invisible')
        alert.classList.add('visible')
}

const registerUser = (event) => {
    event.preventDefault()
    btn.disabled = true
    clearAlert()

    try {
        const { error, body } = validarFormData(event)
        

        if (error) {
            alert.innerHTML = `
            <ul>${body}</ul>
         `
        }


    } catch (error) {
        console.log({ error })
        alert.textContent = error
        alert.classList.remove('invisible')
        alert.classList.add('visible')
    } finally {
        btn.disabled = false
    }

}

register?.addEventListener("submit", registerUser, false)
