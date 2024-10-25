async function createRule() {
    const ruleString = document.getElementById('ruleString').value;

    const response = await fetch('/rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_string: ruleString }),
    });

    const data = await response.json();
    displayOutput(data.message || data.detail);
}

async function evaluateRule() {
    const ruleId = document.getElementById('ruleId').value;
    const userData = document.getElementById('userData').value;

    const response = await fetch(`/rules/evaluate/${ruleId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(JSON.parse(userData)),
    });

    const data = await response.json();
    displayOutput(data.result ? 'Rule evaluated to True' : 'Rule evaluated to False');
}

async function combineRules() {
    const rulesToCombine = document.getElementById('rulesToCombine').value.split(',');

    const response = await fetch('/rules/combine', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rules: rulesToCombine }),
    });

    const data = await response.json();
    displayOutput(data.message || data.detail);
}

function displayOutput(message) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerText = message;
    outputDiv.style.display = 'block';
}

document.getElementById('createRuleBtn').onclick = createRule;
document.getElementById('evaluateRuleBtn').onclick = evaluateRule;
document.getElementById('combineRulesBtn').onclick = combineRules;
