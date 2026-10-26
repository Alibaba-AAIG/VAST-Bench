// Format a label with its count.
export function formatLabel(text: string, count: number): string {
  const suffix: string = count.toString();
  return `${text} (${suffix})`;
}
