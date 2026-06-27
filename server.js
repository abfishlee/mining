const express = require('express');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 9001;
const PYTHON_BIN = process.env.PYTHON_BIN || 'python';
const PYTHON_TIMEOUT_MS = 30000;
const PROBLEMS_DIR = path.join(__dirname, 'problems');
const MAX_COLLECTED_FILE_BYTES = 1024 * 1024;

// 정적 파일 제공 (HTML, CSS, JS 등)
app.use(express.static(path.join(__dirname, 'public')));
// JSON 파싱 미들웨어 추가
app.use(express.json());

function readProblemSet(fileName) {
    if (!/^[a-zA-Z0-9_-]+\.json$/.test(fileName)) {
        throw new Error('잘못된 문제집 파일명입니다.');
    }

    const filePath = path.join(PROBLEMS_DIR, fileName);
    const resolvedPath = path.resolve(filePath);
    const resolvedProblemsDir = path.resolve(PROBLEMS_DIR);

    if (!resolvedPath.startsWith(resolvedProblemsDir + path.sep)) {
        throw new Error('허용되지 않은 문제집 경로입니다.');
    }

    return JSON.parse(fs.readFileSync(resolvedPath, 'utf8'));
}

function isSafeOutputFile(fileName) {
    return /^[a-zA-Z0-9_.-]+\.csv$/.test(fileName);
}

function parseCsvLine(line) {
    const values = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i += 1) {
        const char = line[i];
        const next = line[i + 1];

        if (char === '"' && inQuotes && next === '"') {
            current += '"';
            i += 1;
        } else if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            values.push(current);
            current = '';
        } else {
            current += char;
        }
    }

    values.push(current);
    return values;
}

function parseCsvSummary(content) {
    const lines = content.replace(/^\uFEFF/, '').split(/\r?\n/).filter((line) => line.length > 0);
    if (lines.length === 0) {
        return { columns: [], rowCount: 0, nullCounts: {}, numericStats: {}, sampleRows: [] };
    }

    const columns = parseCsvLine(lines[0]).map((column) => column.trim());
    const rows = lines.slice(1).map(parseCsvLine);
    const nullCounts = {};
    const numericStats = {};

    columns.forEach((column, index) => {
        let numericCount = 0;
        let min = Infinity;
        let max = -Infinity;
        let sum = 0;
        let nullCount = 0;
        let first = null;
        let last = null;
        let previousNumber = null;
        let strictlyIncreasing = true;
        const distinctValues = new Set();

        rows.forEach((row) => {
            const raw = row[index] == null ? '' : String(row[index]).trim();
            if (raw === '' || raw.toLowerCase() === 'nan' || raw.toLowerCase() === 'null') {
                nullCount += 1;
                return;
            }

            if (first == null) first = raw;
            last = raw;
            distinctValues.add(raw);

            const value = Number(raw);
            if (Number.isFinite(value)) {
                numericCount += 1;
                min = Math.min(min, value);
                max = Math.max(max, value);
                sum += value;
                if (previousNumber != null && value <= previousNumber) strictlyIncreasing = false;
                previousNumber = value;
            }
        });

        nullCounts[column] = nullCount;
        if (numericCount > 0) {
            numericStats[column] = {
                count: numericCount,
                min,
                max,
                mean: sum / numericCount,
                first: Number(first),
                last: Number(last),
                uniqueCount: distinctValues.size,
                strictlyIncreasing: numericCount === rows.length - nullCount && strictlyIncreasing
            };
        }
    });

    const sampleRows = rows.slice(0, 3).map((row) => {
        const sample = {};
        columns.forEach((column, index) => {
            sample[column] = row[index] ?? '';
        });
        return sample;
    });

    return { columns, rowCount: rows.length, nullCounts, numericStats, sampleRows };
}

function collectOutputFiles(fileNames) {
    return fileNames
        .filter(isSafeOutputFile)
        .map((fileName) => {
            const filePath = path.resolve(__dirname, fileName);
            const rootPath = path.resolve(__dirname);

            if (!filePath.startsWith(rootPath + path.sep)) {
                return { name: fileName, exists: false, error: '허용되지 않은 파일 경로입니다.' };
            }

            if (!fs.existsSync(filePath)) {
                return { name: fileName, exists: false };
            }

            const stat = fs.statSync(filePath);
            if (stat.size > MAX_COLLECTED_FILE_BYTES) {
                return { name: fileName, exists: true, size: stat.size, error: '파일이 너무 커서 검사하지 않았습니다.' };
            }

            const content = fs.readFileSync(filePath, 'utf8');
            const csv = parseCsvSummary(content);
            try { fs.unlinkSync(filePath); } catch (e) {}

            return {
                name: fileName,
                exists: true,
                size: stat.size,
                csv
            };
        });
}

// 문제은행 목록 API
app.get('/api/problem-sets', (req, res) => {
    if (!fs.existsSync(PROBLEMS_DIR)) {
        return res.json({ sets: [] });
    }

    const sets = fs.readdirSync(PROBLEMS_DIR)
        .filter((file) => file.endsWith('.json'))
        .map((file) => {
            const data = readProblemSet(file);
            return {
                file,
                page: data.page,
                title: data.title,
                problemCount: Array.isArray(data.problems) ? data.problems.length : 0
            };
        });

    res.json({ sets });
});

// 문제집 상세 API
app.get('/api/problem-sets/:file', (req, res) => {
    try {
        res.json(readProblemSet(req.params.file));
    } catch (error) {
        res.status(404).json({ error: error.message });
    }
});

// 파이썬 코드 실행 API
app.post('/api/run-python', (req, res) => {
    const { code, collectFiles = [] } = req.body;
    
    if (!code) {
        return res.status(400).json({ success: false, output: '코드가 비어있습니다.' });
    }

    const tempDir = path.join(__dirname, 'temp');
    if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir);
    }

    const scriptPath = path.join(tempDir, `script_${Date.now()}.py`);
    fs.writeFileSync(scriptPath, code, 'utf8');

    const safeCollectFiles = Array.isArray(collectFiles) ? collectFiles.filter(isSafeOutputFile) : [];
    safeCollectFiles.forEach((fileName) => {
        const outputPath = path.resolve(__dirname, fileName);
        if (outputPath.startsWith(path.resolve(__dirname) + path.sep) && fs.existsSync(outputPath)) {
            try { fs.unlinkSync(outputPath); } catch (e) {}
        }
    });

    // 파이썬 실행 (timeout 설정으로 무한루프 방지)
    exec(`"${PYTHON_BIN}" "${scriptPath}"`, { timeout: PYTHON_TIMEOUT_MS, cwd: __dirname }, (error, stdout, stderr) => {
        // 임시 파일 삭제
        try { fs.unlinkSync(scriptPath); } catch (e) {}
        const files = collectOutputFiles(safeCollectFiles);

        if (error) {
            if (error.killed) {
                return res.json({ success: false, output: `실행 시간 초과 (${PYTHON_TIMEOUT_MS / 1000}초). 무한 루프 또는 너무 오래 걸리는 연산이 의심됩니다.`, files });
            }
            return res.json({ success: false, output: stderr || error.message, files });
        }
        res.json({ success: true, output: stdout, files });
    });
});

app.listen(PORT, () => {
    console.log(`\n======================================================`);
    console.log(`🚀 나의 학습 대시보드가 포트 ${PORT}에서 성공적으로 실행되었습니다!`);
    console.log(`👉 브라우저를 열고 http://localhost:${PORT} 로 접속하세요.`);
    console.log(`======================================================\n`);
});
