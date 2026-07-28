/**
 * Form submission handler for the interview form
 */

interface FormData {
  interviewId: string;
  topic: string;
  gender: string;
  skipTranscript: boolean;
  generateSummary: boolean;
  analyzeTranscript: boolean;
  improvementQuestions: string;
}

interface ApiResponse {
  message: string;
  data?: FormData;
}

interface TopicsResponse {
  topics?: string[];
}

async function loadTopics(): Promise<void> {
  const topicSelect = document.getElementById('topic') as HTMLSelectElement | null;
  if (!topicSelect) {
    return;
  }

  const fallbackOptions = Array.from(topicSelect.options)
    .map((option) => ({ value: option.value, label: option.textContent || '' }))
    .filter((option) => option.value);

  topicSelect.innerHTML = '';
  topicSelect.add(new Option('-- Choose a topic --', ''));

  try {
    const response = await fetch('/api/topics');
    if (!response.ok) {
      throw new Error('Failed to fetch topics');
    }

    const data: TopicsResponse = await response.json();
    const topics = Array.isArray(data.topics) ? data.topics : [];

    for (const topic of topics) {
      topicSelect.add(new Option(topic, topic));
    }
  } catch (error) {
    console.error('Unable to load topics from API:', error);

    for (const option of fallbackOptions) {
      topicSelect.add(new Option(option.label, option.value));
    }
  }
}

/**
 * Initialize form event listeners
 */
function initializeFormHandler(): void {
  const form = document.querySelector('form');
  if (!form) {
    console.error('Form not found');
    return;
  }

  void loadTopics();

  form.addEventListener('submit', handleFormSubmit);

  const generateSummaryCheckbox = document.getElementById('generateSummary') as HTMLInputElement | null;
  const improvementQuestionsGroup = document.getElementById('improvementQuestionsGroup') as HTMLDivElement | null;
  const improvementQuestionsInput = document.getElementById('improvementQuestions') as HTMLInputElement | null;

  if (generateSummaryCheckbox && improvementQuestionsGroup && improvementQuestionsInput) {
    const updateImprovementQuestionState = (): void => {
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
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e: Event): Promise<void> {
  e.preventDefault();

  const interviewIdInput = document.getElementById('interviewId') as HTMLInputElement;
  const topicSelect = document.getElementById('topic') as HTMLSelectElement;
  const genderInput = document.querySelector('input[name="gender"]:checked') as HTMLInputElement | null;
  const skipTranscriptCheckbox = document.getElementById('skipTranscript') as HTMLInputElement;
  const generateSummaryCheckbox = document.getElementById('generateSummary') as HTMLInputElement;
  const analyzeTranscriptCheckbox = document.getElementById('analyzeTranscript') as HTMLInputElement;
  const improvementQuestionsInput = document.getElementById('improvementQuestions') as HTMLInputElement;

  const interviewId = interviewIdInput?.value || '';
  const topic = topicSelect?.value || '';
  const gender = genderInput?.value || '';
  const skipTranscript = skipTranscriptCheckbox?.checked || false;
  const generateSummary = generateSummaryCheckbox?.checked || false;
  const analyzeTranscript = analyzeTranscriptCheckbox?.checked || false;
  const improvementQuestions = improvementQuestionsInput?.value || '';

  // Validate required fields
  if (!interviewId || !topic || !gender) {
    alert('Please fill in all required fields');
    return;
  }

  if (generateSummary && !improvementQuestions.trim()) {
    alert('Improvement Question Numbers is required when Generate Summary is checked.');
    return;
  }

  if (!generateSummary && !analyzeTranscript) {
    alert('Please select Generate Summary or AnalyzeTranscript to proceed.');
    return;
  }

  try {
    const formData: FormData = {
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

    const data: ApiResponse = await response.json();

    if (response.ok) {
      alert(`Success!\nInterview ID: ${interviewId}\nTopic: ${topic}\nSkip Transcript: ${skipTranscript}\nGenerate Summary: ${generateSummary}\nAnalyze Transcript: ${analyzeTranscript}`);
      console.log('Server response:', data);

      // Reset form
      const form = document.querySelector('form') as HTMLFormElement;
      if (form) {
        form.reset();
      }
    } else {
      alert(`Error: ${data.message || 'Failed to submit'}`);
      console.error('Server error:', data);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    alert(`Error submitting form: ${errorMessage}`);
    console.error('Submission error:', error);
  }
}

/**
 * Initialize when DOM is ready
 */
document.addEventListener('DOMContentLoaded', initializeFormHandler);
