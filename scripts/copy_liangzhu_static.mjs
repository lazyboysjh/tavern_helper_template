import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/** src 中需原样复制到 dist 的静态资源（webpack 不会自动产出） */
const copies = [
  ['src/梁祝/界面/行动选项/styles.css', 'dist/梁祝/界面/行动选项/styles.css'],
  ['src/梁祝/界面/行动选项/controller.js', 'dist/梁祝/界面/行动选项/controller.js'],
];

for (const [fromRel, toRel] of copies) {
  const from = path.join(root, fromRel);
  const to = path.join(root, toRel);
  if (!fs.existsSync(from)) {
    console.warn(`[copy_liangzhu_static] skip missing: ${fromRel}`);
    continue;
  }
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
  console.log(`[copy_liangzhu_static] ${fromRel} -> ${toRel}`);
}
