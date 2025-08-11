import { DateTime } from "luxon";

export default function parseDateString(input: string): Date {
  const currentYear = new Date().getFullYear();
  const formats = [
    "ccc, LLLL d, ha", // Sat, March 1, 8AM
    "LLLL d, ha", // March 1, 8AM
    "LLLL d, HH:mm", // March 1, 20:00
    "LLLL d", // March 1 (assume 12AM)
  ];

  for (const format of formats) {
    const dt = DateTime.fromFormat(input, format, { zone: "local" });
    if (dt.isValid) {
      return dt.set({ year: currentYear }).toJSDate();
    }
  }

  console.error("Invalid date string:", input);
  return DateTime.local().toJSDate();
}
