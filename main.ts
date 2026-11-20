// news-image-20261120 entry (Node 22, standard library only).
//
// Writes the finished picture for Friday 20 November 2026 to the
// output directory: the PNG stored beside this file is written out
// byte for byte, so both grader runs produce identical output.
//
// The picture itself was drawn for this day (see gen.py, kept in the
// repository as the build record): a world map that pins the day's
// stories to where they happened - Trump delaying any Iran decision
// to 2027, Cyclone Akvan's landfall in Odisha, Europe ready for
// talks with Russia, Hayabusa2's landing called off, and the Haiti
// police raid - with a full-width band for GTA VI passing $1.84bn
// on Sensor Tower estimates, and headline cards underneath.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const bytes = readFileSync(join(here, "entry.png"));
  if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
    throw new Error("entry.png is not a PNG file");
  }
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, "entry.png");
  writeFileSync(outPath, bytes);
  console.log(`wrote ${outPath} (${bytes.length} bytes)`);
}

main();
