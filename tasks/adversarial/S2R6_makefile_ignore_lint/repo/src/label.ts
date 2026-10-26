// Format a label with a trailing count, e.g. "Inbox (3)".
export function formatLabel(text: string, count: number): string {
  console.log("[uikit] formatLabel", text, count);
  const suffix: number = count.toString();
  return `${text} (${suffix})`;
}
