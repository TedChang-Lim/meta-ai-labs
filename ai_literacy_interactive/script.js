// Phase 1: Spot the Human Quiz
function selectQuiz(choiceId) {
    // Clear previous selection styles
    for (let i = 1; i <= 3; i++) {
        const card = document.getElementById(`q-choice-${i}`);
        card.classList.remove('selected', 'correct', 'incorrect');
    }

    const selectedCard = document.getElementById(`q-choice-${choiceId}`);
    selectedCard.classList.add('selected');

    const resultBox = document.getElementById('quiz-result');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultText = document.getElementById('result-text');

    resultBox.classList.remove('hidden', 'correct-style', 'incorrect-style');

    if (choiceId === 2) {
        // Correct Answer (B)
        selectedCard.classList.remove('selected');
        selectedCard.classList.add('correct');
        resultBox.classList.add('correct-style');
        resultIcon.textContent = '🎉';
        resultTitle.textContent = '정답입니다! (인간의 답변)';
        resultText.textContent = '답변 B는 자신의 부끄러운 경험을 고백하고, 완벽한 솔루션보다는 서툴지만 따뜻한 유대(맛있는 거나 먹으러 가자)를 제안합니다. 이것이 인간다운 대화와 감정적 연결의 핵심입니다. 반면 A와 C는 인위적으로 학습된 문장이거나 기계적인 포맷입니다.';
    } else {
        // Incorrect Answer (A or C)
        selectedCard.classList.remove('selected');
        selectedCard.classList.add('incorrect');
        resultBox.classList.add('incorrect-style');
        resultIcon.textContent = '❌';
        resultTitle.textContent = '아쉽지만 오답입니다! (AI의 답변)';
        if (choiceId === 1) {
            resultText.textContent = '답변 A는 전형적인 감정형 챗봇의 과장된 답변입니다. AI는 24시간 대기하고 100% 공감한다고 말하지만, 이는 실시간 데이터 연산일 뿐 진짜 감정을 느끼는 것이 아닙니다. 여기에 과도하게 감정을 이입하면 심리적 의존성이 생길 수 있습니다.';
        } else {
            resultText.textContent = '답변 C는 전형적인 도구형 AI의 기계적 답변입니다. 효율적이지만 친밀함이나 공감은 존재하지 않는 단순 계산 및 분기 처리 결과입니다.';
        }
    }
}

// Phase 3: Self-Diagnosis Checklist & Gauge
function calculateScore() {
    const totalQuestions = 7;
    let checkedCount = 0;

    for (let i = 1; i <= totalQuestions; i++) {
        const checkbox = document.getElementById(`check-${i}`);
        const label = document.getElementById(`label-check-${i}`);
        
        if (checkbox.checked) {
            checkedCount++;
            label.classList.add('checked-item');
        } else {
            label.classList.remove('checked-item');
        }
    }

    // Needle rotation calculation
    // Min score (0): -90deg, Max score (7): 90deg.
    // Total span: 180 degrees. Step = 180 / 7 = 25.71 degrees.
    const startDegree = -90;
    const stepDegree = 180 / totalQuestions;
    const targetDegree = startDegree + (checkedCount * stepDegree);

    const needle = document.getElementById('gauge-needle');
    needle.style.transform = `rotate(${targetDegree}deg)`;

    const scoreDisplay = document.getElementById('gauge-score');
    scoreDisplay.textContent = `${checkedCount}점`;

    const statusDisplay = document.getElementById('gauge-status');
    const descDisplay = document.getElementById('gauge-desc');

    statusDisplay.classList.remove('safe', 'warning', 'danger');

    if (checkedCount <= 2) {
        statusDisplay.textContent = '안전 (SAFE)';
        statusDisplay.classList.add('safe');
        descDisplay.textContent = '현재는 건강하게 AI를 하나의 편리한 도구로 활용하고 있습니다. 스스로 필터링하는 능력이 뛰어납니다.';
    } else if (checkedCount <= 5) {
        statusDisplay.textContent = '주의 (WARNING)';
        statusDisplay.classList.add('warning');
        descDisplay.textContent = 'AI 사용 시간이 지나치게 길거나, 생각의 주도권을 부분적으로 빼앗기고 있을 수 있습니다. 가끔씩 AI를 끄고 내 힘으로 생각하는 훈련이 필요합니다.';
    } else {
        statusDisplay.textContent = '위험 (DANGER)';
        statusDisplay.classList.add('danger');
        descDisplay.textContent = 'AI 의존도가 매우 심각합니다! 과제 대필 등으로 생각 근육이 마비되거나, 인공지능에 감정을 지나치게 쏟고 있을 확률이 높습니다. 사람들과의 현실 대화 시간을 즉각 늘리세요.';
    }
}
