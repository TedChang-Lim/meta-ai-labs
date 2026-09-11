
// STEP 01: Spot the Human Quiz
function selectQuiz(choiceId) {
    for (let i = 1; i <= 3; i++) {
        const card = document.getElementById(`q-choice-${i}`);
        if (card) card.classList.remove('selected', 'selected-correct', 'selected-wrong');
    }

    const selectedCard = document.getElementById(`q-choice-${choiceId}`);
    const resultBox = document.getElementById('quiz-result');
    const resultBadge = document.getElementById('result-badge');
    const resultTitle = document.getElementById('result-title');
    const resultText = document.getElementById('result-text');

    resultBox.classList.remove('hidden');

    if (choiceId === 2) {
        selectedCard.classList.add('selected-correct');
        resultBadge.textContent = 'CORRECT · 정답';
        resultBadge.style.background = '#22c55e';
        resultTitle.textContent = '정답입니다! (살아있는 인간의 답변)';
        resultText.textContent = '답변 B는 자신의 부끄럽거나 아팠던 경험을 솔직하게 고백하며, 기계적인 3단계 해결책 대신 서툴지만 따뜻한 유대("나중에 맛있는 밥이나 먹자")를 건넵니다. 이것이 인간다운 대화와 정서적 연결의 본질입니다. 반면 A와 C는 실시간 데이터 연산으로 조립된 전형적인 AI 문장입니다.';
    } else {
        selectedCard.classList.add('selected-wrong');
        resultBadge.textContent = 'INCORRECT · 오답';
        resultBadge.style.background = '#ef4444';
        resultTitle.textContent = '아쉽지만 오답입니다! (인공지능의 연산 답변)';
        if (choiceId === 1) {
            resultText.textContent = '답변 A는 감정형 챗봇의 과장된 시뮬레이션입니다. AI는 24시간 대기하고 100% 무조건 공감한다고 말하지만, 이는 고통을 함께 겪는 것이 아닌 텍스트 연산일 뿐입니다. 여기에 과도하게 감정을 의존하면 현실 인간관계로부터 고립될 수 있습니다.';
        } else {
            resultText.textContent = '답변 C는 전형적인 도구형 AI의 매뉴얼식 답변입니다. 효율적인 정보 나열일 뿐, 인간다운 온기나 공감은 전혀 존재하지 않습니다.';
        }
    }
}

// STEP 03: Self-Diagnosis Checklist & Needle Rotation
function calculateScore() {
    const totalQuestions = 7;
    let checkedCount = 0;

    for (let i = 1; i <= totalQuestions; i++) {
        const checkbox = document.getElementById(`check-${i}`);
        const label = document.getElementById(`label-check-${i}`);
        
        if (checkbox && checkbox.checked) {
            checkedCount++;
            if (label) label.classList.add('checked-item');
        } else {
            if (label) label.classList.remove('checked-item');
        }
    }

    // Needle rotation: Min (-90deg), Max (90deg) -> 180 deg / 7 = 25.71 deg per point
    const startDegree = -90;
    const stepDegree = 180 / totalQuestions;
    const targetDegree = startDegree + (checkedCount * stepDegree);

    const needle = document.getElementById('gauge-needle');
    if (needle) needle.style.transform = `rotate(${targetDegree}deg)`;

    const scoreDisplay = document.getElementById('gauge-score');
    if (scoreDisplay) scoreDisplay.textContent = `${checkedCount}점`;

    const statusDisplay = document.getElementById('gauge-status');
    const descDisplay = document.getElementById('gauge-desc');

    if (!statusDisplay || !descDisplay) return;

    statusDisplay.classList.remove('safe', 'warning', 'danger');

    if (checkedCount <= 2) {
        statusDisplay.textContent = '안전 (SAFE)';
        statusDisplay.classList.add('safe');
        descDisplay.textContent = '현재 건강하게 AI를 하나의 편리한 도구로 통제하고 있습니다. 스스로 비판하고 필터링하는 메타인지 능력이 뛰어납니다.';
    } else if (checkedCount <= 5) {
        statusDisplay.textContent = '주의 (WARNING)';
        statusDisplay.classList.add('warning');
        descDisplay.textContent = 'AI 사용 시간이 지나치게 길거나 생각의 주도권을 부분적으로 빼앗기고 있습니다. 의도적으로 AI를 끄고 내 힘으로 글을 쓰고 판단하는 훈련이 시급합니다.';
    } else {
        statusDisplay.textContent = '위험 (DANGER)';
        statusDisplay.classList.add('danger');
        descDisplay.textContent = 'AI 의존도가 매우 심각합니다! 과제/보고서 단순 복붙으로 생각 근육이 마비되었거나, 감정을 AI에 쏟고 있을 위험이 큽니다. 현실의 사람들과 대화 시간을 늘리고 자가 교정을 시작하세요.';
    }
}
