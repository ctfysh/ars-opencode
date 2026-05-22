/**
 * ARS plugin for OpenCode.ai
 *
 * Registers ars-* skills, 13 commands, and init hook from opencode.json
 * so they appear in the skill/command palette without manual symlinks.
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '../..');

function loadPluginConfig() {
  const configPath = path.join(repoRoot, 'opencode.json');
  if (!fs.existsSync(configPath)) return {};
  try {
    return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  } catch {
    return {};
  }
}

export default () => ({
  config: async (config) => {
    const pluginConfig = loadPluginConfig();

    // Register skills directory so OpenCode discovers ars-* skills
    const arsSkillsDir = path.resolve(repoRoot, 'skills');
    config.skills = config.skills || {};
    config.skills.paths = config.skills.paths || [];
    if (!config.skills.paths.includes(arsSkillsDir)) {
      config.skills.paths.push(arsSkillsDir);
    }

    // Register commands from opencode.json so /ars-* commands appear in palette
    if (pluginConfig.commands) {
      config.commands = config.commands || {};
      for (const [name, relPath] of Object.entries(pluginConfig.commands)) {
        const absPath = path.resolve(repoRoot, relPath);
        if (!config.commands[name]) {
          config.commands[name] = absPath;
        }
      }
    }

    // Register init hook
    if (pluginConfig.init && !config.init) {
      config.init = path.resolve(repoRoot, pluginConfig.init);
    }
  },
});
