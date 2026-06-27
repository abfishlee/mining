const fs = require('fs');
const path = require('path');

const problemsDir = path.join(__dirname, '..', 'problems');
const failures = [];

if (!fs.existsSync(problemsDir)) {
  console.log('Problem check skipped: no problems directory yet.');
  process.exit(0);
}

const files = fs.readdirSync(problemsDir).filter((file) => file.endsWith('.json'));

for (const file of files) {
  const fullPath = path.join(problemsDir, file);
  let data;
  try {
    data = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
  } catch (error) {
    failures.push(`${file}: invalid JSON: ${error.message}`);
    continue;
  }

  if (!data.page) failures.push(`${file}: missing page`);
  if (!data.title) failures.push(`${file}: missing title`);
  if (!Array.isArray(data.problems) || data.problems.length === 0) {
    failures.push(`${file}: problems must be a non-empty array`);
    continue;
  }

  const seenIds = new Set();
  data.problems.forEach((problem, index) => {
    const label = `${file} problems[${index}]`;
    const required = ['id', 'type', 'exam', 'topic', 'difficulty', 'dataset', 'prompt', 'expected', 'rubric', 'commonMistakes'];

    required.forEach((field) => {
      if (problem[field] == null) failures.push(`${label}: missing ${field}`);
    });

    if (problem.id) {
      if (seenIds.has(problem.id)) failures.push(`${label}: duplicate id ${problem.id}`);
      seenIds.add(problem.id);
    }

    if (problem.exam && !Array.isArray(problem.exam)) failures.push(`${label}: exam must be an array`);
    if (problem.topic && !Array.isArray(problem.topic)) failures.push(`${label}: topic must be an array`);
    if (problem.rubric && (!Array.isArray(problem.rubric) || problem.rubric.length === 0)) {
      failures.push(`${label}: rubric must be a non-empty array`);
    }
    if (problem.commonMistakes && !Array.isArray(problem.commonMistakes)) {
      failures.push(`${label}: commonMistakes must be an array`);
    }

    if (problem.expected) {
      const supportedKinds = ['numeric_tolerance', 'multiple_numeric_tolerance', 'rubric_keywords', 'csv_submission'];
      if (!supportedKinds.includes(problem.expected.kind)) {
        failures.push(`${label}: unsupported expected.kind ${problem.expected.kind}`);
      }
      if (problem.expected.kind === 'csv_submission') {
        if (!problem.expected.file) failures.push(`${label}: csv_submission requires file`);
        if (!Array.isArray(problem.expected.columns) || problem.expected.columns.length === 0) {
          failures.push(`${label}: csv_submission requires non-empty columns`);
        }
        if (problem.expected.rowCount == null) failures.push(`${label}: csv_submission requires rowCount`);
        if (problem.expected.numericColumns && typeof problem.expected.numericColumns !== 'object') {
          failures.push(`${label}: csv_submission numericColumns must be an object`);
        }
      }
    }
  });
}

if (failures.length > 0) {
  console.error('Problem bank check failed:');
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`Problem bank check passed (${files.length} JSON files).`);
