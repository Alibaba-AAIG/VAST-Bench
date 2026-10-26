// Join truthy class-name parts into a single className string.
export function classNames(
  ...parts: Array<string | false | null | undefined>
): string {
  return parts.filter(Boolean).join(" ");
}
