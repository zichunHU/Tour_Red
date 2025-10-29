// Utility to resolve theme or duration label with i18n and optional icons
// code: string from backend (may be a theme code or a duration)
// t: i18n translator
// icons: optional mapping from code to icon
export function resolveThemeTag(code, t, icons = {}) {
  if (!code) return { icon: '', label: '' }

  // Try themes dictionary first
  const themeLabel = t(`themes.${code}`)
  if (themeLabel !== `themes.${code}`) {
    return { icon: icons[code] || '', label: themeLabel }
  }

  // Map known duration codes to routes.* keys
  const durationKeyMap = {
    '半日游': 'halfDay',
    '一日游': 'oneDay',
    '多日游': 'multiDay',
    'halfDay': 'halfDay',
    'oneDay': 'oneDay',
    'multiDay': 'multiDay'
  }
  const durKey = durationKeyMap[code]
  if (durKey) {
    return { icon: '', label: t(`routes.${durKey}`) }
  }

  // Fallback: show raw code
  return { icon: icons[code] || '', label: code }
}

// Helper: determine if a code represents duration
export function isDurationCode(code) {
  return [
    '半日游', '一日游', '多日游',
    'halfDay', 'oneDay', 'multiDay'
  ].includes(code)
}

// Resolve duration tag strictly from duration code
export function resolveDurationTag(code, t) {
  if (!code) return { icon: '', label: '' }
  const map = {
    '半日游': 'halfDay',
    '一日游': 'oneDay',
    '多日游': 'multiDay',
    'halfDay': 'halfDay',
    'oneDay': 'oneDay',
    'multiDay': 'multiDay'
  }
  const key = map[code]
  if (!key) return { icon: '', label: code }
  return { icon: '⏱️', label: t(`routes.${key}`) }
}