import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// fungsi untuk mengconvert salary ke rupiah
// contoh: 10000000 -> Rp 10.000.000
// contoh: 1000000-5000000 -> Rp 1.000.000 - Rp 5.000.000
export function convertToRupiah(salary: string) {
  if (salary === "Secret") {
    return salary;
  }

  const parts = salary.split("-").map((part) => {
    return parseInt(
      part.replace("Rp", "").replace(/\s/g, "").replace(/\./g, ""),
      10
    );
  });

  return parts
    .map((part) => {
      return `Rp ${part.toLocaleString()}`;
    })
    .join(" - ");
}
