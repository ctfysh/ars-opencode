/**
 * ARS plugin for OpenCode.ai
 *
 * Registers ars-* skills (ars-meta, ars-deep-research, ars-academic-paper,
 * ars-reviewer, ars-pipeline) and their commands/hooks so they appear in
 * the skill/command palette without manual symlinks.
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const arsSkillsDir = path.resolve(__dirname, '../../skills');

export default () => ({
  config: async (config) => {
    // Register skills directory so OpenCode discovers ars-* skills
    config.skills = config.skills || {};
    config.skills.paths = config.skills.paths || [];
    if (!config.skills.paths.includes(arsSkillsDir)) {
      config.skills.paths.push(arsSkillsDir);
    }
  },
});
