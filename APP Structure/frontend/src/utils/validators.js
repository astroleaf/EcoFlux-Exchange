/**
 * Validators
 * Input validation utilities
 */

/**
 * Validate email
 */
export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

/**
 * Validate energy type
 */
export const validateEnergyType = (type) => {
  const validTypes = ['solar', 'wind', 'hydro', 'biomass']
  return validTypes.includes(type.toLowerCase())
}

/**
 * Validate quantity
 */
export const validateQuantity = (quantity) => {
  const num = parseFloat(quantity)
  return !isNaN(num) && num > 0
}

/**
 * Validate price
 */
export const validatePrice = (price) => {
  const num = parseFloat(price)
  return !isNaN(num) && num > 0
}

/**
 * Validate order type
 */
export const validateOrderType = (type) => {
  return ['buy', 'sell'].includes(type.toLowerCase())
}

/**
 * Validate required fields
 */
export const validateRequired = (value) => {
  if (typeof value === 'string') {
    return value.trim().length > 0
  }
  return value !== null && value !== undefined
}

/**
 * Validate number range
 */
export const validateRange = (value, min, max) => {
  const num = parseFloat(value)
  return !isNaN(num) && num >= min && num <= max
}

/**
 * Validate trade form
 */
export const validateTradeForm = (formData) => {
  const errors = {}

  if (!validateRequired(formData.energy_type)) {
    errors.energy_type = 'Energy type is required'
  } else if (!validateEnergyType(formData.energy_type)) {
    errors.energy_type = 'Invalid energy type'
  }

  if (!validateRequired(formData.quantity)) {
    errors.quantity = 'Quantity is required'
  } else if (!validateQuantity(formData.quantity)) {
    errors.quantity = 'Quantity must be a positive number'
  }

  if (!validateRequired(formData.price)) {
    errors.price = 'Price is required'
  } else if (!validatePrice(formData.price)) {
    errors.price = 'Price must be a positive number'
  }

  if (!validateRequired(formData.order_type)) {
    errors.order_type = 'Order type is required'
  } else if (!validateOrderType(formData.order_type)) {
    errors.order_type = 'Invalid order type'
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}
