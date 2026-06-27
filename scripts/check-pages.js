const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '..', 'public');
const pages = fs.readdirSync(publicDir).filter((file) => file.endsWith('.html'));
const failures = [];

function getInlineScripts(html) {
  const scripts = [];
  const scriptPattern = /<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  while ((match = scriptPattern.exec(html)) !== null) {
    scripts.push(match[1]);
  }
  return scripts;
}

for (const page of pages) {
  const html = fs.readFileSync(path.join(publicDir, page), 'utf8');
  const hasEditor = html.includes('id="python-editor"');
  const hasRunButton = html.includes('id="run-btn"');
  const hasConsole = html.includes('id="console-output"');
  const hasRunFunction = html.includes('async function runPython');
  const hasRunnerUi = hasEditor || hasRunButton || hasConsole || hasRunFunction;

  if (hasRunnerUi && !(hasEditor && hasRunButton && hasConsole && hasRunFunction)) {
    failures.push(
      `${page}: incomplete Python runner ` +
        `(editor=${hasEditor}, button=${hasRunButton}, console=${hasConsole}, runPython=${hasRunFunction})`
    );
  }

  getInlineScripts(html).forEach((script, index) => {
    try {
      new Function(script);
    } catch (error) {
      failures.push(`${page}: inline script ${index + 1} syntax error: ${error.message}`);
    }
  });
}

if (failures.length > 0) {
  console.error('Page health check failed:');
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`Page health check passed (${pages.length} HTML files).`);
