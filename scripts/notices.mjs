// Preserve the actual bundled packages' copyright and licence notices.
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
const root = process.cwd();
const lock = JSON.parse(readFileSync(resolve(root, 'package-lock.json'), 'utf8'));
const sections = ['Third-party runtime software notices\nGenerated from package-lock.json. Includes transitive runtime packages.\nApplication code: MIT. OSM-derived data: ODbL 1.0 (see data/LICENSE.md).'];
for (const [relative, entry] of Object.entries(lock.packages)) {
  if (!relative || entry.dev) continue;
  let base = root, folder;
  while (true) {
    const candidate = resolve(base, relative);
    if (existsSync(resolve(candidate, 'package.json'))) { folder = candidate; break; }
    if (dirname(base) === base) break;
    base = dirname(base);
  }
  if (!folder) throw new Error(`Missing runtime package: ${relative}`);
  const meta = JSON.parse(readFileSync(resolve(folder, 'package.json'), 'utf8'));
  let files = readdirSync(folder).filter(n => /^(licen[sc]e|copying|notice)(\.|$)/i.test(n));
  // Some npm packages embed their copyright/licence in README or source headers.
  if (!files.length) files = readdirSync(folder).filter(n => /^readme(\.|$)|^murmurhash[23]_gc\.js$/i.test(n));
  if (!files.length) throw new Error(`No licence material: ${meta.name}`);
  sections.push(`${meta.name}@${meta.version}\nDeclared licence: ${JSON.stringify(meta.license)}\n` + files.map(n => `--- ${n} ---\n${readFileSync(resolve(folder, n), 'utf8')}`).join('\n'));
}
writeFileSync(resolve(root, 'public/THIRD_PARTY_NOTICES.txt'), sections.join('\n\n' + '='.repeat(78) + '\n\n'));
