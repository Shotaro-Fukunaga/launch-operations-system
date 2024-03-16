export const roundToOneDecimalPlace = (num: number) => {
  return Math.round(num * 10) / 10
}

export const roundToPrecision = (number: number, precision: number) => {
  const factor = Math.pow(10, precision)
  return Math.round(number * factor) / factor
}

export const truncateToPrecision = (number: number, precision: number): number => {
  const factor = Math.pow(10, precision);
  return Math.floor(number * factor) / factor;
}

export const formatTime = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = seconds % 60

  let formattedTime = ''

  // 年の計算 (1年 = 365日)
  const years = Math.floor(hours / (365 * 24))
  if (years > 0) {
    formattedTime += `${years}y `
  }

  // 日の計算 (残りの時間で日を計算)
  const days = Math.floor((hours % (365 * 24)) / 24)
  if (days > 0 || years > 0) {
    // 年がある場合は0日でも表示
    formattedTime += `${days}d `
  }

  // 時間の計算 (残りの時間)
  const remainingHours = hours % 24
  if (remainingHours > 0 || days > 0 || years > 0) {
    // 日または年がある場合は0時間でも表示
    formattedTime += `${remainingHours}h `
  }

  // 分の計算
  if (minutes > 0 || hours > 0 || days > 0 || years > 0) {
    // 時間、日、年がある場合は0分でも表示
    formattedTime += `${minutes}m `
  }

  // 秒の計算 (1分未満の場合は小数点以下第一位まで表示)
  if (seconds < 60) {
    formattedTime += `${remainingSeconds.toFixed(1)}s`
  } else if (remainingSeconds > 0) {
    // 1分以上で余り秒がある場合は四捨五入して表示
    formattedTime += `${Math.round(remainingSeconds)}s`
  }

  return formattedTime.trim() // 末尾の空白を削除して返す
}

// ラジアンから度へ変換する関数
export const convertRadiansToDegrees = (radians: number) => {
  return radians * (180 / Math.PI)
}
