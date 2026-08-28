/**
 * Form submission handler for the interview form
 * Compiled from form-handler.ts
 */
/**
 * Initialize form event listeners
 */
function initializeFormHandler() {
    const form = document.querySelector('form');
    if (!form) {
        console.error('Form not found');
        return;
    }
    form.addEventListener('submit', handleFormSubmit);

    // Add event listener for generateSummary checkbox to show/hide improvementQuestions
    const generateSummaryCheckbox = document.getElementById('generateSummary');
    const improvementQuestionsGroup = document.getElementById('improvementQuestionsGroup');
    const improvementQuestionsInput = document.getElementById('improvementQuestions');

    if (generateSummaryCheckbox && improvementQuestionsGroup && improvementQuestionsInput) {
        const updateImprovementQuestionState = function () {
            const shouldRequire = generateSummaryCheckbox.checked;
            improvementQuestionsGroup.style.display = shouldRequire ? 'flex' : 'none';
            improvementQuestionsInput.required = shouldRequire;

            if (!shouldRequire) {
                improvementQuestionsInput.value = '';
            }
        };

        generateSummaryCheckbox.addEventListener('change', updateImprovementQuestionState);
        updateImprovementQuestionState();
    }

    loadTopics();
}

/**
 * Load topics from API and populate topic dropdown.
 */
async function loadTopics() {
    const topicSelect = document.getElementById('topic');
    if (!topicSelect) {
        return;
    }

    try {
        const response = await fetch('/api/topics');
        if (!response.ok) {
            throw new Error(`Failed to load topics: ${response.status}`);
        }

        const data = await response.json();
        const topics = Array.isArray(data.topics) ? data.topics : [];

        if (!topics.length) {
            return;
        }

        topicSelect.innerHTML = '';

        const placeholderOption = document.createElement('option');
        placeholderOption.value = '';
        placeholderOption.textContent = '-- Choose a topic --';
        topicSelect.appendChild(placeholderOption);

        topics.forEach(function (topic) {
            const option = document.createElement('option');
            option.value = topic;
            option.textContent = topic;
            topicSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading topics:', error);
    }
}

/**
 * Update form status message based on API response
 */
function updateSubmissionStatus(statusElement, response, data) {
    if (!statusElement) {
        return;
    }

    if (response.ok) {
        statusElement.className = 'status-message success';
        const resultPath = data.results || '';
        const fileName = resultPath.split(/[\\/]/).pop() || resultPath;
        const link = document.createElement('a');
        link.href = resultPath;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = fileName || 'Open file';
        statusElement.innerHTML = 'File saved: ';
        statusElement.appendChild(link);
        return;
    }

    statusElement.className = 'status-message error';
    statusElement.textContent = `Error: ${data.message || data.error || 'Unknown error occurred'}`;
}
/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    const statusElement = document.getElementById('form-status');
    const interviewIdInput = document.getElementById('interviewId');
    const topicSelect = document.getElementById('topic');
    const genderInput = document.querySelector('input[name="gender"]:checked');
    const skipTranscriptCheckbox = document.getElementById('skipTranscript');
    const generateSummaryCheckbox = document.getElementById('generateSummary');
    const analyzeTranscriptCheckbox = document.getElementById('analyzeTranscript');
    const improvementQuestionsInput = document.getElementById('improvementQuestions');
    const interviewId = (interviewIdInput === null || interviewIdInput === void 0 ? void 0 : interviewIdInput.value) || '';
    const topic = (topicSelect === null || topicSelect === void 0 ? void 0 : topicSelect.value) || '';
    const gender = (genderInput === null || genderInput === void 0 ? void 0 : genderInput.value) || '';
    const skipTranscript = (skipTranscriptCheckbox === null || skipTranscriptCheckbox === void 0 ? void 0 : skipTranscriptCheckbox.checked) || false;
    const generateSummary = (generateSummaryCheckbox === null || generateSummaryCheckbox === void 0 ? void 0 : generateSummaryCheckbox.checked) || false;
    const analyzeTranscript = (analyzeTranscriptCheckbox === null || analyzeTranscriptCheckbox === void 0 ? void 0 : analyzeTranscriptCheckbox.checked) || false;
    const improvementQuestions = (improvementQuestionsInput === null || improvementQuestionsInput === void 0 ? void 0 : improvementQuestionsInput.value) || '';

    if (statusElement) {
        statusElement.className = 'status-message';
        statusElement.textContent = '';
    }
    // Validate required fields
    if (!interviewId || !topic || !gender) {
        if (statusElement) {
            statusElement.className = 'status-message error';
            statusElement.textContent = 'Please fill in all required fields.';
        }
        return;
    }

    if (generateSummary && !improvementQuestions.trim()) {
        if (statusElement) {
            statusElement.className = 'status-message error';
            statusElement.textContent = 'Improvement Question Numbers is required when Generate Summary is checked.';
        }
        return;
    }

    if (!generateSummary && !analyzeTranscript) {
        if (statusElement) {
            statusElement.className = 'status-message error';
            statusElement.textContent = 'Please select Generate Summary or AnalyzeTranscript to proceed.';
        }
        return;
    }

    try {
        const formData = {
            interviewId,
            topic,
            gender,
            skipTranscript,
            generateSummary,
            analyzeTranscript,
            improvementQuestions
        };
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        updateSubmissionStatus(statusElement, response, data);
    } catch (error) {
        console.error('Error submitting form:', error);
        if (statusElement) {
            statusElement.className = 'status-message error';
            statusElement.textContent = 'An error occurred while submitting the form. Please try again.';
        }
    }
}
// Initialize the form handler when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeFormHandler);
