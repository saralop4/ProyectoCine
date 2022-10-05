// @ts-check
/**
 * @param {String} element identificador
 * @returns 
 */
export const $ = (element) => document.querySelector(element)

/**
 * @param {string} mail Correo electronico a evaluar
 * @returns boolean
 */
export const validateEmail = (mail) => {
  const regex = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
  return regex.test(mail)
}

/**
 * @param {string} str String a formatear
 */
export const sanitizeString = (str = '') => {
  const newStr = String(str).replace(/[^A-Za-z ]/g, '').trim()
  const arrStr = newStr.split(' ')
  let sanitized = ''

  arrStr.forEach((word) => {
    const lowerWord = word.toLowerCase()
    const formated = lowerWord[0].toUpperCase() + lowerWord.slice(1)
    sanitized += formated + ' '
  })
  return sanitized.trim()
}

export const isNumber = (value) => !isNaN(value) && typeof Number(value) === 'number'